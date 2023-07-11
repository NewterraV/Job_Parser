import PySimpleGUI as sg
from typing import Any
from src.classes.user_exception import CheckExit


class GUI:
    """Класс с методами графической оболочки"""

    def __init__(self):
        sg.theme('DarkTeal6')

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
    def create_buttons(data: dict[str, list[dict[Any]]], check_exit=True):
        """Метод на основе словаря создает окно с кнопками"""
        layout = [[sg.Text(data['name'])]]
        for i in data['buttons']:
            layout.append([sg.Button(f'{i["title"]}', size=40, key=i['key'], enable_events=True)])
        if check_exit:
            layout.append([sg.Cancel('Exit')])

        window = sg.Window('Создание DataBase Config', layout)
        event, values = window.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Exit'):
                window.close()
                raise CheckExit
            window.close()
            return event

    def create_input_field(self, data: dict[str, list[dict[Any]]], check_exit=True) -> list[str]:
        """Метод создает поле для ввода на основе словаря с параметрами"""

        layout = [[sg.Text(data['name'])]]
        for i in data['line']:
            layout.append([sg.Text(i['title'], size=40),
                           sg.InputText()])
        if check_exit:
            layout.append([sg.Cancel('Exit')])
        window = sg.Window('Создание DataBase Config', layout)
        event, values = window.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Exit'):
                window.close()
                raise CheckExit
            elif len(values) == 0:
                self.print_message('Необходимо ввести минимум одно значение', title='Error', color='lightpink')
                continue
            return values
