from abc import ABC, abstractmethod
from datetime import datetime
from requests import get, HTTPError
import PySimpleGUI as sg
from src.classes.GUI import GUI


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

    def get_data_employers(self, employers: list) -> list[dict]:
        """Метод получает информацию о работодателях"""
        data_employers = []
        layout = GUI.get_progress_bar('Загружаю данные о работодателях', len(employers))

        window = sg.Window('Загрузка', layout=layout)

        for i, employer in enumerate(employers):
            response = get(f'{self.__url_employers}{employer}').json()
            data_employers.append({'name': response['name'],
                                   'id': employer,
                                   'url': response['site_url'],
                                   'area': response['area']['name']}
                                  )
            window.read(timeout=0)
            window['item'].Update(value=f'{response["name"]}')
            window['progress'].update_bar(i + 1)

        window.close()
        return data_employers

    def get_employer_vacancies(self, employers: list) -> list[dict]:
        """Метод получает информацию о вакансиях по работодателю"""

        vacancy_employers = []
        layout = GUI.get_progress_bar('Получаю данные по вакансиям работодателей:', len(employers))

        window = sg.Window('Загрузка', layout=layout)

        # запрашиваем вакансии по каждому работодателю отдельно для получения
        # максимального количества результатов
        for i, employer in enumerate(employers):
            window.read(timeout=0)
            window['item'].Update(value=f'{i} из {len(employers)}')
            window['progress'].update_bar(i + 1)
            self.employer_id = employer
            all_vacancy = self.get_all_vacancies()
            vacancy_employers.extend(all_vacancy)

        window.close()

        return vacancy_employers

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
                vacancies.append({'name': i["name"],
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

        layout = GUI.get_progress_bar(f'Получаю данные по вакансиям работодателя id: {self.employer_id}', 20)

        window = sg.Window('Загрузка', layout=layout)

        for i in (range(20)):
            self.get_response(i)
            # фильтрация бесполезных обращений к API для уменьшения времени выполнения
            if not self.__response.json()['items']:
                break
            all_vacancies.extend(self.get_vacancies())
            window.read(timeout=0)
            window['item'].Update(value=f'Страница {i} из {20}')
            window['progress'].update_bar(i + 1)
        window.close()
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
                vacancies.append({'name': i["profession"],
                                  'employer': i['firm_name'],
                                  'employer_id': i['firm_id'],
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
        print('\033[32mПолучаю данные по вакансиям SuperJob\033[0m')

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
