#open windows cmd(command prompt) and type following command

#pip install numpy scikit-learn db-sqlite3 nltk pandas textblob

#import necessary libraries
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
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


conn = sqlite3.connect('mydatabase1.db', isolation_level=None,
                       detect_types=sqlite3.PARSE_COLNAMES)
db_df = pd.read_sql_query("SELECT * FROM BotResponse", conn)
db_df.to_csv('database1.csv',index=False)
data_list = db_df.Ans.to_list()
#print(db_df._get_value(0, 'Answer'))


#Reading in the corpus
with open('Database1.csv','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

print(raw)