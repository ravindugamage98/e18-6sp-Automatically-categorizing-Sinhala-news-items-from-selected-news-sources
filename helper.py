import numpy as np
import pandas as pd
import re
import string
import pickle

from nltk.stem import PorterStemmer
ps = PorterStemmer()

#load model
with open('static/model/model.pickle', 'rb') as f:
    model = pickle.load(f)

#load stopwords
with open('static/model/corpora/stopwords/sinhala', 'r', encoding='utf-8') as file:
    sw = file.read().splitlines()

#load tokens
vocab = pd.read_csv('static/model/vocabulary.txt', header=None)
tokens = vocab[0].tolist() 

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def preprocessing(text):
    data = pd.DataFrame([text], columns=['Title'])
    data["Title"] = data["Title"].apply(lambda x: " ".join(x.lower() for x in x.split()))
    data["Title"] = data['Title'].apply(lambda x: " ".join(re.sub(r'^https?:\/\/.*[\r\n]*', '', x, flags=re.MULTILINE) for x in x.split()))
    data["Title"] = data["Title"].apply(remove_punctuations)
    data["Title"] = data['Title'].str.replace('\d+', '', regex=True)
    data["Title"] = data["Title"].apply(lambda x: " ".join(x for x in x.split() if x not in sw))
    data["Title"] = data["Title"].apply(lambda x: " ".join(ps.stem(x) for x in x.split()))
    return data["Title"]

def vectorizer(ds):
    vectorized_lst = []
    for sentence in ds:
        sentence_lst = np.zeros(len(tokens))
        for i in range(len(tokens)):
            if tokens[i] in sentence.split():
                sentence_lst[i] = 1     
        vectorized_lst.append(sentence_lst)  
    vectorized_lst_new = np.asarray(vectorized_lst, dtype=np.float32)
    return vectorized_lst_new

def get_prediction(vectorized_text):
    prediction = model.predict(vectorized_text)
    # prediction = new_model.predict(vectorized_text)
    if prediction == 0:
        return 'International'
    elif prediction == 1:
        return 'Sport'
    elif prediction == 2:
        return 'Business'
