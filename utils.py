import requests
COMPANY_NAMES = ['Diasoft', 'Softline', 'VK', 'Альфа-Банк', 'Гринатом', 'Лаборатория Касперского',
                 'Лига Цифровой Экономики', 'Московская Биржа', 'РТУ МИРЭА', 'Яндекс']


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
