import PySimpleGUI as sg
from src.classes.user_exception import CheckExit


class GUI:
    """Класс с методами графической оболочки"""

    @staticmethod
    def print_message(text, title='Сообщение', color=None):
        """Метод выводит окно с сообщением"""

        layout = [[sg.Text(text, text_color=color)],
                  [sg.OK()]]

        window = sg.Window(title, layout)
        while True:
            event, values = window.read()
            if event in (sg.WIN_CLOSED, 'OK'):
                break
        window.close()

    @ staticmethod
    def create_buttons(buttons: list[dict]):
        """Метод на основе словаря создает окно с кнопками"""
        layout = [[sg.Text('Выберите функцию:')]]
        for i in buttons:
            layout.append([sg.Button(f'{i["title"]}', size=40, key=i['key'], enable_events=True)])
        layout.append([sg.Cancel('Exit')])

        window = sg.Window('Создание DataBase Config', layout)
        event, values = window.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Exit'):
                window.close()
                raise CheckExit
            window.close()
            return event
