import json
from flask import Flask, render_template, request, send_file, redirect, url_for, send_from_directory, session, \
    make_response
import wget
import requests
from flask import jsonify
import connection_db
from werkzeug.utils import secure_filename
import os, datetime
import rename_random
from transliterate import translit

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
URL = 'https://api.telegram.org/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/'


# https://api.telegram.org/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/setWebhook # удаление webhook
# https://api.telegram.org/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/setWebhook?url=https://9b31-213-87-132-139.ngrok.io # создание webhook
# https://api.telegram.org/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/getWebhookinfo # информация о webhook

def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        #json.dump(data, f, indent=2, ensure_ascii=False)
        json.dump(data, f, indent=2)


def send_message(chat_id, text='bla-bla-bla'):
    url = URL + 'sendMessage'
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        #return '200' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        r = request.get_json()

        st_r = str(r)
        #print(st_r,type(st_r))
        print(r, ' пришло!')
        #print(r.items())
        #print(r['message']['text'])
        #if 'document' in st_r:
        #    print(r[0])

        #return '200'
        if "'message'" in st_r:
            id_name = r['message']['chat']['id']  # определение id отправителя.
        else:
            return '200'


        if 'last_name' in st_r: # Не всегда есть last_name
            your_name = r['message']['from']['first_name'] + ' ' + r['message']['from']['last_name']
        else:
            your_name = r['message']['from']['first_name']

        connection = connection_db.get_connection()  # основной коннект
        print("Соединие установлено ", connection)
        cursor = connection.cursor()  # курсор есть курсор

        where_name=cursor.execute('SELECT * FROM users_list WHERE name LIKE %s', (id_name)) # Поиск id отправителя. Нужно для запрета публикации топика
        print(where_name, '   where_name ')

        topic_id = r['message']['chat']['id']

        if "'text'" in st_r or "document" in st_r or "photo" in st_r:
            if "'text'" in st_r:
                #return '200' # ВАЖНО! это в случае ending_update_count
                print(r['message']['text'], ' Это отправленный текст')

                if r['message']['text'] == '/start':
                    print('Сообщение пришло от ', your_name)
                    send_message(r['message']['chat']['id'], text='Здравствуйте ' + your_name + '. Ознакомтесь с инструкцией.')
                    print('новый запуск')


                #if where_name == 0 or (r['message']['text'] != '/new_topic' or r['message']['text'] != '/close_topic' \
                #                       or r['message']['text'] != '/help'):
                '''
                if where_name == 0:
                    print('Сообщение пришло от ', your_name)
                    send_message(r['message']['chat']['id'], text=your_name + 'У Вас нет открытых обращений. Вам необходимо открыть новое')
                    print('новый запуск')
                    '''
                if (r['message']['text'] != '/new_topic') and where_name==0:
                    print('Сообщение пришло от ', your_name)
                    send_message(r['message']['chat']['id'],
                                 text=your_name + 'У Вас нет открытых обращений. Вам необходимо открыть новое')
                    print('новый запуск')


                if where_name==1:
                    print('where_name = 1')
                    send_message(r['message']['chat']['id'], text='Введите полное описание проблемы')

                    cursor.execute("SELECT * FROM users_list WHERE name LIKE %s",(topic_id))  # узнаем id топика в который вносим изменения
                    id_odinakov=cursor.fetchall()
                    id_odinakov=id_odinakov[0]['topic_id']
                    print(id_odinakov, '     ', type(id_odinakov))
                    cursor.execute('INSERT INTO users_list (Name, topic_id) VALUES(%s,%s)',(id_name, id_odinakov))  # вставвка строки в таблицу user_list

                    cursor.execute("UPDATE topic SET title = %s WHERE ID = %s",(r['message']['text'],id_odinakov))
                    print('перезаписалось')

                if where_name==2:
                    print('Можешь дальше писать')
                    send_message(r['message']['chat']['id'], text='Прикрепите файл. Если не хотите введите "нет":')

                    cursor.execute("SELECT * FROM users_list WHERE name LIKE %s",(topic_id))  # узнаем id топика в который вносим изменения
                    id_odinakov=cursor.fetchall()
                    id_odinakov=id_odinakov[0]['topic_id']
                    print(id_odinakov, '     ', type(id_odinakov))
                    cursor.execute('INSERT INTO users_list (Name, topic_id) VALUES(%s,%s)',(id_name, id_odinakov))  # вставвка строки в таблицу user_list

                    cursor.execute("UPDATE topic SET body_text = %s WHERE ID = %s",(r['message']['text'],id_odinakov))
                    print('перезаписалось')

                if where_name==2 and 'photo' in st_r:
                    send_message(r['message']['chat']['id'], text='Спасибо за сообщение. Топик открыт.')

                    print('PHOTO')
                    print(r['message']['photo'][0]['file_id'], ' : Это id картинки')  # Это id картинки
                    id_image = URL + 'getFile?file_id=' + r['message']['photo'][len(r['message']['photo'])-1]['file_id']  # GET строка которая определяет путь к файлу (getFile это из api телеги)
                    # print(id_image, ' id_image')

                    r_image = requests.get(id_image)
                    r_j = r_image.json()  # запихиваем в json, т.е. читаем его
                    dir_image = r_j['result']['file_path']
                    print(dir_image)

                    url_dir_image = "https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/" + dir_image  # это путь к картинке
                    print(url_dir_image, '  ссылка на файл ')
                    wget.download(url_dir_image)  # качаем картинку


                if r['message']['text'] == '/new_topic' and where_name==0:
                    send_message(r['message']['chat']['id'], text='Введите тему сообщения:')

                    today = datetime.datetime.today()
                    date_time = today.strftime("%Y-%m-%d %H:%M:%S")  # 2017-04-05-00.18.00
                    title = ''
                    body_text=''
                    file_name='В процессе!'
                    status = ''

                    cursor.execute('INSERT INTO topic (author, date_time, title, body_text, file_name, status) VALUES(%s,%s,%s,%s,%s,%s)',\
                                                            (your_name, date_time, title, body_text,file_name,status))  # выполение sql команды

                    cursor.execute('SELECT id FROM topic ORDER BY id DESC LIMIT 1') # Определение последнего id в таблице topic
                    id_next = cursor.fetchall()  # перевод в словарь
                    id_next = id_next[0]['id']
                    print(id_next, ' последний id')

                    cursor.execute('INSERT INTO users_list (Name, topic_id) VALUES(%s,%s)', (id_name, id_next))  # вставвка строки в таблицу user_list

                if r['message']['text'] == '/close_topic' and where_name == 4:
                    #connection = connection_db.get_connection()  # основной коннект
                    #print("Соединие установлено ", connection)
                    #cursor = connection.cursor()  # курсор есть курсор
                    cursor.execute('SELECT topic_id FROM support.users_list WHERE name LIKE %s',(str(id_name)))
                    #return '200'
                    topic_id_user = cursor.fetchall()[-1]['topic_id']
                    cursor.execute(('DELETE FROM support.users_list WHERE topic_id = %s'), (int(topic_id_user)))
                    connection.commit()  # подтверждение изменений в базе
                    print('топик удален')

                    cursor.execute("UPDATE topic SET status = %s WHERE ID = %s", ('закрыт', int(topic_id_user)))
                    connection.commit()
                    #connection.close()

                if where_name==4:

                    cursor.execute('SELECT id FROM topic ORDER BY id DESC LIMIT 1')  # Определение последнего id в таблице topic
                    id_next = cursor.fetchall()  # перевод в словарь
                    id_next = id_next[0]['id']
                    print('where_name= ',where_name, 'id_next= ',id_next,'topic_id= ',topic_id,type(topic_id))

                    cursor.execute('SELECT topic_id FROM support.users_list WHERE Name = %s',(topic_id)) # определить id потика отправителя
                    search_topic_id=cursor.fetchall()
                    search_topic_id=search_topic_id[0]['topic_id']

                    today = datetime.datetime.today()
                    date_time = today.strftime("%Y-%m-%d %H:%M:%S")  # 2017-04-05-00.18.00

                    cursor.execute('INSERT INTO talk (topic_id, chat_id,author, date_time, answer,file_name) VALUES(%s,%s,%s,%s,%s,%s)',(search_topic_id, id_name, your_name, date_time, r['message']['text'], ''))  # выполение sql команды

                #    send_message(r['message']['chat']['id'], text='У Вас есть открытый топик. Закройте его.')

                if where_name==3:
                    send_message(r['message']['chat']['id'], text='Ваша заявка принята. Системный администратор скоро свяжется с Вами')


                    id_odinakov = cursor.fetchall()
                    id_odinakov = id_odinakov[0]['topic_id']
                    print(id_odinakov, '     ', type(id_odinakov))
                    cursor.execute('INSERT INTO users_list (Name, topic_id) VALUES(%s,%s)', (id_name, id_odinakov))  # вставвка строки в таблицу user_list

                    cursor.execute("UPDATE topic SET file_name = %s WHERE ID = %s", ('нет', id_odinakov))
                    cursor.execute("UPDATE topic SET status = %s WHERE ID = %s", ('открыт', id_odinakov))
                    print('перезаписалось фото')

            elif 'photo' in st_r and where_name==3:
                send_message(r['message']['chat']['id'], text='Ваша заявка принята. Системный администратор скоро свяжется с Вами')
                print('PHOTO!!!!!!!!!')
                print(r['message']['photo'][0]['file_id'], ' : Это id картинки')  # Это id картинки
                id_image = URL + 'getFile?file_id=' + r['message']['photo'][len(r['message']['photo'])-1]['file_id']  # GET строка которая определяет путь к файлу (getFile это из api телеги)
                # print(id_image, ' id_image')

                r_image = requests.get(id_image)
                r_j = r_image.json()  # запихиваем в json, т.е. читаем его
                dir_image = r_j['result']['file_path']
                print(dir_image)

                url_dir_image = "https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/" + dir_image  # это путь к картинке
                print(url_dir_image)
                wget.download(url_dir_image)  # качаем картинку

                id_odinakov = cursor.fetchall()
                print(id_odinakov, ' id_odinakov')
                id_odinakov = id_odinakov[0]['topic_id']
                print(id_odinakov, '     ', type(id_odinakov))
                cursor.execute('INSERT INTO users_list (Name, topic_id) VALUES(%s,%s)',
                               (id_name, id_odinakov))  # вставвка строки в таблицу user_list

                cursor.execute("UPDATE topic SET file_name = %s WHERE ID = %s", (url_dir_image, id_odinakov))
                cursor.execute("UPDATE topic SET status = %s WHERE ID = %s", ('открыт', id_odinakov))
                print('перезаписалось фото')

            elif 'document' in st_r and where_name == 3:
                send_message(r['message']['chat']['id'],text='Ваша заявка принята. Системный администратор скоро свяжется с Вами')
                print('Document!!!!!!!!!')
                # print(r['file_id'], ' : Это id документа')
                # return "200"
                # print(r['document'])
                max_size = r['message']['document']['file_id']
                print(r['message']['document']['file_id'], ' : Это id документа')  # Это id картинки
                # return "200"
                id_image = URL + 'getFile?file_id=' + max_size  # GET строка которая определяет путь к файлу (getFile это из api телеги)
                print(id_image, ' id_doc')

                r_image = requests.get(id_image)
                r_j = r_image.json()  # запихиваем в json, т.е. читаем его
                dir_image = r_j['result']['file_path']
                print(dir_image)

                url_dir_image = "https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/" + dir_image  # это путь к картинке
                print(url_dir_image)
                wget.download(url_dir_image)  # качаем картинку
                print('Качаем картинку')

                #cursor.execute('SELECT id FROM topic ORDER BY id DESC LIMIT 1')  # Определение последнего id в таблице topic
                #id_next = cursor.fetchall()  # перевод в словарь
                #id_next = id_next[0]['id']

                today = datetime.datetime.today()
                date_time = today.strftime("%Y-%m-%d %H:%M:%S")  # 2017-04-05-00.18.00

                cursor.execute('SELECT topic_id FROM support.users_list WHERE Name = %s',(topic_id))  # определить id потика отправителя
                search_topic_id = cursor.fetchall()
                search_topic_id = search_topic_id[0]['topic_id']
                print(search_topic_id)
                print(type(search_topic_id), type(id_name), type(your_name), type(date_time), " ", url_dir_image)
                print(search_topic_id, id_name, your_name, date_time, " ", url_dir_image)
                #return '200'
                #cursor.execute('INSERT INTO support.talk (topic_id, chat_id, author, date_time, answer,file_name) VALUES(%s,%s,%s,%s,%s,%s)',(search_topic_id, id_name, your_name, date_time, "", url_dir_image))  # выполение sql команды
                #cursor.execute("SELECT * FROM users_list WHERE name LIKE %s",(topic_id))  # узнаем id топика в который вносим изменения
                #id_odinakov = cursor.fetchall()
                #id_odinakov = id_odinakov[0]['topic_id']
                #print(id_odinakov, '     ', type(id_odinakov))
                cursor.execute('INSERT INTO support.users_list (Name, topic_id) VALUES(%s,%s)',(str(id_name), search_topic_id))  # вставвка строки в таблицу user_list

                cursor.execute("UPDATE support.topic SET file_name = %s WHERE ID = %s", (url_dir_image, search_topic_id))
                cursor.execute("UPDATE support.topic SET status = %s WHERE ID = %s", ('открыт', search_topic_id))
                print('перезаписалось док')
                # -------------------------------------------
                '''
                bot_token1 = '1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc'
                chat_id1 = "1292677678"
                # f="C:/Users/gareev_mr/Pictures/1.jpg"
                file1 = "C:/Users/gareev_mr/Pictures/1.jpg"
                print(file1, type(file1))

                files = {
                    'document': open(file1, 'rb')
                }

                message = ('https://api.telegram.org/bot' + bot_token1 + '/sendDocument?chat_id=' + chat_id1)
                send = requests.post(message, files=files)
                '''
            #--------------------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!--------------------------------------


            elif 'photo' in st_r and where_name == 4:
                print('PHOTO!!!!!!!!!')
                max_size=r['message']['photo'][len(r['message']['photo'])-1]['file_id']
                print(r['message']['photo'][0]['file_id'], ' : Это id картинки')  # Это id картинки
                id_image = URL + 'getFile?file_id=' + max_size  # GET строка которая определяет путь к файлу (getFile это из api телеги)
                #id_image = 'getFile?file_id=' + r['message']['photo'][0]['file_id']  # GET строка которая определяет путь к файлу (getFile это из api телеги)
                print(id_image, ' id_image')

                r_image = requests.get(id_image)
                r_j = r_image.json()  # запихиваем в json, т.е. читаем его
                dir_image = r_j['result']['file_path']
                print(dir_image)

                url_dir_image = "https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/" + dir_image  # это путь к картинке
                print(url_dir_image)
                wget.download(url_dir_image)  # качаем картинку


                cursor.execute('SELECT id FROM topic ORDER BY id DESC LIMIT 1')  # Определение последнего id в таблице topic
                id_next = cursor.fetchall()  # перевод в словарь
                id_next = id_next[0]['id']

                today = datetime.datetime.today()
                date_time = today.strftime("%Y-%m-%d %H:%M:%S")  # 2017-04-05-00.18.00

                cursor.execute('SELECT topic_id FROM support.users_list WHERE Name = %s',(topic_id))  # определить id потика отправителя
                search_topic_id = cursor.fetchall()
                search_topic_id = search_topic_id[0]['topic_id']
                cursor.execute('INSERT INTO talk (topic_id, chat_id, author, date_time, answer,file_name) VALUES(%s,%s,%s,%s,%s,%s)',(search_topic_id, id_name, your_name, date_time, "", url_dir_image))  # выполение sql команды
                #cursor.execute('INSERT INTO talk (topic_id, chat_id, author, date_time, answer,file_name) VALUES(%s,%s,%s,%s,%s,%s)',(id_next, id_name,your_name, date_time, '', url_dir_image))  # выполение sql команды

                #    send_message(r['message']['chat']['id'], text='У Вас есть открытый топик. Закройте его.')
                #cursor.execute('INSERT INTO users_list (Name, topic_id) VALUES(%s,%s)',(id_name, id_odinakov))  # вставвка строки в таблицу user_list

                #cursor.execute("UPDATE topic SET file_name = %s WHERE ID = %s", (url_dir_image, id_odinakov))
                print('перезаписалось фото')

            #---------------------

            elif 'document' in st_r and where_name == 4:
                print('Document!!!!!!!!!')
                #print(r['file_id'], ' : Это id документа')
                #return "200"
                #print(r['document'])
                max_size=r['message']['document']['file_id']
                print(r['message']['document']['file_id'], ' : Это id документа')  # Это id картинки
                #return "200"
                id_image = URL + 'getFile?file_id=' + max_size  # GET строка которая определяет путь к файлу (getFile это из api телеги)
                #id_image = 'getFile?file_id=' + r['message']['photo'][0]['file_id']  # GET строка которая определяет путь к файлу (getFile это из api телеги)
                print(id_image, ' id_doc')

                r_image = requests.get(id_image)
                r_j = r_image.json()  # запихиваем в json, т.е. читаем его
                dir_image = r_j['result']['file_path']
                print(dir_image)

                url_dir_image = "https://api.telegram.org/file/bot1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc/" + dir_image  # это путь к картинке
                print(url_dir_image)
                wget.download(url_dir_image)  # качаем картинку
                print('Качаем картинку')


                cursor.execute('SELECT id FROM topic ORDER BY id DESC LIMIT 1')  # Определение последнего id в таблице topic
                id_next = cursor.fetchall()  # перевод в словарь
                id_next = id_next[0]['id']

                today = datetime.datetime.today()
                date_time = today.strftime("%Y-%m-%d %H:%M:%S")  # 2017-04-05-00.18.00

                cursor.execute('SELECT topic_id FROM support.users_list WHERE Name = %s',(topic_id))  # определить id потика отправителя
                search_topic_id = cursor.fetchall()
                search_topic_id = search_topic_id[0]['topic_id']
                print(search_topic_id)
                print(type(search_topic_id), type(id_name), type(your_name), type(date_time), " ", url_dir_image)
                cursor.execute('INSERT INTO support.talk (topic_id, chat_id, author, date_time, answer,file_name) VALUES(%s,%s,%s,%s,%s,%s)',(search_topic_id, id_name, your_name, date_time, "", url_dir_image))  # выполение sql команды
                #cursor.execute('INSERT INTO support.talk (topic_id, chat_id, author, date_time, answer,file_name) values (84,1292677678,"Marat","2021-10-02 20:34:34","","");')
                print('перезаписалось фото')
                #-------------------------------------------
                '''
                bot_token1 = '1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc'
                chat_id1 = "1292677678"
                # f="C:/Users/gareev_mr/Pictures/1.jpg"
                file1 = "C:/Users/gareev_mr/Pictures/1.jpg"
                print(file1, type(file1))

                files = {
                    'document': open(file1, 'rb')
                }

                message = ('https://api.telegram.org/bot' + bot_token1 + '/sendDocument?chat_id=' + chat_id1)
                send = requests.post(message, files=files)
                '''
            #----------------------



            connection.commit()
            connection.close()

            send_message(r['message']['chat']['id'], text='Соббщение принято сервером!')
            # print(r['message']['chat']['id'], " r['message']['chat']['id']")
            write_json(r)
            return jsonify(r)
        else:
            send_message(r['message']['chat']['id'], text='Недопустимый формат')
            print('недопустимый формат')
            return "200"


