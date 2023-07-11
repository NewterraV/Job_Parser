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
    __volume = {'1': '100 вакансий на одну платформу.',
                '2': 'Максимально возможное количество.'}

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
        data = {'name': 'Введите ключевое слово для поиска вакансий:',
                'line': ['Ключевое слово']}
        response = self.__gui.create_input_field(data)
        name_vacancy = response[0]

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

    def __init__(self):
        super().__init__()
        self.__record = WorkingWithJSON()
        self.__file_exel = WorkingWithExel()
        self.__db_manager = DBmanager()
        self.__api = HeadHunterAPI()
        self.__employer = Employer()
        self.__gui = GUI()

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
            self.__gui.print_message('К сожалению по вашему запросу нет вакансий', title='Error', color='lightpink')
            raise CheckExit

        # Получаем список уникальных id работодателей из списка вакансий
        employer_ids = self.__employer.get_list_employer(all_vacancy)
        employer_data = self.__api.get_data_employers(employer_ids)

        self.__db_manager.save_data_to_employer(employer_data)
        self.__db_manager.save_data_to_vacancies(all_vacancy)
        GUI.print_message(f'Успех, получено вакансий: {len(all_vacancy)}')

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
        self.__gui = GUI()

    def search_by_employer(self) -> None:
        """Основная логика работы с вакансиями по работодателю"""

        # Получение списка работодателей
        user_employers = self.get_user_employers()

        # Запрос вакансий по API
        employers_data = self.__api.get_data_employers(user_employers)
        employers_vacancy = self.__api.get_employer_vacancies(user_employers)

        # Сохранение работодателей в БД
        self.__db_manager.save_data_to_employer(employers_data)
        self.__db_manager.save_data_to_vacancies(employers_vacancy)

    def get_user_employers(self) -> list:
        """Метод запрашивает у пользователя список id работодателей HH"""
        data = {'name': 'Введите id работодателей для запроса:\n'
                        'Оставьте строки пустыми для загрузки вакансий работодателей по умолчанию\n',
                'line': ['Работодатель ' + str(i) for i in range(1, 11)]}
        response = self.__gui.create_input_field(data)
        user_employers = [value for value in response.values() if value]

        if len(user_employers):
            return user_employers
        return [1740, 78638, 3529, 4872, 1060266, 115, 2180, 26624, 35065]


class WorkWithUserFilters(WorkWithUserBase):
    """Класс для работы с пользователем при анализе полученных вакансий"""

    __filters_name = {'name': 'Анализ полученных вакансий.\nВыберите действие:',
                      'buttons': [{'title': 'Вывести количество вакансий по работодателю', 'key': '1'},
                                  {'title': 'Вывести список всех вакансий', 'key': '2'},
                                  {'title': 'Вывести среднюю зарплату по всем вакансиям', 'key': '3'},
                                  {'title': 'Получить вакансии с зарплатой выше среднего', 'key': '4'},
                                  {'title': 'Поиск вакансий по ключевому слову в названии', 'key': '5'}]}

    __output = {'name': 'Что сделать с полученным результатом?:',
                'buttons': [{'title': 'Вывести все вакансии на экран', 'key': '1'},
                            {'title': 'Вывести все вакансии на экран в виде таблицы', 'key': '2'},
                            {'title': 'Записать в файл Excel', 'key': '3'},
                            {'title': 'Вернуться к функциям', 'key': '4'}]}

    def __init__(self):
        super().__init__()
        self.__db_manager = DBmanager()
        self.__file_exel = WorkingWithExel()
        self.__gui = GUI()
        self.__filters = {'1': self.get_companies_and_vacancies_count,
                          '2': self.get_all_vacancies,
                          '3': self.get_avg_salary,
                          '4': self.get_vacancies_with_higher_salary,
                          '5': self.get_vacancies_with_keyword}

    def job_analysis(self):
        """Метод на основе ответов пользователя возвращает необходимые данные о вакансиях"""
        while True:
            user_input = self.__gui.create_buttons(self.__filters_name)

            status = self.__filters[user_input]()
            if status:
                continue
            self.get_repeat_analyses()
            continue

    def get_companies_and_vacancies_count(self) -> [None, bool]:
        """Метод выводит на экран таблицу с компаниями и средней зарплатой по ним"""
        data = self.__db_manager.get_companies_and_vacancies_count()
        if self.__gui.create_table(data):
            return True

    def get_all_vacancies(self) -> [bool, None]:
        data = self.__db_manager.get_all_vacancies()
        self.__gui.create_table(data)
        return True

    def get_avg_salary(self) -> bool:
        data = self.__db_manager.get_avg_salary()
        self.__gui.print_message(f'Средняя зарплата по всем вакансиям: {data}')

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
            user_input = self.__gui.create_buttons(self.__output)

            if user_input == '1':
                self.print_vacancy(data)
            elif user_input == '2':
                self.__gui.create_table(data)
            elif user_input == '3':

                filename = input("Введите название файла:\n")
                self.__file_exel.write_file(data, filename=filename)
            elif user_input == '4':
                return True
            continue
