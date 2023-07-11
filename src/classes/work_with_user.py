from prettytable import PrettyTable

from src.classes.DBmanger import DBmanager
from src.classes.api import HeadHunterAPI, SuperJobAPI
from src.classes.employer import Employer
from src.classes.user_exception import CheckExit
from src.classes.working_with_files import WorkingWithJSON, WorkingWithExel
from src.classes.vacancy import Vacancy
from src.classes.GUI import GUI
from src.utils import get_user_vacancies


class MixinCheckInput:
    """Класс с методами проверки ввода"""

    @staticmethod
    def check_exit(value: [str, int]) -> bool:
        """Проверяет ввод пользователя на флаг выхода из программы"""
        if str(value) == '0':
            raise CheckExit
        return False

    @staticmethod
    def check_entry(value: [str, int], dict_: dict) -> bool:
        """Проверяет ввод пользователя на вхождение в диапазон предлагаемых функций"""
        flag = True
        if type(value) is list:
            for i in value:
                if i not in dict_.keys():
                    flag = False
        else:
            if value not in dict_.keys():
                flag = False

        if flag is False:
            print('\033[31mНеверный ввод, попробуйте еще раз.\033[0m')
            return flag
        return flag


class MixinPrint:
    """Класс с методами вывода информации"""

    @staticmethod
    def dict_print(dict_: dict, *args: [int, str]) -> None:
        """Функция печатает словари. При получении дополнительного аргумента, использует его
        как индекс для печати значения словаря"""

        if args:
            for key, values in dict_.items():
                print(f'{key} - {values[int(args[0])]}')
        else:
            for key, values in dict_.items():
                print(f'{key} - {values}')
        print('0 - Завершение программы')

    @staticmethod
    def print_vacancy(list_: list):
        """Функция выводит информацию о вакансиях на экран"""
        for i in list_:
            vacancy = Vacancy(i)
            print(vacancy)

    @staticmethod
    def print_table(data: list) -> None:
        """Метод выводит на экран данные в виде таблицы"""
        table = PrettyTable()
        table.align = 'l'
        table_titles = ['№']
        for i in data[0].keys():
            table_titles.append(i.title())
        table.field_names = table_titles
        count = 1
        for i in data:
            values = [count]
            for item in i.values():
                values.append(item)
            table.add_row(values)
            count += 1
        print(table)


class WorkWithUserBase(MixinCheckInput, MixinPrint):
    """Базовый класс для работы с пользователем"""

    # Данные для выбора типа поиска
    __type_selection = {'name': 'Выберите функцию:',
                        'buttons': [{'title': 'По ключевому слову', 'key': '1'},
                                    {'title': 'По работодателю', 'key': '2'}]}

    # Данные для выбора основной функции
    __main_function = {'name': 'Выберите функцию:',
                       'buttons': [{'title': 'Поиск вакансий', 'key': '1'},
                                   {'title': 'Сгенерировать DataBase Config', 'key': '2'}]}

    # Данные для выбора количества вакансий при поиске
    __volume = {
        '1': '100 вакансий на одну платформу.',
        '2': 'Максимально возможное количество.'
    }

    # Данные для выбора агрегатора
    __aggregator = {'1': ['HeadHunter', HeadHunterAPI],
                    '2': ['SuperJob', SuperJobAPI]
                    }

    def __init__(self):
        self.__record = WorkingWithJSON()
        self.__file_exel = WorkingWithExel()
        self.__db_manager = DBmanager()
        self.__api = HeadHunterAPI()
        self.__gui = GUI()

    @property
    def volume(self):
        return self.__volume

    def get_keyword(self):
        """Метод запрашивает у пользователя ключевое слово"""
        name_vacancy = input('\nВведите ключевое слово для поиска вакансий\n'
                             f'0 - Завершение программы:\n')

        self.check_exit(name_vacancy)
        return name_vacancy.lower()

    def search_type_selection(self) -> str:
        """Функция запрашивает у пользователя тип поиска вакансий"""
        return self.__gui.create_buttons(self.__type_selection)

    def starting_program(self) -> str:
        """Метод выводит окно с выбором функции, возвращает текстовое значение выбранное пользователем"""
        return self.__gui.create_buttons(self.__main_function)

    def get_repeat(self):
        """Запрашивает повтор поиска вакансий"""

        data = {'name': 'Выполнить новый поиск?',
                'buttons': [{'title': 'Да', 'key': True},
                            {'title': 'Нет', 'key': False}]}
        return self.__gui.create_buttons(data, check_exit=False)

    def get_aggregator(self) -> list:
        """Метод запрашивает список агрегаторов для поиска у пользователя"""

        while True:
            # Запрашиваем агрегаторов
            print('\nВведите через запятую номера платформ для загрузки вакансий (1, 2)')
            self.dict_print(self.__aggregator, 0)
            user_input = input()

            self.check_exit(user_input)
            # Проверяем ввод на валидность
            if not self.check_entry(user_input.split(', '), self.__aggregator):
                continue
            # создаем список платформ выбранных пользователем
            user_aggregator = [self.__aggregator[i][1] for i in user_input.split(', ')]
            return user_aggregator

    def get_repeat_analyses(self) -> [bool, None]:
        data = {'name': 'Вернуться к анализу вакансий?:',
                'buttons': [{'title': 'Да', 'key': True},
                            {'title': 'Нет', 'key': False}]}
        return self.__gui.create_buttons(data, check_exit=False)

    def get_drop_db(self) -> bool:
        """Метод выдает запрос на удаление базы данных"""
        data = {'name': 'Удалить созданную базу данных перед выходом?:',
                'buttons': [{'title': 'Да', 'key': True},
                            {'title': 'Нет', 'key': False}]}

        return self.__gui.create_buttons(data, check_exit=False)


