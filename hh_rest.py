import requests
import pprint
import json
import time
url = 'https://api.hh.ru/vacancies'

d=dict()
d['keywords']= 'C#'
requirements=dict()

sal=0
for p in range(3):
    params = {
        'text': 'C#',
        'area': 66,
        'only_with_salary': True,
        'page': p # есть страницы т.к. данных много
        }

    result = requests.get(url, params=params).json()

    d['count']=result['found']
    items = result['items']
    #print(p)

    for item in items:
        #print(item['name'])
        urlv = item['url']
        res = requests.get(urlv).json()
        if res['key_skills']:
            for req in res['key_skills']:
                #print(req)
                r= req['name']

                if r in requirements:

                    requirements[r] += 1

                else:
                    requirements[r] =1
        if item['salary']['from']:
            #print(result['items'][i]['salary']['from'])
            sal+=item['salary']['from']
        elif item['salary']['to']:
            #print(result['items'][i]['salary']['to'])
            sal+=item['salary']['to']
    #pprint.pprint(d)
    #time.sleep(1)
d['salary']=sal/d['count']
d['requirements']=sorted(requirements.items(), key=lambda q: q[1],reverse=True)
# d['requirements'] = requirements
print('----------------------')  
pprint.pprint(d)
print('----------------------') 
with open('hh.json', 'w') as f:
       json.dump(d, f)