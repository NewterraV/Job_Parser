from abc import ABC, abstractmethod
from datetime import datetime
from requests import get, HTTPError


class BaseAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self, keyword: str) -> None:
        self.__url = 'https://api.hh.ru/vacancies'
        self.keyword = keyword
        params = {'text': keyword,
                  'page': 10,
                  'per_page': 100,
                  'search_field': 'name'}
        self.response = get(self.__url, params=params)
        self.response_json = self.response.json()

        if not self.response:
            raise HTTPError(f'Ошибка сервера. Код ответа: {self.response.status_code}')

    def get_vacancies(self) -> list:
        """Возвращает список вакансий на основе ответа API"""
        vacancies = []
        for i in self.response_json['items']:

            salary = {'from': i['salary']['from'],
                      'to': i['salary']['to'],
                      'currency': i['salary']['currency']
                      } if i['salary'] else {'from': None,
                                             'to': None,
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
        return vacancies


class SuperJobAPI(BaseAPI):
    """Класс для работы с API SuperJob"""
    def __init__(self, keyword: str):

        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__token = 'v3.r.137597184.113108d119212cc819e7bd5e4351adf19edb8f31'\
                       '.afada7711de6cfa115505c80d6d45294df15712d'
        self.keyword = keyword
        params = {'app_key': self.__token,
                  'page': 0,
                  'count': 100,
                  'keyword': self.keyword
                  }
        self.response = get(url=self.__url, params=params)
        self.response_json = self.response.json()
        if not self.response:
            raise HTTPError(f'Ошибка сервера. Код ответа: {self.response.status_code}')

    def get_vacancies(self) -> list:
        """Возвращает список вакансий на основе ответа API"""
        vacancies = []
        for i in self.response_json['objects']:
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
                              'requirement': f"{i['candidat'][:170]}..."
                              })
        return vacancies