#return 1
# return '<h1>Привет бот!</h1>'


# https://api.telegram.org/bot1672815585:AAF7AfgKlB7ULG5mVUpWqRdvRJtQXFh_lNQ/setWebhook?url=https://45b84249eabc.ngrok.io

# -----------------------------------------------------------------------------------------------------------------------------

@app.route('/admin/<status>')
def index1(status):
    connection = connection_db.get_connection()  # основной коннект
    print("Соединие установлено ", connection,status)
    if status=='Все':
        sql = "SELECT * FROM topic"
        cursor = connection.cursor()  # курсор есть курсор

        cursor.execute(sql)  # выполение sql команды
        topic_table = cursor.fetchall()  # fetchall() это перевод обьекта в кортеж

    if status == "закрыт":
        sql = "select * from support.topic t WHERE status = 'закрыт'"
        cursor = connection.cursor()  # курсор есть курсор

        cursor.execute(sql)  # выполение sql команды
        topic_table = cursor.fetchall()  # fetchall() это перевод обьекта в кортеж

    if status == "открыт":
        sql = "select * from support.topic t WHERE status = 'открыт'"
        cursor = connection.cursor()  # курсор есть курсор

        cursor.execute(sql)  # выполение sql команды
        topic_table = cursor.fetchall()  # fetchall() это перевод обьекта в кортеж

        #for row in topic_table:
        #    print(row)

    connection.close()

    return render_template('index.html', topic_table=topic_table)


