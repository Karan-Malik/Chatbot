from json import dumps

from flask import Flask, redirect
from flask import render_template, request

from src.service import response
from src.config import Config

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/chat')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    config = {
        'bot': Config.bot,
        'constructor': Config.constructor,
        'homepage': Config.homepage,
        'contact': Config.contact,
        'age': Config.age
    }
    return render_template('index.html', config=config)


@app.route("/message", methods=['POST'])
def message():
    req_data = request.json
    req_message = req_data['message']
    resp = response(req_message)
    dumps(resp, ensure_ascii=False)
    return resp


app.run(debug=True)
