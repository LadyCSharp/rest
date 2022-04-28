import requests
import pprint
import json
url = 'https://api.hh.ru/vacancies'

d=dict()
d['keywords']= 'C#'
d['requirements']=[{'name':'C#', 'count':1}]
sal=0
for p in range(1,12):
    params = {
        'text': 'C#',
        'area': 66,
        'only_with_salary': True,
        'page': p # есть страницы т.к. данных много
        }

    result = requests.get(url, params=params).json()
    d['count']=result['found']
    for i in range(len(result['items'])):
        print(p, i)
        #print(result['items'][i]['url'])
        #print(result['items'][i]['area']['name'])
        print(result['items'][i]['name'])
        
        for req in result['items'][i]['snippet']['requirement'].replace('<highlighttext>','').replace('</highlighttext>','').replace('(','').replace(')','').split():
            #print(req)
            fl=False
            for j in range(len(d['requirements'])):
                if req == d['requirements'][j]['name']:
                    d['requirements'][j]['count']+=1
                    fl=True
            if not fl:
                d['requirements'].append({'name':req, 'count':1})
        if result['items'][i]['salary']['from']:
            #print(result['items'][i]['salary']['from'])
            sal+=result['items'][i]['salary']['from']
        elif result['items'][i]['salary']['to']:
            #print(result['items'][i]['salary']['to'])
            sal+=result['items'][i]['salary']['to']
d['salary']=sal/d['count']
d['requirements']=sorted(d['requirements'], key=lambda q: q['count'],reverse=True)
print('----------------------')  
print(d)
print('----------------------') 
with open('hh.json', 'w') as f:
       # for purshcase in his:
            json.dump(d, f)