@app.route('/talk/<text>')
def talk(text):
    connection = connection_db.get_connection()  # основной коннект
    print("Соединие установлено ", connection)

    sql = "SELECT * FROM talk t WHERE t.topic_id ={}".format(text)
    cursor = connection.cursor()  # курсор есть курсор

    cursor.execute(sql)  # выполение sql команды
    talk_table = cursor.fetchall()  # fetchall() это перевод обьекта в кортеж

    where_name = cursor.execute('SELECT * FROM users_list WHERE topic_id=%s',(text))  # Поиск id отправителя. Нужно для запрета публикации топика
    print(where_name, '   where_name ')

    connection.close()

    return render_template('talk.html', talk_table=talk_table, text=text,where_name=where_name)  # f обязательно для позвращения переменной


file_name = ''


@app.route('/send_answer', methods=['POST'])
def send_answer():
    global file_name
    file_name = ''
    if request.method == 'POST':
        answer = request.form['answer']
        topic_id = request.form['topic_id']
        print(answer, topic_id)

        connection = connection_db.get_connection()  # основной коннект
        print("Соединие установлено ", connection)
        cursor = connection.cursor()  # курсор есть курсор

        cursor.execute('SELECT name FROM support.users_list WHERE topic_id = %s;',(topic_id))
        id_t = cursor.fetchall()[0]['name']
        print('id_t: ',id_t,type(id_t))

        #cursor.execute('SELECT chat_id FROM support.talk t WHERE topic_id = %s and chat_id != 1111',(topic_id)) # определение кому отправить сообщение
        #chat_id=cursor.fetchall()
        #print('chat_id: ',chat_id)
        #chat_id=chat_id[len(chat_id)-1]['chat_id']
        #send_message(chat_id, text=answer) #отправка сообщения в телеграмм
        send_message(id_t,text=answer)

        author = "admin"
        # date_time = "2021-08-30 14:26:00"
        today = datetime.datetime.today()
        date_time = today.strftime("%Y-%m-%d %H:%M:%S")  # 2017-04-05-00.18.00
        # answer = "fdfdfdf"

        #sql = 'INSERT INTO talk (topic_id, author, date_time, answer) VALUES(%s,%s,%s,%s)',(topic_id, author, date_time, answer)
        #cursor.execute('INSERT INTO talk (topic_id, author, date_time, answer,file_name) VALUES(%s,%s,%s,%s,%s)',(topic_id, author, date_time, answer,file_name))  # выполение sql команды
        #connection.commit()

        UPLOAD_FOLDER = 'static'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        f = request.files['file']
        print(f, '    f   ', type(f))
        if f:
            file_name = secure_filename(f.filename)
            if '.' not in file_name:
                print('Не загрузил. Кирилица в названии')
            else:
                #file_name=translit(file_name, "ru", reversed=True)
                print(translit(file_name, "ru", reversed=True))

                print(file_name, '- Название загружаемого файла1')
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                # ---------------переименование загруженного файла-----------------
                file_name_split = file_name.split('.')
                first_name_file = rename_random.random_file_name.generate_random_string(16)
                print(first_name_file, 'проба')
                os.rename('static/' + file_name, 'static/' + first_name_file + '.' + file_name_split[1])
                file_name = 'http://127.0.0.1:5000/static/' + first_name_file + '.' + file_name_split[1]
                print(first_name_file + '.' + file_name_split[1], '- Название переименованного файла')

                cursor.execute('INSERT INTO talk (topic_id, chat_id, author, date_time, answer,file_name) VALUES(%s,1111,%s,%s,%s,%s)',
                               (topic_id, author, date_time, answer, file_name))  # выполение sql команды
                connection.commit()

                #----отправака изображения в телегу--------------------------------------------------------------------------------------------
                bot_token1 = '1672815585:AAHEJXSAMuLcbLcVYdUjPaovSraZvZx5uNc'
                last_name=first_name_file + '.' + file_name_split[1]
                file1="static/"+first_name_file + '.' + file_name_split[1]
                files1 = {
                    'photo': open(file1, 'rb')
                }

                files2 = {
                    'document': open(file1, 'rb')
                }

                message1 = ('https://api.telegram.org/bot' + bot_token1 + '/sendPhoto?chat_id=' + str(id_t))
                message2 = ('https://api.telegram.org/bot' + bot_token1 + '/sendDocument?chat_id=' + str(id_t))
                #send = requests.post(message1, files=files1)
                send = requests.post(message2, files=files2)
                #--------------------------------------------------------------------------------------------------------------


        else:
            cursor.execute('INSERT INTO talk (topic_id, chat_id, author, date_time, answer,file_name) VALUES(%s,1111,%s,%s,%s,%s)',(topic_id,author, date_time, answer,file_name))  # выполение sql команды
            connection.commit()

        connection.close()

    return redirect('/talk/' + str(topic_id))

@app.route('/close_topic')
def close_topic():
    return render_template('close_topic.html')

@app.route('/close_topic1', methods=['POST'])
def close_topic1():
    if request.method == 'POST':
        password_close = request.form['password_close']
        topic_id = int(request.form['topic_id'])
        print(topic_id)
        if password_close=='111':
            connection = connection_db.get_connection()  # основной коннект
            print("Соединие установлено ", connection)
            cursor = connection.cursor()  # курсор есть курсор
            cursor.execute(('DELETE FROM support.users_list WHERE topic_id = %s'),(topic_id))
            connection.commit()#подтверждение изменений в базе
            print('топик удален')

            cursor.execute("UPDATE topic SET status = %s WHERE ID = %s", ('закрыт',topic_id ))
            connection.commit()
            connection.close()
        return render_template('close_topic.html')
    return render_template('close_topic.html')


name_file = ''

if __name__ == '__main__':
    # main()
    app.run()
