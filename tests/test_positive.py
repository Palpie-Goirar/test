import allure
from tests.fixture.fixture_init import StatusСodes, RequestInspection, ResponseCheck, RedirectN
import pytest

check = ResponseCheck()
status = StatusСodes()


def test_RequestInspection():
    inspection = RequestInspection()

    with allure.step("Отправляем запрос на страницу headers"):
        headers = inspection.headers()

    check.checkingSuccess(headers)

    """Не уверен что это нужно, но думаю что стоит проверять не только код ответа, а что-то и в содержимом,
     пусть будет домен"""
    with allure.step("Проверяем содержимое ответа"):
        hostName = headers.json()['headers']['Host']
        allure.attach('Host', hostName)
        assert hostName == "httpbin.org"


@pytest.mark.parametrize("pageCode, checkMethod", [(200, check.checkingSuccess),
                                                   (300, check.checkingRedirection),
                                                   (400, check.checkingClientErrors),
                                                   (500, check.checkingServerErrors)],
                         ids=["200-code", "300-code", "400-code", "500-code"])
@pytest.mark.parametrize("statuses", [status.StatusGet, status.StatusPost,
                                      status.StatusDelete, status.StatusPatch, status.StatusPut],
                         ids=["Get", "Post", "Delete", "Patch", "Put"])
def test_CheckStatusСodes(pageCode, checkMethod, statuses):
    with allure.step("Отправляем запрос на старницу status"):
        code = statuses(pageCode)

    checkMethod(code)



def test_RedirectN():
    redirect = RedirectN()

    with allure.step("Проверяем что возвращается код ответа редиректа"):
        noRedirection = redirect.redirectN(1, False)
        check.checkingRedirection(noRedirection)

    with allure.step("Проверяем что после редиректов мы получаем 200 код ответа"):
        redirection = redirect.redirectN(5)
        check.checkingSuccess(redirection)


# ToDo Можно так же попробовать считать количество переходов что бы убедиться что все работает как положено
