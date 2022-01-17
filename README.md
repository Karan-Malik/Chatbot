# Ted, The Deep-Learning Chatbot

## About this Project
Ted is a multipurpose chatbot made using Python3, who can chat with you and help in performing daily tasks. It uses NLP and Deep-Learning to analyse the user's message, classify it into the a broader category and then reply with a suitable message or the required information. It is hosted using flask and is available on heroku at the link specified above. 

First, the user message is lemmatized and pre-processed, before passing it to the deep-learning model used, an Artificial Neural Network with Softmax, to specify the query category which achieves an accuracy of **over 98%**.

## Project UI
Home Page:

![image](https://raw.githubusercontent.com/Karan-Malik/Chatbot/master/UI/main_screen.PNG?token=AKGUW5C2TMM37OQE5FSPXLS66D55O)

Chat Screen:

![image](https://raw.githubusercontent.com/Karan-Malik/Chatbot/master/UI/chat_screen.PNG?token=AKGUW5APXEVSAKONVS5IBS266D5ZA)

## Chatbot Features
Among other things, the bot can:
1. Chat with you
2. Help you with Google Search
3. Get the weather of any city
4. Get the top trending news in India at that moment
5. Get the top ten globally popular songs at that moment
6. Set a timer for you and so on

#### To check the complete list of capabilities and how to access them, type 'help' in the message box.

## Dataset
The dataset used for training was self-populated and is stored as Intents.json in chatbot_codes. The data from this file was used to create the pickle files for words and classes. The pre-trained model with weights is available as mymodel.h5 in the same file.

## How to Use on your System
You can chat with Ted at this [link](https://ted-the-deep-learning-bot.herokuapp.com/)

To run it locally on your system, follow these steps:
1. Clone this repository onto your system. On Command Prompt, run the following command:

```
git clone https://github.com/Karan-Malik/Chatbot.git
```
2. Change your directory to Chatbot:
```
cd Chatbot
```
3. Make sure you have all the required libraries listed in requirements.txt. In case any of the libraries are missing, install them using pip. Type this command into your Command Prompt, replacing 'Your-library-name' by the required library name:
```
pip install Your-library-name 
```
4. Then run the follwing commands to run the application:
```
set FLASK_APP=chatbot.py
flask run
```

5. Enter the url provided after running the previous commands into your web browser

Ted is now ready to chat!

#### I would like to thank [Ashutosh Varma](https://github.com/ashutoshvarma) and [Manorit Chawdhry](https://github.com/manorit2001) for their help and contribution to this project. Do check out their Github accounts!

##### Copyright (c) 2020 Karan-Malik

