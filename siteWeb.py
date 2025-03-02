from flask import Flask
app = Flask(__name__)

@app.route('/')
def welcome():
    return "Bienvenue sur mon site Web"

if __name__=='__main__':
    app.run()