class WorkWithUserKeyWord(WorkWithUserBase):
    """Класс с набором методов для работы с пользователем при поиске вакансий по ключевому слову"""

    __function_all = {'1': 'Получить список вакансий с использованием фильтров',
                      '2': 'Получить топ 5 вакансий по зарплате',
                      '3': 'Записать все вакансии в файл Excel',
                      '4': 'Удалить вакансии'}

    __data_filter = {'name': None,
                     'salary': None,
                     'area': None,
                     'keyword': None}

    __output = {'1': 'Вывести все вакансии на экран',
                '3': 'Вывести топ 5 вакансий по зарплате на экран',
                '4': 'Записать в файл Excel',
                '5': 'Вернуться к функциям'
                }

    def __init__(self):
        super().__init__()
        self.__record = WorkingWithJSON()
        self.__file_exel = WorkingWithExel()
        self.__db_manager = DBmanager()
        self.__api = HeadHunterAPI()
        self.__employer = Employer()

    def keyword_search(self) -> None:
        """Основная логика работы с вакансиями по ключевому слову"""

        name_vacancy = self.get_keyword()
        user_platform = [HeadHunterAPI]  # self.get_aggregator()  -- раскомментировать после разработки
        # возможности получения данных о работодателе от super.job

        user_volume = '1'  # self.get_volume()  -- раскомментировать после разработки
        # возможности получения большого кол-ва вакансий

        # выполняем загрузку списка вакансий
        all_vacancy = get_user_vacancies(user_platform, keyword=name_vacancy,
                                         all_result=True if user_volume != '1' else False)

        if not all_vacancy:
            print('\033[31mК сожалению по вашему запросу нет вакансий\033[0m')
            raise CheckExit

        print(f'\033[32mУспех, количество полученных вакансий: {len(all_vacancy)}\033[m')

        # Получаем список уникальных id работодателей из списка вакансий
        employer_ids = self.__employer.get_list_employer(all_vacancy)
        employer_data = self.__api.get_data_employers(employer_ids)

        print('\033[32mЗаполняю базу данных\033[0m')
        self.__db_manager.save_data_to_employer(employer_data)
        self.__db_manager.save_data_to_vacancies(all_vacancy)

    @property
    def record(self):
        """Возвращает self.__record"""
        return self.__record

    @staticmethod
    def get_salary_range() -> list:
        """Запрашивает у пользователя диапазон зарплат"""

        while True:
            salary = input('\nВведите диапазон зарплаты от '
                           'и до через тире (формат: 0-1000)\n').split('-')

            if len(salary) == 2 and salary[0].isdigit() and \
                    salary[1].isdigit():
                break
            print('Неверный ввод, попробуйте снова')
        return salary


