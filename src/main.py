from src.classes.work_with_user import WorkWithUserBase, WorkWithUserKeyWord, WorkWithUserEmployer
from src.classes.user_exception import CheckExit


if __name__ == "__main__":
    user = WorkWithUserBase()
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
            break

        except CheckExit:
            # Предлагаем пользователю повторить поиск
            if user.get_repeat():
                continue
            break
