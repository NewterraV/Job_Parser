import psycopg2

from src.config import config


class DBmanager():
    """Класс для работы с DataBase"""
    __slots__ = 'params'

    def __init__(self):
        self.params = config()

    def create_database(self, db_name='vacancies'):
        """Метод создает базу данных с необходимыми таблицами"""

        # открытие соединения с базой данных
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        # Создание новой базы данных
        cur.execute(f"DROP DATABASE {db_name}")
        cur.execute(f"CREATE DATABASE {db_name}")
        conn.close()

        # Открытие соединения с созданной базой данных
        conn = psycopg2.connect(db_name='vacancies', **self.params)

        # Добавление таблицы employer
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employer (
                    employer_id INTEGER PRIMARY KEY
                    title VARCHAR(255) NOT NULL
                    url TEXT
                    area VARCHAR(70)
                )
                """
            )

        # Добавление таблицы vacancies
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY
                    employer_id INT REFERENCES employer(employer_id)
                    title VARCHAR(200) NOT NULL
                    salary_from INTEGER
                    salary_to INTEGER
                    salary_currency VARCHAR(5)
                    area VARCHAR(70)
                    url TEXT
                    requirement VARCHAR(180)
                    )
            """)

        # закрытие соединения
        conn.commit()
        conn.close()
