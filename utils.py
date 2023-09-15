import requests
import psycopg2
from math import ceil
COMPANY_NAMES = ['Diasoft', 'Softline', 'SKYPRO', 'VK', 'Вебиум', 'Гринатом', 'Лаборатория Касперского',
                 'Лига Цифровой Экономики', 'Московская Биржа', 'РТУ МИРЭА']


def get_ids(company_names: list[str]) -> dict[str, str]:
    """Функция перебирает компании из списка и для каждой находит id"""

    company_ids = {}

    for company in company_names:
        responses = requests.get('https://api.hh.ru/employers', params={'area': '113', 'text': company}).json()['items']
        for response in responses:
            if response['name'].lower() == company.lower():
                company_ids[company] = response['id']

    return company_ids


def company_get_info(company_ids: dict[str, str]) -> list[dict]:
    """Функция перебирает значения из списка, по id находит информацию о компании"""
    companies_info = []

    for company_id in company_ids.values():
        response = requests.get('https://api.hh.ru/employers/' + company_id).json()
        data = {
            'id': company_id,
            'name': response['name'],
            'description': response['alternate_url'],
            'open_vacancies': response['open_vacancies']
        }
        companies_info.append(data)

    return companies_info


def vacancies_get_info(company_ids: dict[str, str]) -> list[dict]:
    """Функция перебирает значения из списка, по id находит информацию о вакансиях"""

    vacancies_info = []
    for company_id in company_ids.values():
        amount = requests.get('https://api.hh.ru/vacancies', params={'employer_id': company_id}).json()['found']
        pages = ceil(amount/50)

        for page in range(pages):
            vacancies = requests.get('https://api.hh.ru/vacancies',
                                     params={'employer_id': company_id, 'page': page, 'per_page': 50}).json()['items']

            for vacancy in vacancies:

                try:
                    data = {'id': vacancy['id'], 'name': vacancy['name'], 'company_id': company_id,
                            'salary_from': vacancy['salary']['from'], 'salary_to': vacancy['salary']['to'],
                            'currency': vacancy['currency'], 'url': vacancy['alternate_url']}
                except TypeError as e:
                    data = {'id': vacancy['id'], 'name': vacancy['name'], 'company_id': company_id,
                            'salary_from': None, 'salary_to': None, 'currency': None, 'url': vacancy['alternate_url']}
                except KeyError as e:
                    if e.args[0] == 'currency':
                        data = {'id': vacancy['id'], 'name': vacancy['name'], 'company_id': company_id,
                                'salary_from': vacancy['salary']['from'], 'salary_to': vacancy['salary']['to'],
                                'currency': None, 'url': vacancy['alternate_url']}
                vacancies_info.append(data)

    return vacancies_info


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных для сохранения данных о компаниях и вакансиях"""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    try:
        cur.execute(f'CREATE DATABASE {database_name}')
    except Exception:
        cur.execute(f'DROP DATABASE {database_name}')
        cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE companies (
                company_id INTEGER PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                description TEXT,
                open_vacancies INTEGER
            )
            """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE vacancies (
                vacancy_id INTEGER PRIMARY KEY,
                vacancy_name TEXT,
                company_id INT REFERENCES companies(company_id),
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(5),
                url TEXT
            )
            """
        )

    conn.commit()
    conn.close()


def save_data_to_companies(data: list[dict], database_name: str, params: dict) -> None:
    """Сохранение данных в таблицу companies"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in data:
            cur.execute(
                """
                INSERT INTO companies (company_id, company_name, description, open_vacancies)
                VALUES (%s, %s, %s, %s)
                """,
                (int(company['id']), company['name'], company['description'], int(company['open_vacancies']))
            )

    conn.commit()
    conn.close()


def save_data_to_vacancies(data: list[dict], database_name: str, params: dict) -> None:
    """Сохранение данных в таблицу vacancies"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vacancy in data:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, company_id, salary_from, salary_to, currency, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (int(vacancy['id']), vacancy['name'], int(vacancy['company_id']), vacancy['salary_from'],
                 vacancy['salary_to'], vacancy['currency'], vacancy['url'])
            )

    conn.commit()
    conn.close()
