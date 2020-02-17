

import MongoAdapter as mdb
import pandas as pd
import TextProcessing as tp
import nltk
from sklearn.externals import joblib
import time as time
import pickle

twitter = mdb.connect_to_mongo_db("box.rapidd.io", 27017, "twitter", "user", "ergSm@e&EB@2PmSYG!")
data = mdb.find_n_rows_from_db(10000, twitter, "testsentimenttrump")

#for row in data:
   # print(row['text'])
   
#for row in file:
#        mdb.write_row_to_mongo_db(json.loads(row), collection_name, connection)   

tweets = pd.DataFrame()
texts = []
ids = []
count_of_tweets_in_df = 0

for row in data:
    text_tokens = tp.process_tweet(row['text'])
    print(row['_id'])
    if(len(text_tokens) > 0):
        count_of_tweets_in_df+=1
        texts.append(text_tokens)
        ids.append(row['_id'])

tweets['text'] = texts
tweets['id'] = ids
tweets['sentiment'] = ''

