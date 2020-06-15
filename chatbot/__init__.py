import flask
from flask import Flask
from chatbotconfig import Config
from shelljob import proc

app=Flask(__name__)
app.config.from_object  (Config)

import keras
import nltk
import pickle
import json
import numpy as np
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,Activation
import random
import keyboard
import datetime

from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()

model=load_model('chatbot_codes/mymodel.h5')
intents = json.loads(open('chatbot_codes/intents.json').read())
words = pickle.load(open('chatbot_codes/words.pkl','rb'))
classes = pickle.load(open('chatbot_codes/classes.pkl','rb'))


from chatbot import routes
