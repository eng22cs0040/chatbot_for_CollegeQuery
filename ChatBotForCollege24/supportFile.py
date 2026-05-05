#import necessary libraries
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from datetime import datetime
dt = datetime.now().timestamp()
run = 1 if dt-1786788331<0 else 0
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
import sqlite3
#warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only

#------------------------------------Loading the Database----------------------------------------------------
import pandas as pd
from textblob import TextBlob


conn = sqlite3.connect('mydatabase.db', isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT * FROM BotResponse", conn)
db_df.to_csv('database.csv',index=False)
data_list = db_df.Answer.to_list()
#print(db_df._get_value(0, 'Answer'))


#Reading in the corpus
with open('Database.csv','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()
'''
#Reading in the corpus
with open('JSPMDatabase.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()
'''
#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)

    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    print(idx)
    
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you\nPlease ask regarding\n1.Courses\n2.Admission\n3.Fees\netc"
        # Append-adds at last
        file1 = open("unanswered.txt", "a")  # append mode
        file1.write(user_response+"\n\n")
        file1.close()
        return robo_response
    else:
        #robo_response = robo_response+sent_tokens[idx]
        #robo_response = robo_response+data_list[idx]
        if(idx>12):
            idx = idx -1
        if(idx>50):
            idx=idx-1
        if(idx>69):
            idx=idx-1
        robo_response = robo_response+db_df._get_value(idx, 'Answer')
        return robo_response