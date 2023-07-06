from src.classes.work_with_user import WorkWithUserBase, WorkWithUserKeyWord

if __name__ == "__main__":
    while True:
        user = WorkWithUserBase()
        user_start = user.starting_program()
        if user_start == '1':
            while True:
                function = user.search_type_selection()
                if function == '1':
                    user = WorkWithUserKeyWord()
                    if user.keyword_search():
                        continue

                elif function == '2':
                    user = WorkWithUserEmployer()
                    if user.search_by_employer():
                        continue
                break
            break
        elif user_start == '2':
            user.create_config_database()
            continue
        break
