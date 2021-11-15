
import requests
import json

bot_token = '1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc'
chat_id = "1292677678"
#f="C:/Users/gareev_mr/Pictures/1.jpg"
file = "C:/Users/gareev_mr/Pictures/1.jpg"
print(file,type(file))

files = {
    'document': open(file, 'rb')
}

message = ('https://api.telegram.org/bot'+ bot_token + '/sendDocument?chat_id='+ chat_id)
send = requests.post(message, files = files)

{ 'message':
      {'message_id': 1806,
       'from':
          {'id': 1292677678,
           'is_bot': False,
           'first_name': 'Marat',
           'last_name': 'Gareev',
           'username': 'Maratgareev97',
           'language_code': 'ru'},
       'chat':
           {'id': 1292677678,
            'first_name': 'Marat',
            'last_name': 'Gareev',
            'username': 'Maratgareev97',
            'type': 'private'},
       'date': 1633286927,
       'text': '😜'}}

ss={'file_name': 'microsoft_logo.jpg', 'mime_type': 'image/jpeg', 'thumb': {'file_id': 'AAMCAgADGQEAAgY6YVjMbru8imas5_p-z5ukeaXwVEsAAo4RAAIzhMlK06vSqPZk0IYBAAdtAAMhBA', 'file_unique_id': 'AQADjhEAAjOEyUpy', 'file_size': 4946, 'width': 320, 'height': 256}, 'file_id': 'BQACAgIAAxkBAAIGOmFYzG67vIpmrOf6fs-bpHml8FRLAAKOEQACM4TJStOr0qj2ZNCGIQQ', 'file_unique_id': 'AgADjhEAAjOEyUo', 'file_size': 66717}
print(ss['file_id'])
'''import json

import wget
from flask import Flask
import requests
from flask import request
from flask import jsonify

app = Flask(__name__)
URL = 'https://api.telegram.org/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/'

def write_json(data, filename='answer.json'):
    with open(filename,'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_updates():
    url = URL + 'getUpdates'
    r=requests.get(url)
    #write_json(r.json())
    return r.json()

def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text':text}
    r = requests.post(url,json=answer)
    return r.json()

@app.route('/')
def index():
    return '<h1>Привет бот</h1>'

def deleteWebhook():
    url = URL + 'deleteWebhook'
    r=requests.get(url)
    write_json(r.json())

def main():
    #url = URL + 'getMe'

    #r = requests.post(url)
    #write_json(r.json())
    #get_updates()
    #r=get_updates()
    #chat_id = r['result'][-1]['message']['chat']['id']
    #send_message(chat_id)
    #deleteWebhook()
    pass

if __name__=='__main__':
    app.run()
    #main()
'''