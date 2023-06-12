from datetime import datetime


class Vacancy:
    """Базовый класс вакансии"""

    __slots__ = ('__name', '__aggregator', '__employer', '__salary_from', '__salary_to',
                 '__salary_curr', '__area', '__created', '__url', '__requirement')

    def __init__(self, data: dict):
        self.__name = data['name']
        self.__aggregator = data['aggregator']
        self.__employer = data['employer']
        self.__salary_from = data['salary']['from'] if data['salary']['from'] else 0
        self.__salary_to = data['salary']['to'] if data['salary']['to'] else 0
        self.__salary_curr = data['salary']['currency'].upper() if data['salary']['currency'] else 'Не указано'
        self.__area = data['area'].title()
        self.__created = datetime.fromisoformat(data['created'])
        self.__url = data['url']
        self.__requirement = data['requirement']

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__name}, {self.__aggregator}, {self.__employer})'

    def __str__(self):
        return f'\nВакансия "{self.__name}" от компании "{self.__employer}".\nЗарплата от: {self.__salary_from} '\
               f'до: {self.__salary_to} в валюте: {self.__salary_curr}\nМесто расположения:'\
               f' {self.__area}, url: {self.__url}'\
               f'\nКраткое описание:\n {self.__requirement}\nДата публикации: {self.__created.strftime("%d.%m.%y")}\n'\
               f'Вакансия получена от портала: {self.__aggregator}\n'

    def __lt__(self, other):
        salary_list = self.get_max_salary(self, other)
        return salary_list[0] < salary_list[1]

    def __le__(self, other):
        salary_list = self.get_max_salary(self, other)
        return salary_list[0] <= salary_list[1]

    def __gt__(self, other):
        salary_list = self.get_max_salary(self, other)
        return salary_list[0] > salary_list[1]

    def __ge__(self, other):
        salary_list = self.get_max_salary(self, other)
        return salary_list[0] >= salary_list[1]

    @property
    def name(self):
        return self.__name

    @property
    def salary_from(self):
        return self.__salary_from

    @property
    def salary_to(self):
        return self.__salary_to

    @property
    def area(self):
        return self.__area

    @property
    def requirement(self):
        return self.__requirement

    @staticmethod
    def get_max_salary(ex_1, ex_2):
        """Статический метод возвращает верхний порог зарплаты двух полученных экземпляров класса 'Vacancy'"""
        salary_1 = ex_1.salary_to if ex_1.salary_to > ex_1.salary_from else ex_1.salary_from
        salary_2 = ex_2.salary_to if ex_2.salary_to > ex_2.salary_from else ex_2.salary_from

        return salary_1, salary_2
