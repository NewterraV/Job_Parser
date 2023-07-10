import psycopg2
import psycopg2.extras
from tqdm import tqdm

from src.config import config


class WorkWithDB:
    """Класс для генерации и наполнения DataBase"""
    __slots__ = 'params'

    def __init__(self):
        self.params = config()

    def create_database(self, db_name='vacancies') -> None:
        """Метод создает базу данных с необходимыми таблицами"""

        # открытие соединения с базой данных
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        # Создание новой базы данных
        try:
            cur.execute(f"CREATE DATABASE {db_name}")
        except psycopg2.DatabaseError:
            cur.execute(f"DROP DATABASE {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")

        conn.close()

        # Открытие соединения с созданной базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление таблицы employer
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employer (
                    employer_id INTEGER PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    area VARCHAR(70),
                    url TEXT
                )
            """)

        # Добавление таблицы vacancies
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INT REFERENCES employer(employer_id),
                    title VARCHAR(200) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(5),
                    area VARCHAR(70),
                    created DATE,
                    url TEXT,
                    requirement VARCHAR(255)
                    )
            """)

        # закрытие соединения
        conn.commit()
        conn.close()

    def clear_database(self, db_name='vacancies') -> None:
        """Метод очищает данные из таблиц базы данных"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу employer
        with conn.cursor() as cur:
            cur.execute("""
                        TRUNCATE TABLE vacancies;
                        TRUNCATE TABLE employer;
                        """)

        # Закрытие соединения
        conn.commit()
        conn.close()

    def save_data_to_employer(self, data: list[dict[str, int]]) -> None:
        """Метод добавляет данные в таблицу employer"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу employer
        with conn.cursor() as cur:
            for item in tqdm(data, bar_format='{l_bar}{bar}{n_fmt}/{total_fmt} [{elapsed}]',
                             colour='green'):
                cur.execute("""
                    INSERT INTO employer (employer_id, title, url, area)
                    VALUES (%s, %s, %s, %s)
                """, (item['id'], item['name'], item['url'], item['area']))

        # Закрытие соединения
        conn.commit()
        conn.close()

    def save_data_to_vacancies(self, data) -> None:
        """Метод добавляет данные в таблицу vacancies"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу vacancies
        with conn.cursor() as cur:
            for item in tqdm(data, bar_format='{l_bar}{bar}{n_fmt}/{total_fmt} [{elapsed}]',
                             colour='green'):
                cur.execute("""
                            INSERT INTO vacancies 
                            (employer_id, title, salary_from, salary_to, currency, area, created, url, requirement)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (item['employer_id'],
                              item['name'],
                              item['salary']['from'],
                              item['salary']['to'],
                              item['salary']['currency'],
                              item['area'],
                              item['created'],
                              item['url'],
                              item["requirement"]
                              ))

        # Закрытие соединения
        conn.commit()
        conn.close()


class DBmanager(WorkWithDB):
    """Класс для работы с данными DataBase"""

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Метод получает список всех компаний и количество вакансий у каждой компании"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу vacancies
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""SELECT employer.title, 
                ROUND(avg(salary_from), 1) as avg_salary
                FROM employer
                JOIN vacancies USING(employer_id)
                GROUP BY employer_id"""
                        )
            data = []
            for i in cur:
                data.append({'Name': i[0], 'avg_salary': float(i[1])})

        # Закрытие соединения
        conn.commit()
        conn.close()
        return data

    def get_all_vacancies(self) -> list[dict]:
        """Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу vacancies
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""SELECT 
            vacancies.title, employer.title, 
            concat(salary_from, '-', salary_to, ' ', currency) as salary, vacancies.url
            FROM vacancies
            JOIN employer USING(employer_id)"""
                        )
            data = []
            for i in cur:
                data.append({'vacancy': i[0], 'employer': i[1], 'salary': i[2], 'url': i[3]})

        # Закрытие соединения
        conn.commit()
        conn.close()
        return data

    def get_avg_salary(self) -> float:
        """Метод получает среднюю зарплату по вакансиям"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу vacancies
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""SELECT ROUND(AVG(salary_from), 1)
                                   FROM vacancies"""
                        )
            for i in cur:
                data = float(i[0])

        # Закрытие соединения
        conn.commit()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self) -> list[dict]:
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""SELECT vacancies.title,
                        employer.title,
                        salary_from,
                        salary_to,
                        currency,
                        vacancies.area,
                        vacancies.url,
                        created,
                        requirement
                        FROM vacancies
                        JOIN employer USING(employer_id)
                        WHERE salary_from >= (SELECT AVG(salary_from) FROM vacancies)"""
                        )
            data = []
            for i in cur:
                salary = {'from': i[2],
                          'to': i[3],
                          'currency': i[4]
                          }
                data.append({'aggregator': None,
                             'name': i[0],
                             'employer': i[1],
                             "salary": salary,
                             'area': i[5],
                             'created': i[7],
                             'url': i[6],
                             'requirement': i[8]
                             })

        # Закрытие соединения
        conn.commit()
        conn.close()
        return data

    def get_vacancies_with_keyword(self,  keyword):
        """Поиск вакансий по ключевому слову в названии"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"""SELECT vacancies.title,
                        employer.title,
                        salary_from,
                        salary_to,
                        currency,
                        vacancies.area,
                        vacancies.url,
                        created,
                        requirement
                        FROM vacancies
                        JOIN employer USING(employer_id)
                        WHERE vacancies.title LIKE '%{keyword}%'"""
                        )
            data = []
            for i in cur:
                salary = {'from': i[2],
                          'to': i[3],
                          'currency': i[4]
                          }
                data.append({'name': i[0],
                             'employer': i[1],
                             "salary": salary,
                             'area': i[5],
                             'created': i[7],
                             'url': i[6],
                             'requirement': i[8]
                             })

        # Закрытие соединения
        conn.commit()
        conn.close()
        return data
