import pandas as pd
import numpy as np

df = pd.read_csv("D:/Competitions_2020_2021/Apscript/task/balanced_reviews.csv")
# EDA Activities



print(df.shape)

(df.columns.tolist())

df['overall'].value_counts()

df.isnull().any(axis=0)

df.isnull().any(axis=1)

df[df.isnull().any(axis=1)].tail()

# handling the missing data
df.dropna(inplace=True)

df['overall'] == 3

df = df[df['overall'] != 3]

df['Positivity'] = np.where(df['overall'] > 3, 1, 0)


# TF_IDF (term frequency-inverse document frequency)


from sklearn.model_selection import train_test_split

features_train, features_test, labels_train, labels_test = train_test_split(df['reviewText'], df['Positivity'],
                                                                            random_state=42)

from sklearn.feature_extraction.text import TfidfVectorizer

vect = TfidfVectorizer(min_df=5).fit(features_train)

features_train_vectorized = vect.transform(features_train)

from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(features_train_vectorized, labels_train)

from sklearn.metrics import roc_auc_score

predictions = model.predict(vect.transform(features_test))

roc_auc_score(labels_test, predictions)

# Use pickle to save the model

# serialise
import pickle

pkl_filename = "pickle_model.pkl"

with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)


# deserialize
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)

# joblib module

import joblib

with open("joblib_model.pkl", 'wb') as file:
    joblib.dump(model, file)

# this code has to be executed on Sylvester mac
# deserialize
with open("joblib_model.pkl", 'rb') as file:
    joblib_model = joblib.load(file)

predictions = joblib_model.predict(vect.transform(features_test))

roc_auc_score(labels_test, predictions)

# pre trained
# textblob



from textblob import TextBlob

text_blob_object = TextBlob(df['reviewText'][350])

text_blob_object.sentiment











