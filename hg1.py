import requests
import pprint

#token = 'MY_TOKEN'
token = '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'
url = 'https://api.github.com/search/code?q=sqlite3 select insert delete update eval+in:file+language:python'
session = requests.Session()
session.auth = ('LadyCSharp', token)

result = session.get(url).json()

items = result['items']
d=dict()
for item in items:
    if not item['path'].startswith('venv'):
        pprint.pprint(item)
