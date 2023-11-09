import nltk

from src.config import Config

nltk_requirements = open(f'{Config.basedir}/nltk_requirements.txt').read()
complement_list = nltk_requirements.split('\n')
for complement in complement_list:
    nltk.download(complement)
