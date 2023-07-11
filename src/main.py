from src.classes.work_with_user import WorkWithUserBase, WorkWithUserKeyWord, WorkWithUserEmployer, WorkWithUserFilters
from src.classes.DBmanger import WorkWithDB
from src.classes.user_exception import CheckExit
from src.classes.GUI import GUI
from utils import check_config, create_config_database
from requests import HTTPError, ConnectionError
from psycopg2 import ProgrammingError

if __name__ == "__main__":
    # Проверка наличия конфигурационного файла
    check_config()
    user = WorkWithUserBase()
    db = WorkWithDB()
    db.create_database()

    # Запуск основного функционала программы
    while True:
        while True:
            try:
                user_start = user.starting_program()
                if user_start == '1':

                    # Выбор типа поиска
                    while True:
                        function = user.search_type_selection()
                        # Запуск поиска по ключевому слову
                        if function == '1':
                            user = WorkWithUserKeyWord()
                            user.keyword_search()
                            break
                        # # Запуск поиска по работодателю
                        elif function == '2':
                            user = WorkWithUserEmployer()
                            user.search_by_employer()
                            break
                # Генерация конфига database
                elif user_start == '2':
                    create_config_database()
                    continue
                user = WorkWithUserFilters()
                user.job_analysis()

            except (HTTPError, ConnectionError):
                GUI.print_message('Неполадки с подключением к серверу:', title='Error', color='lightpink')
                break

            except CheckExit:
                GUI.print_message('Выполняется выход из приложения.')
                break

            except ProgrammingError:
                GUI.print_message('ВНИМАНИЕ:неверно сконфигурирован'
                                  ' файл конфигурации для доступа к базе данных.'
                                  '\nПриступаю к генерации:', title='Error', color='lightpink')

                create_config_database()
                break

            else:
                if user.get_repeat():
                    db.clear_database()
                    continue
            break

        # Предлагаем пользователю повторить поиск
        if user.get_repeat():
            db.clear_database()
            continue
        if user.get_drop_db():
            db.drop_db()
        break
