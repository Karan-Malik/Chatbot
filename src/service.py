import requests
import time
import nltk
import numpy as np
import pickle
import random
import tensorflow as tf

from pygame import mixer
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout

from src.config import Config
from src.repository import IntentRepository


class ModelService:
    # TODO: Melhorar comparacao:
    #       Transformar em caixa baixa e remover acentuacao e pontuacao antes de comparar
    #       O que fazer com palavras com muiplos generos (Obrigad(o))
    BASE_PATH = f'{Config.basedir}/src/static/models'

    def __init__(self):
        self.__lemmatizer = WordNetLemmatizer()
        self.__intent_repository = IntentRepository()
        try:
            self.__words, self.__classes, self.__model = self.load_files()
        except:
            self.training()
        finally:
            self.__words, self.__classes, self.__model = self.load_files()

    @property
    def lemmatizer(self):
        return self.__lemmatizer

    @property
    def intent_repository(self):
        return self.__intent_repository

    @property
    def words(self):
        return self.__words

    @property
    def classes(self):
        return self.__classes

    @property
    def model(self):
        return self.__model

    def set_words(self, words):
        pickle.dump(words, open(f'{self.BASE_PATH}/words.pkl', 'wb'))

    def set_classes(self, classes):
        pickle.dump(classes, open(f'{self.BASE_PATH}/classes.pkl', 'wb'))

    def set_model(self, model, hist):
        model.save(f'{self.BASE_PATH}/model.h5', hist)

    def load_files(self):
        words = pickle.load(open(f'{self.BASE_PATH}/words.pkl', 'rb'))
        classes = pickle.load(open(f'{self.BASE_PATH}/classes.pkl', 'rb'))
        model = load_model(f'{self.BASE_PATH}/model.h5')
        return words, classes, model

    def training(self):
        # TODO: Criar uma rota de traino, além de chama-la caso nao exista os arquivos de modelo
        ignored_tokens = ['?', '!', ',']

        words = []
        classes = []
        documents = []
        model = Sequential()

        intent_list = self.intent_repository.find_all_intents()
        for intent in intent_list:
            for pattern in intent['patterns']:
                pattern_tokens = nltk.word_tokenize(pattern)
                words.extend(pattern_tokens)
                documents.append((pattern_tokens, intent['tag']))
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        words = [
            self.lemmatizer.lemmatize(word.lower()) for word in words if word not in ignored_tokens
        ]
        words = sorted(list(set(words)))
        classes = sorted(list(set(classes)))
        print(len(documents), "documents")
        print(len(classes), "classes", classes)
        print(len(words), "unique lemmatized words", words)
        self.set_words(words)
        self.set_classes(classes)

        # create our training data
        training = []
        # create an empty array for our output
        output_empty = [0] * len(classes)
        # training set, bag of words for each sentence
        for doc in documents:
            # initialize our bag of words
            bow = []
            # list of tokenized words for the pattern
            sentence_words = doc[0]
            # lemmatize each word - create base word, in attempt to represent related words
            sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
            # create our bag of words arrays with 1, if word match found in current pattern
            for word in words:
                bow.append(1) if word in sentence_words else bow.append(0)
            # output is a '0' for each tag and '1' for current tag (for each pattern)
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
            training.append([bow, output_row])
        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training, dtype=object)
        # create train and test lists. X - patterns, Y - intents
        train_x = list(training[:, 0])
        train_y = list(training[:, 1])
        print("Training data created")

        # Create model
        # - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
        # equal to number of intents to predict output intent with softmax
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compile model.
        #   Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
        # adam = tf.keras.optimizers.legacy.Adam(0.001)
        sgd = tf.keras.optimizers.legacy.SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=['accuracy'])

        # fitting and saving the model.
        # model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=10, verbose=1)
        # hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=10, verbose=1)
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        self.set_model(model, hist)

        print("model created")

    def clean_up_sentence(self, sentence):
        sentence_tokens = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(token.lower()) for token in sentence_tokens]
        return sentence_words

    def create_sentence_embedding(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bow = list(np.zeros(len(self.words)))
        for word_of_sentence in sentence_words:
            for index, word in enumerate(self.words):
                if word == word_of_sentence:
                    bow[index] = 1
        return np.array(bow)

    def predict_intent(self, sentence, threshold=0.8):
        sentence_embedding = self.create_sentence_embedding(sentence)
        prediction = self.model.predict(np.array([sentence_embedding]))[0]
        results = [[index, value] for index, value in enumerate(prediction) if value > threshold]
        results.sort(key=lambda x: x[1], reverse=True)
        intent_list = []
        for result in results:
            intent_list.append({'intent': self.classes[result[0]], 'prob': str(result[1])})
        return intent_list


class ChatService:
    def __init__(self):
        self.__intent_repository = IntentRepository()
        self.__model_service = ModelService()

    @staticmethod
    def get_parameter(text):
        return text.split(':')[1].strip()

    def set_options(self):
        context_list = self.__intent_repository.find_all_intent_contexts_group_by_intent()
        btn_list = [f'\n<{context}>' for context in context_list]
        feature_list = ' '.join(btn_list)
        return f'Sou um chatbot com funcões predefinidas. Minhas capacidades são: {feature_list}'

    def set_weather(self, text):
        city = self.get_parameter(text)
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
            return f'Não consegui encontrar informações do tempo em {city}'
        weather_forecast = result.json()
        temp = weather_forecast['main']['temp']
        cond = weather_forecast['weather'][0]['description']
        return f'A temperatura em {city} é de {temp}C e o tempo está com {cond}'

    def set_timer(self, text):
        mixer.init()
        seconds = self.get_parameter(text)
        time.sleep(int(seconds))
        mixer.music.load(f'{Config.basedir}/src/static/assets/Handbell-ringing-sound-effect.mp3')
        mixer.music.play()
        return 'Fim do temporizador!'

    def set_search(self, text):
        query = self.get_parameter(text)
        search = f'https://www.google.com/search?q={query}'
        command = {'name': 'redirect', 'param': [search]}
        result = 'Redirecionando para o Google...'
        return command, result

    def switch_feature(self, tag, text):
        command = {}
        result = None
        if tag == 'options':
            result = self.set_options()
        if tag == 'weather':
            result = self.set_weather(text)
        if tag == 'timer':
            result = self.set_timer(text)
        if tag == 'search':
            command, result = self.set_search(text)
        return command, result

    def get_response(self, text):
        tag_list = self.__model_service.predict_intent(text)
        if len(tag_list) == 0:
            tag = 'noanswer'
        else:
            tag = tag_list[0]['intent']
        command, result = self.switch_feature(tag, text)
        if result is None:
            result = self.__intent_repository.find_one_intent_response_by_tag_order_by_random(tag)
        return {'tag': tag, 'message': result, 'command': command}
