import PySimpleGUI as sg
from typing import Any
from src.classes.user_exception import CheckExit
from src.classes.working_with_files import MixinFormat
from src.classes.vacancy import Vacancy


class GUI(MixinFormat):
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

        window = sg.Window('Парсер вакансий', layout)
        event, values = window.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Exit'):
                window.close()
                raise CheckExit
            window.close()
            return event

    def create_input_field(self, data: dict[str, list[str]], check_exit=True, check_value=False) -> dict[Any]:
        """Метод создает поле для ввода на основе словаря с параметрами"""

        layout = [[sg.Text(data['name'])]]
        for i in data['line']:
            layout.append([sg.Text(i, size=20),
                           sg.InputText(size=20)])
        if check_exit:
            layout.append([sg.OK(), sg.Cancel('Exit')])
        else:
            layout.append([sg.OK()])

        window = sg.Window('Парсер вакансий', layout)
        event, values = window.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Exit'):
                window.close()
                raise CheckExit
            if check_value:
                if len(values) == 0:
                    self.print_message('Необходимо ввести минимум одно значение', title='Error', color='lightpink')
                    continue
            window.close()
            return values

    def create_table(self, data):
        f_data = self.table_formatting(data)
        layout = [[sg.Table(values=f_data['values'],
                            headings=f_data['headings'],
                            max_col_width=25,
                            auto_size_columns=True,
                            display_row_numbers=True,
                            right_click_selects=True,
                            justification='right',
                            num_rows=20,
                            key='-TABLE-',
                            row_height=20,
                            tooltip='This is a table')],
                  [sg.Text(f'Количество результатов: {len(f_data["values"])}')],
                  [sg.OK(), sg.Cancel('Exit')]]

        window = sg.Window('Парсер вакансий', layout)
        event, values = window.read()
        while True:
            if event in (sg.WIN_CLOSED, 'Exit'):
                window.close()
                raise CheckExit
            window.close()
            return True

    @staticmethod
    def get_progress_bar(title, number):
        """Метод возвращает настройки для запуска интерфейса отображения выполнения"""

        layout = [[sg.Text(title)],
                  [sg.ProgressBar(number, orientation='h', size=(20, 20), key='progress')],
                  [sg.Text(key='item', size=30)]]
        return layout

    @staticmethod
    def print_vacancy(data):
        """Функция выводит информацию о вакансиях на экран"""
        count = 0
        vacancy = Vacancy(data[count])

        layout = [[sg.Text(f'Вакансия {count + 1} из {len(data)}', key='number', size=80)],
                  [sg.Text(str(vacancy), key='item')],
                  [sg.Button('Назад', key='<'), sg.Button('Далее', key='>')],
                  [sg.OK('Вернуться к функциям', key=0), sg.Cancel('Exit')]]

        window = sg.Window('Информация о вакансии', layout)

        while True:
            event, values = window.read()
            if event == '<':
                if count == -len(data) + 1:
                    count = 0
                else:
                    count -= 1
            elif event == '>':
                if count == len(data) - 1:
                    count = 0
                else:
                    count += 1
            elif event == 'Exit':
                window.close()
                raise CheckExit
            elif event == 0:
                window.close()
                return
            vacancy = Vacancy(data[count])
            number = count + 1 if count >= 0 else len(data) + count - 1 if event == ">" else len(data) + count + 1
            window['number'].update(f'Вакансия {number} из {len(data)}')
            window['item'].update(str(vacancy))
