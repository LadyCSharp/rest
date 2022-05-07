import requests
import pprint

#token = 'MY_TOKEN'
token = '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'
url = 'https://api.github.com/search/code?q=select+in:file+language:python'
#url = 'https://api.github.com/search/code?q=sqlite3 select insert delete update eval+in:file+language:python'

session = requests.Session()
session.auth = ('LadyCSharp', token)

result = session.get(url).json()

items = result['items']
d=dict()
mess='В коде используется sqlite3'
for item in items:
    if not item['path'].startswith('venv'):
        pprint.pprint(item)
        #with open(item['url'], 'rt') as f:
        #    text=f.readlines()
        #    if 'eval' in text:
        #        mess='В коде используется eval'
        #    if 'sqlite3' in text:
        #        mess='В коде используется sqlite3'
         
        if item['repository']['html_url'] in d:
            d[item['repository']['html_url']].append({
               'name': item['name'],
               'unsafe code type': mess, 
               'status': 'Потенциально опасен'
                })
        else:
            d[item['repository']['html_url']]=[{
               'name': item['name'],
               'unsafe code type': mess,
               'status': 'Потенциально опасен'
                }]


pprint.pprint(d)