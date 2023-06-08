from datetime import datetime
import json


class Vacancy:
    """Базовый класс вакансии"""

    all_vacancy = []

    def __init__(self, data: dict):
        self.name = data['name']
        self.__aggregator = data['aggregator']
        self.employer = data['employer']
        self.salary_from = data['salary']['from'] if data['salary']['from'] else 0
        self.salary_to = data['salary']['to'] if data['salary']['to'] else 0
        self.salary_curr = data['salary']['currency'].upper() if data['salary']['currency'] else 'Не указано'
        self.area = data['area'].title()
        self.created = datetime.fromisoformat(data['created'])
        self.url = data['url']
        self.requirement = data['requirement']

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name}, {self.__aggregator}, {self.employer})'

    def __str__(self):
        return f'\nВакансия "{self.name}" от компании "{self.employer}".\nЗарплата от: {self.salary_from} '\
               f'до: {self.salary_to} в валюте: {self.salary_curr}\nМесто расположения: {self.area}, url: {self.url}'\
               f'\nКраткое описание:\n {self.requirement}\nДата публикации: {self.created.strftime("%d.%m.%y")}\n'\
               f'Вакансия получена от портала: {self.__aggregator}\n'

    @staticmethod
    def get_max_salary(ex_1, ex_2):
        """Статический метод возвращает верхний порог зарплаты двух полученных экземпляров класса 'Vacancy'"""
        salary_1 = ex_1.salary_to if ex_1.salary_to > ex_1.salary_from else ex_1.salary_from
        salary_2 = ex_2.salary_to if ex_2.salary_to > ex_2.salary_from else ex_2.salary_from

        return salary_1, salary_2

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
