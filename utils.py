import requests
COMPANY_NAMES = ['Diasoft', 'VK', 'Гринатом', 'КРОК', 'ЛАНИТ', 'Лаборатория Касперского',
                 'Лига Цифровой Экономики', 'Ростелеком', 'СБЕР', 'Яндекс']


def get_ids(company_names: list[str]):
    """Функция перебирает компании из списка и для каждой находит id"""

    company_ids = {}

    for company in company_names:
        responses = requests.get('https://api.hh.ru/employers', params={'text': company}).json()['items']
        for response in responses:
            if response['name'].lower() == company.lower():
                company_ids[company] = response['id']

    return company_ids
