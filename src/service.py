import random
import requests
import time
import nltk
import numpy as np
import pickle

from json import loads
from pygame import mixer
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

from src.config import Config


intents = loads(
    open(f'{Config.basedir}/src/static/models/intents.json').read()
    .replace('BOT', Config.bot)
    .replace('CONSTRUCTOR', Config.constructor)
    .replace('HOMEPAGE', Config.homepage)
    .replace('CONTACT', Config.contact)
    .replace('AGE', Config.age)
)
words = pickle.load(open(f'{Config.basedir}/src/static/models/words.pkl', 'rb'))
model = load_model(f'{Config.basedir}/src/static/models/model.h5')
classes = pickle.load(open(f'{Config.basedir}/src/static/models/classes.pkl', 'rb'))

lemmatizer = WordNetLemmatizer()


#TODO: Criar classes para separar o que é predicao, utils e conversacao
def clean_up(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def create_bow(sentence):
    sentence_words = clean_up(sentence)
    bag = list(np.zeros(len(words)))
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)


def predict_intent(sentence):
    p = create_bow(sentence)
    res = model.predict(np.array([p]))[0]
    threshold = 0.8
    results = [[i, r] for i, r in enumerate(res) if r > threshold]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for result in results:
        return_list.append({'intent': classes[result[0]], 'prob': str(result[1])})
    return return_list


def get_parameter(text):
    return text.split(':')[1].strip()


def get_response(return_list, intents_json, text):
    result = None
    command = {}
    if len(return_list) == 0:
        tag = 'noanswer'
    else:
        tag = return_list[0]['intent']
    if tag == 'options':
        context_list = [intent['context'] for intent in intents['intents'] if 'context' in intent]
        btn_list = [f'\n<{context}>' for context in context_list]
        feature_list = ' '.join(btn_list)
        result = f'Sou um chatbot com funcões predefinidas. Minhas capacidades são: {feature_list}'
    if tag == 'weather':
        city = get_parameter(text)
        result = requests.get(
            Config.weather_url,
            params={
                "q": "{},{}".format(city, 'br'),
                "appid": Config.weather_key,
                "units": "metric",
                "lang": "pt_br"
            }
        )
        if result.status_code != 200:
            result = f'Não consegui encontrar informações do tempo em {city}'
        weather_forecast = result.json()
        temp = weather_forecast['main']['temp']
        cond = weather_forecast['weather'][0]['description']
        result = f'A temperatura em {city} é de {temp}C e o tempo está com {cond}'
    if tag == 'timer':
        mixer.init()
        seconds = get_parameter(text)
        time.sleep(int(seconds))
        mixer.music.load(f'{Config.basedir}/src/static/assets/Handbell-ringing-sound-effect.mp3')
        mixer.music.play()
        result = 'Fim do temporizador!'
    if tag == 'search':
        query = get_parameter(text)
        search = f'https://www.google.com/search?q={query}'
        command = {'name': 'redirect', 'param': [search]}
        result = 'Redirecionando para o Google...'
    if result is None:
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if tag == i['tag']:
                result = random.choice(i['responses'])
    return {'message': result, 'tag': tag, 'command': command}


def response(text):
    return_list = predict_intent(text)
    return get_response(return_list, intents, text)
