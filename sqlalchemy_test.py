from flask import Flask, render_template, request,send_file, redirect, url_for, send_from_directory,session,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:GOGUDAserver123!@localhost/support'

db = SQLAlchemy(app)
#print(db)

class test_sqlalchemy(db.Model):
    id = db.Column(db.String(200), unique = True)
    email = db.Column(db.String(200), unique=True)

@app.route('/')
def index():
    #db.create_all()
    u = test_sqlalchemy(id="1",email="Первая")
    db.session.add(u)
    db.session.flush()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)