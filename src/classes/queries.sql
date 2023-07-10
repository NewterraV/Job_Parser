[create_database]
CREATE DATABASE {self.db_name};
CREATE TABLE employer (
    employer_id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    area VARCHAR(70),
    url TEXT
                );
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

[clear_database]
TRUNCATE TABLE vacancies, employer;

[drop_db]
DROP DATABASE {self.db_name};

[save_data_to_employer]
INSERT INTO employer (employer_id, title, url, area)
    VALUES (%s, %s, %s, %s);

[save_data_to_vacancies]
INSERT INTO vacancies
    (employer_id, title, salary_from, salary_to, currency, area, created, url, requirement)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);

[get_companies_and_vacancies_count]
SELECT employer.title,
    ROUND(avg(salary_from), 1) as avg_salary
FROM employer
JOIN vacancies USING(employer_id)
GROUP BY
ORDER BY employer.title;


[get_all_vacancies]
SELECT vacancies.title,
    employer.title,
    concat(salary_from, '-', salary_to, ' ', currency) as salary,
    vacancies.url
FROM vacancies
JOIN employer USING(employer_id)
ORDER BY vacancies.title;

[get_avg_salary]
SELECT ROUND(AVG(salary_from), 1)
FROM vacancies;

[get_vacancies_with_higher_salary]
SELECT vacancies.title,
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
WHERE salary_from >= (SELECT AVG(salary_from) FROM vacancies)
ORDER BY vacancies.title;

[get_vacancies_with_keyword]
SELECT vacancies.title,
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
WHERE LOWER(vacancies.title) LIKE %KEYWORD%
ORDER BY vacancies.title;
