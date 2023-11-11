from json import dumps

from flask import Flask, redirect
from flask import render_template, request

from src.service import ChatService
from src.config import Config

app = Flask(__name__)
chat_service = ChatService()



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
    resp = chat_service.get_response(req_message)
    dumps(resp, ensure_ascii=False)
    return resp

#TODO: Add training endpoint
# @app.route("/training", methods=['POST'])
# def training():
#     pass


app.run(debug=True)