class WorkWithUserEmployer(WorkWithUserBase):
    """Класс для работы с пользователем при поиске вакансий по работодателю"""

    def __init__(self):
        super().__init__()
        self.__record = WorkingWithJSON()
        self.__file_exel = WorkingWithExel()
        self.__db_manager = DBmanager()
        self.__api = HeadHunterAPI()

    def search_by_employer(self) -> None:
        """Основная логика работы с вакансиями по работодателю"""

        # Получение списка работодателей
        user_employers = self.get_user_employers()

        # Запрос вакансий по API
        employers_data = self.__api.get_data_employers(user_employers)
        employers_vacancy = self.__api.get_employer_vacancies(user_employers)

        # Сохранение работодателей в БД
        print('\033[32mЗаполняю базу данных\033[0m')
        self.__db_manager.save_data_to_employer(employers_data)
        self.__db_manager.save_data_to_vacancies(employers_vacancy)

    def get_user_employers(self) -> list:
        """Метод запрашивает у пользователя список id работодателей HH"""

        user_input = input('Введите через запятую id работодателей для запроса '
                           '\033[34m(формат: 1235795, 79987456, 7854458)\033[0m\n'
                           'Оставьте строку пустой для загрузки вакансий работодателей по умолчанию\n'
                           '0 - завершение программы\n')
        # Проверяем на выход
        self.check_exit(user_input)
        # Создаем список работодателей
        if user_input:
            return user_input.split(', ')
        # Возврат списка по умолчанию
        return [1740, 78638, 3529, 4872, 1060266, 115, 2180, 26624, 35065]


class WorkWithUserFilters(WorkWithUserBase):
    """Класс для работы с пользователем при анализе полученных вакансий"""

    __filters_name = {'1': 'Вывести на экран список работодателей и количество вакансий у них;',
                      '2': 'Вывести на экран список всех вакансий;',
                      '3': 'Получить среднюю зарплату по всем вакансиям',
                      '4': 'Получить вакансии с зарплатой выше среднего',
                      '5': 'Поиск вакансий по ключевому слову в названии'}

    __output = {'1': 'Вывести все вакансии на экран',
                '2': 'Вывести все вакансии на экран в виде таблицы',
                '3': 'Записать в файл Excel',
                '4': 'Вернуться к функциям'
                }

    def __init__(self):
        super().__init__()
        self.__db_manager = DBmanager()
        self.__file_exel = WorkingWithExel()
        self.__filters = {'1': self.get_companies_and_vacancies_count,
                          '2': self.get_all_vacancies,
                          '3': self.get_avg_salary,
                          '4': self.get_vacancies_with_higher_salary,
                          '5': self.get_vacancies_with_keyword}

    def job_analysis(self):
        """Метод на основе ответов пользователя возвращает необходимые данные о вакансиях"""
        while True:
            print('\n\033[33mАнализ полученных вакансий.\n\033[0mВыберите действие:\n')
            self.dict_print(self.__filters_name)
            user_input = input()
            self.check_exit(user_input)
            if not self.check_entry(user_input, self.__filters_name):
                continue
            status = self.__filters[user_input]()
            if status:
                continue
            self.get_repeat_analyses()
            continue

    def get_companies_and_vacancies_count(self) -> [None, bool]:
        """Метод выводит на экран таблицу с компаниями и средней зарплатой по ним"""
        data = self.__db_manager.get_companies_and_vacancies_count()
        self.print_table(data)
        return True

    def get_all_vacancies(self) -> [bool, None]:
        data = self.__db_manager.get_all_vacancies()
        self.print_table(data)
        return True

    def get_avg_salary(self) -> bool:
        data = self.__db_manager.get_avg_salary()
        print(f'Средняя зарплата по всем вакансиям: \033[34m{data}\033[0m\n')
        return True

    def get_vacancies_with_higher_salary(self):
        data = self.__db_manager.get_vacancies_with_higher_salary()
        print(f'Найдено результатов: \033[34m{len(data)}\033[0m')
        if self.output_result(data):
            return True
        return

    def get_vacancies_with_keyword(self):

        data = self.__db_manager.get_vacancies_with_keyword(self.get_keyword())
        print(f'Найдено результатов: \033[34m{len(data)}\033[0m')
        if self.output_result(data):
            return True
        return

    def output_result(self, data: list) -> bool:
        while True:
            print('\n\033[33mЧто сделать с полученным результатом?\033[0m')
            self.dict_print(self.__output)
            user_input = input()
            self.check_exit(user_input)
            if not self.check_entry(user_input, self.__output):
                continue

            if user_input == '1':
                self.print_vacancy(data)
            elif user_input == '2':
                self.print_table(data)
            elif user_input == '3':
                filename = input("Введите название файла:\n")
                self.__file_exel.write_file(data, filename=filename)
            elif user_input == '4':
                return True
            continue
