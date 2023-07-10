from requests import HTTPError, ConnectionError
from easygui import passwordbox
from src.classes.working_with_files import WorkingWithINI


def get_user_vacancies(user_platform, keyword=None, all_result=False) -> [list, False]:
    """Функция на основе списка платформ выдает список словарей вакансий. По флагу all_result определяет
    количество возвращаемых результатов. В случае ошибок со стороны сервера вернет False"""

    all_vacancy = []
    while True:
        try:
            for i in user_platform:
                vacancies = i(keyword=keyword)
                if all_result:
                    all_vacancy += vacancies.get_all_vacancies()
                    continue
                all_vacancy += vacancies.get_vacancies()
            return all_vacancy

        except (HTTPError, ConnectionError):

            print('Неполадки с подключением к серверу:\n'
                  'любое значение - попробовать снова\n'
                  '0 - Завершение программы\n')
            user_input = input()

            if user_input != '0':
                continue
            return False


def create_config_database() -> None:
    """Функция создает конфиг для работы с базой данных"""

    record = WorkingWithINI()
    host = input('Введите значение host:\n(Enter - \033[34mlocalhost\033[0m)\n0 - завершение программы\n')

    user = input('Введите имя пользователя:\n(Enter - \033[34mpostgres\033[0m)\n0 - завершение программы\n')
    while True:
        print('Введите пароль в \033[33mотдельно появившемся окне\033[0m')
        password = passwordbox('Пароль для доступа к базе данных:\n0 - завершение программы')
        if password:
            break
        print('\033[31mError: пароль не может быть пустым\033[0m')
    port = input('Введите номер порта:\n(Enter - \033[34m5432\033[0m)\n0 - завершение программы\n')
    param = f'[postgresql]\n' \
            f'host={host if host else "localhost"}\n' \
            f'user={user if user else "postgres"}\n' \
            f'password={password}\n' \
            f'port={port if port else 5432}\n'
    record.write_file(param)
    print('\033[32mDataBase Config успешно сгенерирован\033[0m')


def check_config():
    record = WorkingWithINI()
    if not record.check_config():
        print(('\033[31mВНИМАНИЕ: отсутствует файл конфигурации для доступа к базе данных.'
               '\nСгенерируйте конфигурационный файл\033[0m'))
        create_config_database()


def get_volume(self) -> [bool, str]:
    """Запрашивает у пользователя количество результатов для запроса по API"""
    while True:
        print('\nВыберите количество результатов:')
        self.dict_print(self.__volume)
        user_volume = input()
        self.check_exit(user_volume)
        if self.check_entry(user_volume, self.__volume):
            return user_volume
