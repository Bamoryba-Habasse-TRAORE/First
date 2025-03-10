from flask import Flask
app= Flask(__name__)

@app.route('/')
def calcul(x):
    if type(x) == int :
        for i in range(1,x):
            x=i*x
    return x
@app.route("/")
def welcome():   
    return ("Hello World")

if __name__== (__main__)
    app.run()