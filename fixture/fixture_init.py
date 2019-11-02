import logging

import requests
import allure
import tests.conftest

logger = logging.getLogger()

class ApiClient(object):
    """Класс для запросов к API"""

    def __init__(self, address="httpbin.org"):
        """Конструктор"""
        self.address = address

    def __generation_url(self, url):
        """Метод формирования ссылки"""
        logger.info('Формируем адрес для запроса')
        with allure.step('Формируем адрес для запроса'):
            link = "https://{}/{}".format(self.address, url)
            logger.info('Адрес запроса сформирован - {}'.format(link))
            allure.attach('Адрес отправления запроса', link)
            return link

    def post(self, url):
        logger.debug('Отправка POST запроса')
        response = requests.post(self.__generation_url(url))
        return response

    def get(self, url, redirects: bool = None):
        if redirects is not None:
            logger.debug('Отправка GET запроса с указанным параметром редиректа {}'.format(redirects))
            response = requests.get(self.__generation_url(url), allow_redirects=redirects)
        else:
            logger.debug('Отправка GET запроса')
            response = requests.get(self.__generation_url(url))
        return response

    def delete(self, url):
        logger.debug('Отправка DELETE запроса')
        response = requests.delete(self.__generation_url(url))
        return response

    def patch(self, url):
        logger.debug('Отправка PATCH запроса')
        response = requests.patch(self.__generation_url(url))
        return response

    def put(self, url):
        logger.debug('Отправка PUT запроса')
        response = requests.put(self.__generation_url(url))
        return response


class RequestInspection(object):

    def __init__(self):
        """Конструктор"""
        self.api = ApiClient()

    def headers(self):
        logger.debug('Отправляем запрос на страницу headers')
        data = self.api.get('headers')
        return data


class StatusСodes(object):

    def __init__(self):
        """Конструктор"""
        self.api = ApiClient()

    def StatusGet(self, payload):
        logger.debug('Отправляем GET запрос на страницу status/{}'.format(payload))
        data = self.api.get("status/{}".format(payload))
        return data

    def StatusDelete(self, payload):
        logger.debug('Отправляем DELETE запрос на страницу status/{}'.format(payload))
        data = self.api.delete("status/{}".format(payload))
        return data

    def StatusPost(self, payload):
        logger.debug('Отправляем POST запрос на страницу status/{}'.format(payload))
        data = self.api.post("status/{}".format(payload))
        return data

    def StatusPatch(self, payload):
        logger.debug('Отправляем PATCH запрос на страницу status/{}'.format(payload))
        data = self.api.patch("status/{}".format(payload))
        return data

    def StatusPut(self, payload):
        logger.debug('Отправляем PUT запрос на страницу status/{}'.format(payload))
        data = self.api.put("status/{}".format(payload))
        return data

class RedirectN(object):

    def __init__(self):
        """Конструктор"""
        self.api = ApiClient()

    def redirectN(self, payload, redirect: bool = None):
        if redirect is not None:
            logger.debug('Отправляем запрос на страницу redirect/{}'.format(payload))
            logger.debug('Параметр redirect не был передан')
            data = self.api.get("redirect/{}".format(payload), redirects=redirect)
        else:
            logger.debug('Отправляем запрос на страницу redirect/{}'.format(payload))
            logger.debug('Параметр redirect был передан. Значение {}'.format(redirect))
            data = self.api.get("redirect/{}".format(payload))
        return data

class ResponseCheck(object):

    def checkingSuccess(self, response):
        logger.info('Проверяем код ответа')
        with allure.step('Проверяем код ответа'):
            allure.attach('Код ответа', response.status_code)
            assert response.status_code == 200 or response.status_code == 201
            logger.info('Код ответа верный')

    def checkingRedirection(self, response):
        logger.info('Проверяем код ответа')
        with allure.step('Проверяем код ответа'):
            allure.attach('Код ответа', response.status_code)
            assert response.status_code == 300 or response.status_code == 302
            logger.info('Код ответа верный')

    def checkingClientErrors(self, response):
        logger.info('Проверяем код ответа')
        with allure.step('Проверяем код ответа'):
            allure.attach('Код ответа', response.status_code)
            assert response.status_code == 400
            logger.info('Код ответа верный')

    def checkingServerErrors(self, response):
        logger.info('Проверяем код ответа')
        with allure.step('Проверяем код ответа'):
            allure.attach('Код ответа', response.status_code)
            assert response.status_code == 500
            logger.info('Код ответа верный')