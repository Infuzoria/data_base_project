import psycopg2
from config import config
from pandas import DataFrame


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self, database_name: str):
        self.name = database_name
        self.__params = config()

    def get_companies_and_vacancies_count(self):
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
        return rows
