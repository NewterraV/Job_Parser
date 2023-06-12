from src.classes.api import HeadHunterAPI, SuperJobAPI
from src.classes.working_with_files import WorkingWithJSON


class MixinCheckInput:

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
        print('\n0 - Завершение программы')


class WorkWithUser(MixinCheckInput, MixinPrint):
    __slots__ = '__record'

    __platform = {'1': ['HeadHunter', HeadHunterAPI],
                  '2': ['SuperJob', SuperJobAPI]
                  }
    __volume = {
        '1': '100 вакансий на одну платформу.',
        '2': 'Максимально возможное количество.'
    }

    def __init__(self):
        self.__record = WorkingWithJSON()

    def get_user_platform(self) -> bool:
        """Функция предлагает пользователю выбрать платформу для получения вакансий,
        после получает вакансии и записывает их в JSON файл, при успешной работе возвращает True"""

        name_vacancy = input('Введите ключевое слово для поиска вакансий\n\n'
                             f'0 - Завершение программы:\n')
        if not self.check_exit(name_vacancy):
            all_vacancy = []
            while True:
                print('Введите через запятую номера платформ для загрузки вакансий (1, 2)')
                self.dict_print(self.__platform, 0)
                user_input = input()

                if not self.check_exit(user_input):

                    user_platform = user_input.split(', ')

                    if not self.check_entry(user_platform, self.__platform):
                        continue

                    while True:
                        print('Выберите количество результатов:')
                        self.dict_print(self.__volume)
                        user_volume = input()
                        if not self.check_exit(user_volume):

                            if self.check_entry(user_volume, self.__volume):
                                break
                            continue

                        return False
                    if not self.check_exit(user_volume):
                        for i in user_platform:
                            vacancies = self.__platform[i][1](name_vacancy)
                            print('Загружаю вакансии, ожидайте.')
                            if user_volume == '1':
                                all_vacancy += vacancies.get_vacancies()
                                continue
                            all_vacancy += vacancies.get_all_vacancies()

                    print(f'Успех, количество полученных вакансий: {len(all_vacancy)}')

                    self.__record.write_file(all_vacancy)
                    return True
        return False

