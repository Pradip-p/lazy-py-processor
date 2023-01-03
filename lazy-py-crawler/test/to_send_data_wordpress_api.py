import os
import json
import requests
import base64

url = 'https://shirtof.com/wp-json/wp/v2/posts'

user = 'demo'

password = '3tEv efYM w30d 7Asn 9hS9 QilX'

credentials = user + ':' + password


# token = base64.b64decode(creds.encode())
token = base64.b64encode(credentials.encode())
# header = {'Authorization':'Basic'+token.decode('latin-1')}

header = {'Authorization': 'Basic ' + token.decode('utf-8'),
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}

post = {
    'date': '2022-03-23T10:00:00',
    'title': 'testing',
    'content': 'testing testing 123',
    'status': 'publish',
    "title": 'test',
}

wordPressresponse = requests.get(url , headers=header)
print(wordPressresponse.text)

with open('wordPresResponseLog.txt', 'a') as wPResponse:
    wPResponse.write(str(wordPressresponse))