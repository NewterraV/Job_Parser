from requests import HTTPError, ConnectionError


def get_user_vacancies(user_platform, keyword=None,  all_result=False) -> [list, False]:
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
