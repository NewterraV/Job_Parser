from abc import ABC, abstractmethod
import json
from src.classes.vacancy import Vacancy
from src.classes.user_exception import FileIsEmpty
from os import path


class WorkingWithFiles(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def read_file(self, data: dict, filename: str) -> list:
        """Метод возвращает список из JSON файла по заданным параметрам."""
        pass

    @abstractmethod
    def write_file(self, data: list, filename) -> None:
        """Метод записывает данные в файл JSON"""
        pass

    @abstractmethod
    def clear_file(self, filename: str) -> None:
        """Метод очищает ранее записанный JSON файл"""
        pass


class MixinFilter:
    """Дополнительный функционал для WorkingWithFiles"""

    def get_list_by_param(self, items: list, param: dict, flag=True) -> list:
        """Метод принимает список вакансий, параметры для перебора. Аргумент flag меняет заполнение
         списка вакансиями подходящими под параметры на вакансии неподходящие """
        vacancy_list = []
        if not items:
            raise FileIsEmpty
        if flag:
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
            if param['salary'][0] <= vacancy.salary_from or param['salary'][0] <= vacancy.salary_to:
                status_from = True
            else:
                status_from = False

            if param['salary'][1] >= vacancy.salary_from and param['salary'][1] >= vacancy.salary_to:
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


class WorkingWithJSON(WorkingWithFiles, MixinFilter):
    """Класс для работы с JSON файлами"""

    def __init__(self):
        self.__path_data_home = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
        self.__path_data = path.join(self.__path_data_home, 'data')

    def read_file(self, data: dict, filename='vacancy.json') -> list:
        path_file = path.join(self.__path_data, filename)
        try:
            with open(path_file, 'r', encoding='utf8') as f:
                vacancy = self.get_list_by_param(json.load(f), data)
                return vacancy
        except FileIsEmpty:
            print(FileIsEmpty)

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

    def del_file_by_param(self, data: dict, filename='vacancy.json'):
        """Метод удаляет из файла вакансии с заданными параметрами"""
        path_file = path.join(self.__path_data, filename)
        with open(path_file, 'r', encoding='utf8') as f:
            vacancy = json.load(f)

        vacancy_new = self.get_list_by_param(vacancy, data, False)

        with open(path_file, 'w', encoding='utf8') as f:
            f.write(json.dumps(vacancy_new, indent=2, ensure_ascii=False))
