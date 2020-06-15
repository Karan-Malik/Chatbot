# Ted, The Deep-Learning Chatbot

### Project website: [https://ted-the-deep-learning-bot.herokuapp.com/](https://ted-the-deep-learning-bot.herokuapp.com/)

## About this Project
This is a Multipurpose chatbot which can chat with you and help in performing common daily tasks. It uses NLP and Deep-Learning to analyse the user's message and classify it into the a broader category and then reply with a suitable message or information. It is hosted using flask and is available on heroku at the link specified above. 

First, the user message is lemmatized and pre-processed, before passing it to the deep-learning model used, an Artificial Neural Network with Softmax to specify the query category which achieves an accuracy of **over 98%**.

Among other things, the bot can:
1. Chat with you
2. Help you with Google Search
3. Tell the weather of any city
4. Get the top trending news in India at that moment
5. Get the top ten gloabally popular songs at that moment
6. Set a timer for you and so on

#### To check complete list of capabilities and how to access them, type 'help' in the message box.

## Dataset
The dataset used for self-populated and is stored as Intents.json in chatbot_codes. The data from this file was used to create the pickle files for words and classes. The pre-trained model with weights is available as mymodel.h5 in the same file.



