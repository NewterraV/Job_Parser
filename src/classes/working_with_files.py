from abc import ABC, abstractmethod
import json
from src.classes.vacancy import Vacancy
from src.classes.user_exception import FileIsEmpty
from os import path
from typing import Any
from pandas import DataFrame


class WorkingWithFiles(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def read_file(self, data: dict, filename: str) -> list:
        """Метод возвращает список из JSON файла по заданным параметрам."""
        pass

    @abstractmethod
    def write_file(self, data: Any, filename) -> None:
        """Метод записывает данные в файл JSON"""
        pass

    @abstractmethod
    def clear_file(self, filename: str) -> None:
        """Метод очищает ранее записанный JSON файл"""
        pass


class MixinFilter:
    """Дополнительный функционал для WorkingWithFiles"""

    def get_list_by_param(self, items: list, param: dict, reverse=False) -> list:
        """Метод принимает список вакансий, параметры для перебора. Аргумент flag меняет заполнение
         списка вакансиями подходящими под параметры на вакансии неподходящие """

        vacancy_list = []
        if not items:
            raise FileIsEmpty
        if not reverse:
            for i in items:
                if self.check_param(i, param):
                    vacancy_list.append(i)
        else:
            for i in items:
                if not self.check_param(i, param):
                    vacancy_list.append(i)
        return vacancy_list

    @staticmethod
    def check_param(data: dict, param: dict) -> bool:
        """Метод получает вакансию и список параметров. Проверяет вакансию на соответствие и возвращает значение bool"""

        status_list = []
        vacancy = Vacancy(data)
        # проверка по названию
        if param['name'] is None:
            status_list.append(True)
        else:
            status_list.append(param['name'].lower() in vacancy.name.lower())

        # проверка по диапазону зп
        if param['salary'] is None:
            status_list.append(True)
        else:
            if int(param['salary'][0]) <= vacancy.salary_from or int(param['salary'][0]) <= vacancy.salary_to:
                status_from = True
            else:
                status_from = False

            if int(param['salary'][1]) >= vacancy.salary_from and int(param['salary'][1]) >= vacancy.salary_to:
                status_to = True
            else:
                status_to = False
            status_list.append(True if status_to and status_from else False)

        # проверка по городу
        if param['area'] is None:
            status_list.append(True)
        else:
            status_list.append(param['area'].lower() in vacancy.area.lower())

        # проверка по ключевому слову
        if param['keyword'] is None:
            status_list.append(True)
        else:
            status_list.append(param['keyword'].lower() in vacancy.requirement.lower())

        if status_list == [True, True, True, True]:
            return True
        return False


class MixinFormat:

    @staticmethod
    def exel_format(data: list) -> dict:
        """Функция подготавливает данные для записи в exel"""

        vacancy = {
            "Название вакансии": [],
            "Работодатель": [],
            "Зарплата от": [],
            "Зарплата до": [],
            "В валюте": [],
            "Краткое описание": [],
            "Ссылка на вакансию": [],
            "Населенный пункт": [],
            "Вакансия создана": [],
            "Агрегатор": [],

        }
        for i in data:
            vacancy['Агрегатор'].append(i.aggregator)
            vacancy["Название вакансии"].append(i.name)
            vacancy["Работодатель"].append(i.employer)
            vacancy["Зарплата от"].append(i.salary_from)
            vacancy["Зарплата до"].append(i.salary_to)
            vacancy["В валюте"].append(i.salary_curr)
            vacancy["Населенный пункт"].append(i.area)
            vacancy["Вакансия создана"].append(i.created)
            vacancy["Ссылка на вакансию"].append(i.url)
            vacancy["Краткое описание"].append(i.requirement)

        return vacancy


class WorkingWithJSON(WorkingWithFiles, MixinFilter):
    """Класс для работы с JSON файлами"""
    __slots__ = ('__path_data_home', '__path_data')

    def __init__(self):
        self.__path_data_home = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
        self.__path_data = path.join(self.__path_data_home, 'data')

    def read_file(self, data: dict, filename='vacancy.json') -> list:

        path_file = path.join(self.__path_data, filename)
        try:
            with open(path_file, 'r', encoding='utf8') as f:
                vacancies = self.get_list_by_param(json.load(f), data)
                vacancy_list = [Vacancy(i) for i in vacancies]
                return vacancy_list
        except FileIsEmpty:
            return []

        except NotImplementedError:
            print(f'Файл с именем {filename} не найден')

    def write_file(self, data: list, filename='vacancy.json'):

        path_file = path.join(self.__path_data, filename)
        with open(path_file, 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))

    def clear_file(self, filename='vacancy.json'):

        path_file = path.join(self.__path_data, filename)
        with open(path_file, 'w', encoding='utf8') as f:
            f.write('')

    def clear_file_by_param(self, data: dict, filename='vacancy.json'):
        """Метод удаляет из файла вакансии с заданными параметрами"""

        path_file = path.join(self.__path_data, filename)
        with open(path_file, 'r', encoding='utf8') as f:
            vacancy = json.load(f)

        vacancy_new = self.get_list_by_param(vacancy, data, True)

        with open(path_file, 'w', encoding='utf8') as f:
            f.write(json.dumps(vacancy_new, indent=2, ensure_ascii=False))


class WorkingWithExel(WorkingWithFiles, MixinFilter, MixinFormat):
    __slots__ = ('__path_data_home', '__path_data')

    def __init__(self):
        self.__path_data_home = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
        self.__path_data = path.join(self.__path_data_home, 'data')

    def write_file(self, data: list, filename='vacancy.xlsx') -> None:
        path_file = path.join(self.__path_data, filename)
        dt = DataFrame(self.exel_format(data))
        dt.to_excel(path_file)

    def clear_file(self, filename: str) -> None:
        pass

    def read_file(self, data: dict, filename: str) -> list:
        pass


class WorkingWithINI(WorkingWithFiles):
    __slots__ = ('__path_data_home', '__path_data')

    def __init__(self):
        self.__path_data_home = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
        self.__path_data = path.join(self.__path_data_home, 'data')

    def write_file(self, data: Any, filename='database.ini') -> None:
        path_file = path.join(self.__path_data, filename)
        with open(path_file, 'w', encoding='utf8') as f:
            f.write(data)

    def read_file(self, data: dict, filename: str) -> list:
        pass

    def clear_file(self, filename: str) -> None:
        pass

