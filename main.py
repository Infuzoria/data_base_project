import utils
from work_with_db import DBManager
from config import config


def main():

    # Получим ID компаний, информацию о которых необходимо сохранить в БД
    company_ids = utils.get_ids(utils.COMPANY_NAMES)

    # Получим информацию о компаниях и вакансиях по ID компаний
    companies_info = utils.company_get_info(company_ids)
    vacancies_info = utils.vacancies_get_info(company_ids)

    # Создаем базу данных
    params = config()
    db_name = 'hh_database'
    utils.create_database(db_name, params)

    # Заполняем БД данными
    utils.save_data_to_companies(companies_info, db_name, params)
    utils.save_data_to_vacancies(vacancies_info, db_name, params)

    # Выполняем запросы
    db_manager = DBManager(db_name, params)

    print("Список компаний:")
    list_of_companies = db_manager.get_companies_and_vacancies_count()
    for key, val in list_of_companies.items():
        print(key, val)

    print("Список всех вакансий:")
    list_of_vacancies = db_manager.get_all_vacancies()
    for row in list_of_vacancies:
        print(*row)

    avg_salary_to = db_manager.get_avg_salary_to()
    print(f"Средняя зарплата по верхнему уровню: {avg_salary_to}")

    print("Список вакансий с зарплатой выше средней по верхнему уровню:")
    data = db_manager.get_vacancies_with_higher_salary_to()
    for row in data:
        print(*row)

    print("Список вакансий, найденных по ключевому слову: Python")
    keyword_vacancies = db_manager.get_vacancies_with_keyword('Python')
    for row in keyword_vacancies:
        print(*row)


if __name__ == '__main__':
    main()
