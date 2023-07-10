from src.classes.work_with_user import WorkWithUserBase, WorkWithUserKeyWord, WorkWithUserEmployer, WorkWithUserFilters
from src.classes.DBmanger import WorkWithDB
from src.classes.user_exception import CheckExit
from requests import HTTPError, ConnectionError


if __name__ == "__main__":
    user = WorkWithUserBase()
    db = WorkWithDB()
    db.create_database()
    while True:
        try:
            user_start = user.starting_program()
            if user_start == '1':
                while True:
                    function = user.search_type_selection()
                    if function == '1':
                        user = WorkWithUserKeyWord()
                        user.keyword_search()
                        break

                    elif function == '2':
                        user = WorkWithUserEmployer()
                        user.search_by_employer()
                        break
            elif user_start == '2':
                user.create_config_database()
                continue
            user = WorkWithUserFilters()
            user.job_analysis()

            break

        except (HTTPError, ConnectionError):
            print('\033[31Неполадки с подключением к серверу:\033[0m'
                  )

        except CheckExit:
            print('\033[31mВыполняется выход из приложения.\033[0m')

        finally:
            # Предлагаем пользователю повторить поиск
            if user.get_repeat():
                db.clear_database()
                continue
            if user.get_drop_db():
                db.drop_db()
            break
