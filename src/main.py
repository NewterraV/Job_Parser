from src.classes.work_with_user import WorkWithUserBase, WorkWithUserKeyWord, WorkWithUserEmployer, WorkWithUserFilters
from src.classes.DBmanger import WorkWithDB
from src.classes.user_exception import CheckExit
from utils import check_config, create_config_database
from requests import HTTPError, ConnectionError
from psycopg2 import ProgrammingError


if __name__ == "__main__":
    # Проверка наличия конфигурационного файла
    check_config()
    user = WorkWithUserBase()
    db = WorkWithDB()

    # Запуск основного функционала программы
    while True:
        try:
            user_start = user.starting_program()
            if user_start == '1':

                # Выбор типа поиска
                while True:
                    function = user.search_type_selection()

                    # Запуск поиска по ключевому слову
                    if function == '1':
                        db.create_database()
                        user = WorkWithUserKeyWord()
                        user.keyword_search()
                        break
                    # # Запуск поиска по работодателю
                    elif function == '2':
                        db.create_database()
                        user = WorkWithUserEmployer()
                        user.search_by_employer()
                        break
            # Генерация конфига database
            elif user_start == '2':
                create_config_database()
                continue
            user = WorkWithUserFilters()
            user.job_analysis()

            break

        except (HTTPError, ConnectionError):
            print('\033[31Неполадки с подключением к серверу:\033[0m'
                  )

        except CheckExit:
            print('\033[31mВыполняется выход из приложения.\033[0m')

        except ProgrammingError:
            print('\033[31mВНИМАНИЕ: отсутствует или неверно сконфигурирован'
                  ' файл конфигурации для доступа к базе данных.'
                  '\nПриступаю к генерации:\033[0m')
            create_config_database()
            continue

        finally:
            # Предлагаем пользователю повторить поиск
            if user.get_repeat():
                db.clear_database()
                continue
            if user.get_drop_db():
                db.drop_db()
            break
