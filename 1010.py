from flask import Flask, render_template, request, redirect
import random
import time
random.seed(version=2)

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name1 = request.form['name']
        return redirect('/second')
    return render_template('1010.html')

@app.route('/second')
def index1():
    color=random.randint(0,16777215)
    col=hex(color)[2::]
    return render_template('1111.html', name2=col)


if __name__ == '__main__':
    # main()
    app.run()