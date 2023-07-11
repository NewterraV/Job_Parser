from requests import HTTPError, ConnectionError
from src.classes.working_with_files import WorkingWithINI
from src.classes.user_exception import CheckExit
from src.classes.GUI import GUI
import PySimpleGUI as sg


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

    sg.theme('DarkTeal6')
    layout = [[sg.Text('Введите необходимые данные в форму:')],
              [sg.Text('Host:', size=15),
               sg.InputText(key='host', default_text='localhost')],
              [sg.Text('Имя пользователя:', size=15),
               sg.InputText(key='user_name', default_text='postgres')],
              [sg.Text('Пароль:', size=15), sg.InputText(key='password', password_char='*', do_not_clear=True)],
              [sg.Text('Номер порта:', size=15), sg.InputText(key='port', default_text='5432')],
              [sg.OK(), sg.Cancel('Exit')]]

    window = sg.Window('Создание DataBase Config', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            raise CheckExit
        if not values['password']:
            GUI.print_message('поле "Пароль" не может быть пустым', title='Error', color='lightpink')
            continue
        if event in (sg.WIN_CLOSED, 'OK'):
            param = f'[postgresql]\n' \
                    f'host={values["host"] if values["host"] else "localhost"}\n' \
                    f'user={values["user_name"] if values["user_name"] else "postgres"}\n' \
                    f'password={values["password"]}\n' \
                    f'port={values["port"] if values["port"] else 5432}\n'
            record.write_file(param)
        break
    window.close()

    GUI.print_message('DataBase Config успешно сгенерирован', color='orange')


def check_config():
    record = WorkingWithINI()
    if not record.check_config():
        GUI.print_message('ВНИМАНИЕ: отсутствует файл конфигурации для доступа к базе данных.'
                          '\nСгенерируйте конфигурационный файл', title='Error', color='lightpink')
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
