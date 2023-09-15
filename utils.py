import requests
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
