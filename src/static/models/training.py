import json
import nltk
import pickle
import random
import numpy as np
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Dense, Dropout
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

#TODO: Incluir script no arquivo de service e criar uma rota de traino, 
#      além de chama-la caso nao exista os arquivos de modelo

words = []
classes = []
documents = []
ignore = ['?', '!', ',', "'s"]

data_file = open('intents.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        documents.append((w, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore]
words = sorted(list(set(words)))
classes = sorted(list(set(classes)))
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern = doc[0]
    pattern = [lemmatizer.lemmatize(word.lower()) for word in pattern]
    for word in words:
        if word in pattern:
            bag.append(1)
        else:
            bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)
X_train = list(training[:, 0])
y_train = list(training[:, 1])

# Model
model = Sequential()
model.add(Dense(128, activation='relu', input_shape=(len(X_train[0]),)))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(y_train[0]), activation='softmax'))

adam = tf.keras.optimizers.legacy.Adam(0.001)
model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(np.array(X_train), np.array(y_train), epochs=200, batch_size=10, verbose=1)
weights = model.fit(np.array(X_train), np.array(y_train), epochs=200, batch_size=10, verbose=1)
model.save('models.h5')

# Self learning
# print('Ajude-me a aprender?')
# tag = input('Por favor insira a categoria geral da sua pergunta ')
# flag = -1
# for i in range(len(intents['intents'])):
#     if tag.lower() in intents['intents'][i]['tag']:
#         intents['intents'][i]['patterns'].append(input('Digite sua mensagem: '))
#         intents['intents'][i]['responses'].append(input('Insira a resposta esperada: '))
#         flag = 1
# if flag == -1:
#     intents['intents'].append(
#         {'tag': tag,
#          'patterns': [input('Por favor insira a sua mensagem')],
#          'responses': [input('Insira a resposta esperada')]})
# with open('intents.json', 'w') as outfile:
#     outfile.write(json.dumps(intents, indent=4))
# TODO: Rodar treino para incluir informacoes add
