from flask import Flask,render_template

app=Flask(__name__)
                                                                      
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')
@app.route('/welcome_back')
def afterlog():
    return render_template('afterlog.html')

@app.route('/calender.html')
def calender():
    return render_template('calender.html')

if __name__=='__main__':
    app.run(debug=True)