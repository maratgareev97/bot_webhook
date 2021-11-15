from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('333.html')

@app.route('/otvet', methods=['POST'])
def otvet():
    if request.method == 'POST':
        st=request.form['st1']
        for i in range(len(st), 0, -1):
            if 'C' * i in st:
                answer=i
                print(i)
                break

    return render_template('333.html',answer=answer)

if __name__ == '__main__':
    app.run()
