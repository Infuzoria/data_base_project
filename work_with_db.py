import psycopg2
from config import config


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

    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""

        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT company_name, vacancy_name,
                salary_from, salary_to, currency, url
                FROM vacancies
                INNER JOIN companies USING(company_id)
                ORDER BY company_name
                """
            )
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_avg_salary_from(self) -> float:
        """Получает среднюю зарплату по вакансиям по нижней границе"""

        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancies""")
            avg_salary = float(cur.fetchone()[0])

        conn.close()
        return avg_salary

    def get_avg_salary_to(self) -> float:
        """Получает среднюю зарплату по вакансиям по верхней границе"""

        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_to) FROM vacancies""")
            avg_salary = float(cur.fetchone()[0])

        conn.close()
        return avg_salary

    def get_vacancies_with_higher_salary_from(self) -> list[tuple]:
        """Получает список всех вакансий, у которых нижний уровень зарплаты
        выше средней по всем вакансиям"""

        avg_salary_from = self.get_avg_salary_from()
        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT company_name, vacancy_name, 
                salary_from, salary_to, currency, url
                FROM vacancies
                INNER JOIN companies USING(company_id)
                WHERE salary_from > {avg_salary_from}
                """
            )
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_vacancies_with_higher_salary_to(self) -> list[tuple]:
        """Получает список всех вакансий, у которых верхний уровень зарплаты
        выше средней по всем вакансиям"""

        avg_salary_to = self.get_avg_salary_to()
        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT company_name, vacancy_name, 
                salary_from, salary_to, currency, url
                FROM vacancies
                INNER JOIN companies USING(company_id)
                WHERE salary_from > {avg_salary_to}
                """
            )
            rows = cur.fetchall()

        conn.close()
        return rows

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Получает список всех вакансий, в названии которых
        содержится переданное в метод слово"""

        conn = psycopg2.connect(dbname=self.name, **self.__params)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT company_name, vacancy_name, 
                salary_from, salary_to, currency, url
                FROM vacancies
                INNER JOIN companies USING(company_id)
                WHERE vacancy_name LIKE '%{keyword.lower()}%'
                OR vacancy_name LIKE '%{keyword.title()}%'
                """
            )
            rows = cur.fetchall()

        conn.close()
        return rows
