from flask import Flask, render_template, request,send_file, redirect, url_for, send_from_directory,session,make_response
from flask_caching import Cache
import connection_db
from werkzeug.utils import secure_filename
import os, datetime
import rename_random

from pymemcache.client import base





app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
#cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
#cache = Cache(config={'CACHE_TYPE': 'filesystem', 'CACHE_DIR': '/tmp'})
#cache = Cache (config = {'CACHE_TYPE': 'redis'})
#cache.init_app(app)
#cache = base.Client(('127.0.0.1', 11211), timeout=60, connect_timeout=60)




@app.route('/')
def index():
    connection = connection_db.get_connection() # основной коннект
    print("Соединие установлено ", connection)

    sql = "SELECT * FROM topic"
    cursor = connection.cursor() # курсор есть курсор

    cursor.execute(sql) #выполение sql команды
    topic_table=cursor.fetchall() # fetchall() это перевод обьекта в кортеж

    for row in topic_table:
        print(row)

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

    connection.close()

    return render_template('talk.html',talk_table=talk_table,text=text) # f обязательно для позвращения переменной

file_name=''

@app.route('/send_answer', methods=['POST'])
def send_answer():
    global file_name
    file_name=''
    if request.method == 'POST':
        answer = request.form['answer']
        topic_id = request.form['topic_id']
        print(answer,topic_id)

        connection = connection_db.get_connection()  # основной коннект
        print("Соединие установлено ", connection)
        cursor = connection.cursor()  # курсор есть курсор

        author="admin"
        #date_time = "2021-08-30 14:26:00"
        today = datetime.datetime.today()
        date_time = today.strftime("%Y-%m-%d %H:%M:%S")  # 2017-04-05-00.18.00
        #answer = "fdfdfdf"

        #sql = 'INSERT INTO talk (topic_id, author, date_time, answer) VALUES(%s,%s,%s,%s)',(topic_id, author, date_time, answer)
        #cursor.execute('INSERT INTO talk (topic_id, author, date_time, answer,file) VALUES(%s,%s,%s,%s,%s)',(topic_id, author, date_time, answer))  # выполение sql команды
        #connection.commit()

        UPLOAD_FOLDER = 'static'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        f = request.files['file']
        print(f,'    f   ',type(f))
        if f:
            file_name = secure_filename(f.filename)
            print(file_name, '- Название загружаемого файла1')
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            # ---------------переименование загруженного файла-----------------
            file_name_split=file_name.split('.')
            first_name_file=rename_random.random_file_name.generate_random_string(16)
            print(first_name_file,'проба')
            os.rename('static/'+file_name, 'static/'+first_name_file+'.'+file_name_split[1])
            file_name = first_name_file+'.'+file_name_split[1]
            print(first_name_file+'.'+file_name_split[1], '- Название переименованного файла')

            # sql = 'INSERT INTO talk (topic_id, author, date_time, answer) VALUES(%s,%s,%s,%s)',(topic_id, author, date_time, answer)
        cursor.execute('INSERT INTO talk (topic_id, author, date_time, answer,file_name) VALUES(%s,%s,%s,%s,%s)',(topic_id, author, date_time, answer,file_name))  # выполение sql команды
        connection.commit()

        connection.close()

    return redirect('http://127.0.0.1:5000/talk/' + str(topic_id))


name_file=''
'''
@app.route('/downloa/')
def download_file():
    # path = "html2pdf.pdf"
    # path = "info.xlsx"
    global name_file
    #print(file_name,'file_name')
    #path = 'static/'+file_name
    print(name_file,'text1')
    #print(path,'11111111111111111111111111111111111111111111111111111',type(file_name),file_name)
    path1 = 'static/'+name_file
    print(path1,'-path')
    #app.secret_key='lkl'
    #session.clear()
    return send_file(path1)
    #return send_from_directory(directory='static',path='', filename=path1)

@app.route('/talk1/<text1>')
def talk1(text1):
    global name_file
    name_file=text1
    print('name_file: ', name_file)
    return redirect('/downloa')
'''
if __name__ == '__main__':
    app.run(debug=True)

