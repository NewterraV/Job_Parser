from abc import ABC, abstractmethod
from datetime import datetime
from requests import get, HTTPError
import json

class BaseAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        """Возвращает список вакансий на основе атрибута __response"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """Возвращает максимально возможный список вакансий из API"""
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self, keyword: str) -> None:
        self.__url = 'https://api.hh.ru/vacancies'
        self.keyword = keyword
        self.__response = None
        self.get_response()

    def get_response(self, *args) -> None:
        """Метод делает запрос к API, в качестве аргумента может принимать номер страницы для передачи в API.
                После обновляет атрибут __response полученными данными(dict)"""

        params = {'text': self.keyword,
                  'page': 0 if not args else args[0],
                  'per_page': 100,
                  'search_field': 'name'}
        response = get(self.__url, params=params)

        if not response:
            raise HTTPError(f'Ошибка сервера. Код ответа: {response.status_code}')
        self.__response = response

    def get_vacancies(self) -> list:
        """Возвращает список вакансий на основе атрибута __response"""

        vacancies = []
        for i in self.__response.json()['items']:
            try:
                salary = {'from': i['salary']['from'],
                          'to': i['salary']['to'],
                          'currency': i['salary']['currency']
                          } if i['salary'] else {'from': 0,
                                                 'to': 0,
                                                 'currency': None
                                                 }
                vacancies.append({'aggregator': 'HeadHunter',
                                  'name': i["name"],
                                  'employer': i['employer']['name'],
                                  "salary": salary,
                                  'area': i['area']['name'],
                                  'created': i['created_at'],
                                  'url': i['alternate_url'],
                                  'requirement': i['snippet']['requirement']
                                  })
            except KeyError:
                continue
        return vacancies

    def get_all_vacancies(self) -> list:
        """Возвращает максимально возможный список вакансий из API"""

        all_vacancies = []
        count = 0
        while count < 20:
            self.get_response(count)
            # фильтрация бесполезных обращений к API для уменьшения времени выполнения
            if not self.__response.json()['items']:
                break
            count += 1
            all_vacancies.extend(self.get_vacancies())
        return all_vacancies


class SuperJobAPI(BaseAPI):
    """Класс для работы с API SuperJob"""

    def __init__(self, keyword: str):

        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__token = 'v3.r.137597184.113108d119212cc819e7bd5e4351adf19edb8f31'\
                       '.afada7711de6cfa115505c80d6d45294df15712d'
        self.keyword = keyword
        self.__response = None
        self.get_response()

    def get_response(self, *args) -> None:
        """Метод делает запрос к API, в качестве аргумента может принимать номер страницы для передачи в API.
                После обновляет атрибут __response полученными данными(dict)"""
        params = {'app_key': self.__token,
                  'page': 0 if not args else int(args[0]),
                  'count': 100,
                  'keyword': self.keyword
                  }
        response = get(url=self.__url, params=params)

        if not response:
            raise HTTPError(f'Ошибка сервера. Код ответа: {response.status_code}')
        self.__response = response

    def get_vacancies(self) -> list:
        """Возвращает список вакансий на основе атрибута __response"""
        vacancies = []
        for i in self.__response.json()['objects']:
            try:
                vacancies.append({'aggregator': 'SuperJob',
                                  'name': i["profession"],
                                  'employer': i['firm_name'],
                                  "salary": {'from': i['payment_from'],
                                             'to': i['payment_to'],
                                             'currency': i['currency']
                                             },
                                  'area': i['town']['title'],
                                  'created': datetime.utcfromtimestamp(i['date_published']).isoformat(),
                                  'url': i['link'],
                                  'requirement': f"{i['candidat'][:170]}..." if i['candidat'] else None
                                  })
            except KeyError:
                continue
        return vacancies

    def get_all_vacancies(self) -> list:
        """Возвращает максимально возможный список вакансий из API"""
        all_vacancies = []
        count = 0
        while count < 5:
            self.get_response(count)
            count += 1
            # фильтрация бесполезных обращений к API для уменьшения времени выполнения
            if not self.__response.json()['objects']:
                break
            all_vacancies.extend(self.get_vacancies())
        return all_vacancies