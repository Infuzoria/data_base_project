import psycopg2
from config import config
from pandas import DataFrame


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self, database_name: str):
        self.name = database_name
        self.__params = config()

    def get_companies_and_vacancies_count(self) -> dict[str, int]:
        """Получает список всех компаний и количество вакансий у каждой компании"""

        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT company_name, COUNT(*) FROM vacancies
                INNER JOIN companies USING(company_id)
                GROUP BY company_name
                ORDER BY COUNT(*)
                """
            )
            rows = dict(cur.fetchall())

        conn.close()
        return rows

    def get_vacancies_by_company(self, company_name: str) -> list[tuple]:
        """Получает список вакансий указанной компании"""

        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT vacancy_name, salary_from, salary_to, currency, url
                FROM vacancies
                INNER JOIN companies USING(company_id)
                WHERE company_name = '{company_name}'
                """
            )
            rows = cur.fetchall()

        conn.close()
        return rows
