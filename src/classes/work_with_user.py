from src.classes.api import HeadHunterAPI, SuperJobAPI
from src.classes.working_with_files import WorkingWithJSON, WorkingWithExel
from src.Utils import get_user_vacancies, get_top_vacancies


class MixinCheckInput:
    """Класс с методами проверки ввода"""

    @staticmethod
    def check_exit(value: str) -> bool:
        """Проверяет ввод пользователя на флаг выхода из программы"""
        if str(value) == '0':
            return True
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
            print('Неверный ввод, попробуйте еще раз.')
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
            print(i)


class WorkWithUser(MixinCheckInput, MixinPrint):
    """Класс с набором методов для работы с пользователем"""

    __platform = {'1': ['HeadHunter', HeadHunterAPI],
                  '2': ['SuperJob', SuperJobAPI]
                  }
    __volume = {
        '1': '100 вакансий на одну платформу.',
        '2': 'Максимально возможное количество.'
    }
    __function_all = {'1': 'Получить список вакансий с использованием фильтров',
                      '2': 'Получить топ 5 вакансий по зарплате',
                      '3': 'Записать все вакансии в файл Excel',
                      '4': 'Удалить вакансии'}

    __data_filter = {'name': None,
                     'salary': None,
                     'area': None,
                     'keyword': None}

    __filters = {'1': 'Название вакансии',
                 '2': 'Диапазон зарплаты',
                 '3': 'Населенный пункт',
                 '4': 'Ключевое слово для поиска по всей информации о вакансии',
                 '5': 'без фильтров'
                 }

    __output = {'1': 'Вывести все вакансии на экран',
                '2': 'Вывести топ 5 вакансий по зарплате на экран',
                '3': 'Записать в файл Excel',
                '4': 'Вернуться к функциям'
                }

    def __init__(self):
        self.__record = WorkingWithJSON()
        self.__file_exel = WorkingWithExel()

    @property
    def record(self):
        """Возвращает self.__record"""
        return self.__record

    def get_vacancy_in_user_platform(self) -> bool:
        """Функция предлагает пользователю выбрать платформу для получения вакансий,
        после получает вакансии и записывает их в JSON файл, при успешной работе возвращает True"""

        name_vacancy = input('\nВведите ключевое слово для поиска вакансий\n'
                             f'0 - Завершение программы:\n')

        if not self.check_exit(name_vacancy):

            while True:
                print('\nВведите через запятую номера платформ для загрузки вакансий (1, 2)')
                self.dict_print(self.__platform, 0)
                user_input = input()

                if self.check_exit(user_input):
                    break

                if not self.check_entry(user_input.split(', '), self.__platform):
                    continue
                else:
                    # создаем список платформ выбранных пользователем
                    user_platform = [self.__platform[i][1] for i in user_input.split(', ')]

                    while True:
                        print('\nВыберите количество результатов:')
                        self.dict_print(self.__volume)
                        user_volume = input()
                        if not self.check_exit(user_volume):

                            if self.check_entry(user_volume, self.__volume):
                                break
                            continue
                        return False

                    # выполняем загрузку списка вакансий
                    if not self.check_exit(user_volume):
                        print('Загружаю вакансии, ожидайте.')
                        while True:
                            all_vacancy = get_user_vacancies(name_vacancy, user_platform,
                                                             True if user_volume != '1' else False)
                            break

                        if all_vacancy:
                            print(f'Успех, количество полученных вакансий: {len(all_vacancy)}')
                            self.__record.write_file(all_vacancy)
                            return True
                    break
        return False

    def get_function(self):
        """Функция для работы пользователя с вакансиями"""
        while True:
            print('\nВыберите функцию:')
            self.dict_print(self.__function_all)
            user_input = input()
            try:
                if not self.check_exit(user_input):
                    if self.check_entry(user_input, self.__function_all):

                        # Получаем вакансии по параметрам
                        if user_input == '1':
                            return self.get_vacancy_by_param()

                        # Возвращаем топ 5 вакансий
                        if user_input == '2':
                            vacancies = self.__record.read_file(self.__data_filter)
                            if vacancies:
                                return get_top_vacancies(vacancies)
                            return vacancies

                        # Возвращаем все вакансии в exel
                        if user_input == '3':
                            self.__file_exel.write_file(self.__record.read_file(self.__data_filter))
                            return True

                        # Выполняем пользовательскую очистку
                        if user_input == '4':
                            return self.clear()
                return False
            except PermissionError:
                print('Запись не удалась, закройте файл и повторите снова.')
                continue

    def get_vacancies(self) -> [list, bool]:
        """Получает список вакансий по заданным параметрам из файла"""

        data_filter = self.get_filter()
        if data_filter:
            return self.__record.read_file(data_filter)
        return False

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

    def get_filter(self) -> [dict, bool]:
        """Возвращает словарь для функции фильтрации на основе ответов пользователя"""
        data_filter = {}
        while True:
            print('\nВведите через запятую номера необходимых фильтров (формат: 1, 2, 4):')
            self.dict_print(self.__filters)
            user_input = input()

            if self.check_exit(user_input):
                return False
            user_function = user_input.split(', ')
            if not self.check_entry(user_function, self.__filters):
                continue
            break

        data_filter['name'] = input('\nВведите ключевое слово для поиска в названии вакансии:\n') \
            if '1' in user_function else None

        data_filter['salary'] = self.get_salary_range() if '2' in user_function else None

        data_filter['area'] = input('\nВведите название населенного пункта:\n') if '3' in user_function else None

        data_filter['keyword'] = input('\nВведите ключевое слово для поиска по всей вакансии:\n') \
            if '4' in user_function else None
        return data_filter

    def get_repeat(self):
        """Запрашивает повтор поиска вакансий"""
        print('\nВыполнить новый поиск?\n1 - Да\n0 - завершить программу\n')
        user_input = input()
        return not self.check_exit(user_input)

    def clear(self):
        """Выполняет пользовательскую очистку"""
        while True:
            user_filter = input('\nВыберите:\n1 - удалить с фильтрацией\n2 - полная очистка\n'
                                '0 - завершение программы\n')
            if not self.check_exit(user_filter):
                if user_filter == '1':
                    data_filter = self.get_filter()
                    self.__record.clear_file_by_param(data_filter)
                    print('Очистка по выбранным фильтрам завершена')
                    return True

                if user_filter == '2':
                    self.__record.clear_file()
                    print('Очистка завершена')
                    return
            return False

    def get_vacancy_by_param(self):
        """Функция подбирает вакансии по параметрам и выводит их пользователю в выбранном формате"""
        vacancies = self.get_vacancies()
        print(f'Найдено вакансий: {len(vacancies)}')

        while True:
            print('\nВыберите действие:')
            self.dict_print(self.__output)
            user_input = input()
            if not self.check_exit(user_input):
                if self.check_entry(user_input, self.__output):
                    if user_input == '1':
                        return vacancies
                    elif user_input == '3':
                        self.__file_exel.write_file(vacancies)
                        continue
                    elif user_input == '4':
                        return True
                    return get_top_vacancies(vacancies)
            else:
                return False
