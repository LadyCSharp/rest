import requests
import pprint


url = 'https://api.hh.ru/vacancies'

params = {
    'text': 'c#',
    'area': 66,
    'page': 1 # есть страницы т.к. данных много
    }

result = requests.get(url, params=params).json()

pprint.pprint(result)
items = result['items']
first = items[0]

pprint.pprint(first)

