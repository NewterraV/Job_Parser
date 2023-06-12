from src.classes.work_with_user import WorkWithUser

if __name__ == "__main__":
    user = WorkWithUser()
    while True:

        # проверяем статус получения вакансий от API
        if user.get_vacancy_in_user_platform():
            while True:

                # Предлагаем выбрать действие с вакансиями
                vacancy = user.get_function()

                # Выводим результат выполнения
                if type(vacancy) is list:
                    if vacancy:
                        user.print_vacancy(vacancy)
                        continue
                    print('К сожалению, вакансии с данными параметрами отсутствуют.')
                    continue
                if vacancy:
                    continue
                break

            # Выполняем очистку файла перед завершением
            user.record.clear_file()

            # Предлагаем пользователю повторить поиск
            if user.get_repeat():
                continue
        break
