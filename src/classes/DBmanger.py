import psycopg2

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
                    salary_currency VARCHAR(5),
                    area VARCHAR(70),
                    url TEXT,
                    requirement VARCHAR(180)
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
            for item in data:
                cur.execute("""
                    INSERT INTO employer (employer_id, title, url, area)
                    VALUES (%s, %s, %s, %s)
                """, (item['id'], item['name'], item['url'], item['area']))

        # Закрытие соединения
        conn.commit()
        conn.close()
