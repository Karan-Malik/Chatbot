# BOT, The Deep-Learning Chatbot

## About this Project
Chatbot with predefined resources made in Python3, which can chat with you and perform some example tasks. It uses NLP to analyze the user's message, classify it into a category and then respond with a suitable message or necessary information. It is hosted on flask and is available on heroku at the link specified above.
## Project UI
Home Page:

![image](https://raw.githubusercontent.com/thiagootuler/chatbot/master/UI/chat_screen.PNG)

To run it locally on your system, follow these steps:
1. Clone this repository onto your system. On Command Prompt, run the following command:
```
git clone https://github.com/thiagootuler/chatbot.git
```
2. Go to the project directory and configure a virtual environment if you prefer.
3. Make sure you have all the required libraries listed in requirements.txt. In case any of the libraries are missing, install them using pip. Type this command into your Command Prompt:
```
pip install -r requirements.txt 
```
4. Additionally, install the dependencies used by the nltk library (nltk_requirements.txt), running the nltk_config.py script:
```
python3 nltk_config.py
```
5. Then, create an environment variables file (.env) based on the example file left and run the following commands to start the application:
```
python3 chatbot.py
```
6. Enter the url provided after running the previous commands into your web browser

BOT is now ready to chat!

NOTE: If the intentions file is changed, it is recommended to retrain the model. To do so, run the following command:
```
cd src/static/models && python3 training.py
```

##### Copyright (c) 2023 Thiago Tuler

