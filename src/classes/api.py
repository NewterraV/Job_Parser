from abc import ABC, abstractmethod
from datetime import datetime
from requests import get, HTTPError


class BaseAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        """Возвращает список вакансий на основе атрибута __response по ключевому слову"""
        pass

    @abstractmethod
    def get_all_vacancies(self):
        """Возвращает максимально возможный список вакансий из API по ключевому слову"""
        pass


class HeadHunterAPI(BaseAPI):
    """Класс для работы с API HeadHunter"""

    __slots__ = ('__url_vacancies', 'keyword', 'employer_id', '__response')

    def __init__(self, keyword=None, employer_id=None) -> None:

        self.__url_vacancies = 'https://api.hh.ru/vacancies'
        self.__url_employers = 'https://api.hh.ru/employers/'
        self.keyword = keyword
        self.employer_id = employer_id
        self.__response = None
        self.get_response()

    def get_response(self, *args) -> None:
        """Метод делает запрос к API, в качестве аргумента может принимать номер страницы для передачи в API.
                После обновляет атрибут __response полученными данными(dict)"""

        if self.employer_id is None:
            params = {'text': self.keyword,
                      'page': 0 if not args else args[0],
                      'per_page': 100,
                      'search_field': 'name'}
        else:
            params = {'employer_id': self.employer_id,
                      'page': 0 if not args else args[0],
                      'per_page': 100}
        response = get(self.__url_vacancies, params=params)

        if not response:
            raise HTTPError(f'Ошибка сервера. Код ответа: {response.status_code}')
        self.__response = response

    def get_employers(self, employers: list) -> list[dict]:
        """Метод получает информацию о работодателе"""
        data_employers = []
        for employer in employers:
            response = get(f'{self.__url_employers}{employer}').json()
            data_employers.append({'name': response['name'],
                                   'id': employer,
                                   'url': response['site_url'],
                                   'area': response['area']['name']})
        print(data_employers)
        return data_employers

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
                                  'employer_id': i['employer']['id'],
                                  "salary": salary,
                                  'area': i['area']['name'],
                                  'created': i['created_at'],
                                  'url': i['alternate_url'],
                                  'requirement': i['snippet']['requirement'] if i['snippet']['requirement']
                                  else 'Описание отсутствует'
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

    __slots__ = ('__url', 'keyword', '__response', '__token')

    def __init__(self, keyword=None, employer_id=None):

        self.__url = 'https://api.superjob.ru/2.0/vacancies/'
        self.__token = 'v3.r.137597184.113108d119212cc819e7bd5e4351adf19edb8f31' \
                       '.afada7711de6cfa115505c80d6d45294df15712d'
        self.employer_id = employer_id
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
                                  'requirement': f"{i['candidat'][:170]}..." if i['candidat']
                                  else 'Описание отсутствует'
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
