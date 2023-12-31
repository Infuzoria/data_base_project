# data_base_project
**Курсовой проект по базам данных.** 
В рамках проекта были получены данные о компаниях и вакансиях с сайта hh.ru, 
спроектированы таблицы в БД PostgreSQL и загружены данные в созданные таблицы.

# Структура проекта
:one: **main.py** - основной модуль программы, содержит функцию, которая демонстрирует работу модулей.\
:two: **database.ini** - конфигурационный файл, содержит параметры, необходимые для подключения к базе данных.\
:three: **config.py** - содержит единственную функцию config, которая считывает данные из конфигурационного файла
и создает словарь с параметрами на их основе.\
:four: **utils.py** - содержит функции для работы с API и базой данных.
1. *get_ids* - получает на вход список с названиями компаний и возвращает словарь. 
В качестве ключа берется название компании, в качестве значения - ID компании.
2. *company_get_info* - получает информацию о компаниях. На вход подается список с названиями компаний, 
возвращает список словарей. В словарях содержится упорядоченная информация о компаниях.
3. *vacancies_get_info* - похожая функция, возвращает информацию по вакансиям. На вход подается 
список с названиями компаний, на выходе получаем список словарей.
4. *create_database* - создает базу данных и две таблицы: companies, vacancies.
5. *save_data_to_companies* - сохраняет полученные данные о компаниях в базу данных.
6. *save_data_to_vacancies* - сохраняет полученную информацию о вакансиях в базу данных.\

:five: **work_with_db** - содержит класс DBManager. Класс позволяет работать с созданной базой данных, 
выводить значения из нее.
1. *get_companies_and_vacancies_count* - получает список всех компаний и количество вакансий у каждой компании.
2. *get_vacancies_by_company* - получает список вакансий указанной компании.
3. *get_all_vacancies* - получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты 
и ссылки на вакансию.
4. *get_avg_salary_from* - получает среднюю зарплату по вакансиям по нижней границе.
5. *get_avg_salary_to* - получает среднюю зарплату по вакансиям по верхней границе.
6. *get_vacancies_with_higher_salary_from* - получает список всех вакансий, у которых нижний уровень зарплаты 
выше средней по всем вакансиям.
7. *get_vacancies_with_higher_salary_to* - получает список всех вакансий, у которых верхний уровень зарплаты
выше средней по всем вакансиям.
8. *get_vacancies_with_keyword* - получает список всех вакансий, в названии которых
содержится переданное в метод слово.
