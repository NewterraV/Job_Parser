import psycopg2
import psycopg2.extras
from tqdm import tqdm

from src.config import config


class DBmanager:
    """Класс для работы с DataBase"""
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
                    url TEXT,
                    requirement VARCHAR(255)
                    )
            """)

        # закрытие соединения
        conn.commit()
        conn.close()

    def save_data_to_employer(self, data: list[dict[str, int]]) -> None:
        """Метод добавляет данные в таблицу employer"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу employer
        with conn.cursor() as cur:
            for item in tqdm(data, colour='green'):
                cur.execute("""
                    INSERT INTO employer (employer_id, title, url, area)
                    VALUES (%s, %s, %s, %s)
                """, (item['id'], item['name'], item['url'], item['area']))

        # Закрытие соединения
        conn.commit()
        conn.close()

    def save_data_to_vacancies(self, data):
        """Метод добавляет данные в таблицу vacancies"""

        # Открытие соединения с базой данных
        conn = psycopg2.connect(dbname='vacancies', **self.params)

        # Добавление данных в таблицу vacancies
        with conn.cursor() as cur:
            for item in tqdm(data, colour='green'):
                cur.execute("""
                            INSERT INTO vacancies 
                            (employer_id, title, salary_from, salary_to, currency, area, url, requirement)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (item['employer_id'],
                              item['name'],
                              item['salary']['from'],
                              item['salary']['to'],
                              item['salary']['currency'],
                              item['area'],
                              item['url'],
                              item["requirement"]
                              ))

        # Закрытие соединения
        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self):
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

    def get_all_vacancies(self):
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

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass