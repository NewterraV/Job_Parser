from requests import HTTPError, ConnectionError


def get_user_vacancies(keyword: str, user_platform: list, all_result=False) -> [list, False]:
    """Функция на основе списка платформ выдает список словарей вакансий. По флагу all_result определяет
    количество возвращаемых результатов. В случае ошибок со стороны сервера вернет False"""

    all_vacancy = []
    while True:
        try:
            for i in user_platform:
                vacancies = i(keyword)
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


def get_top_vacancies(list_: list):
    """Функция возвращает топ 5 вакансий по зарплате"""
    return sorted(list_, reverse=True)[:5]
