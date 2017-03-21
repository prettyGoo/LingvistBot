import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer


from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

import numpy as np
import numpy.random as nprand
import os, os.path

import nltk
from nltk.classify import apply_features
from nltk.stem.porter import PorterStemmer
from nltk.corpus import brown
from nltk.corpus import stopwords



def tokenizer_porter(text):
  return [porter.stem(word) for word in text.split()]


def tokenizer(text):
  return text.split()

porter = PorterStemmer()
stop = stopwords.words('english')

X = np.array([], dtype=object)
y = np.array([])

categories = ['hobbies', 'news', 'government', 'reviews']

for category in categories:
  for fileid in brown.fileids(category):
    doc = ''
    for w in brown.words(fileid):
      doc += '%s ' % w
    # x = np.append(x, brown.words(fileid))
    X = np.append(X, doc)
    y = np.append(y, category)

# # X = np.array(x ,dtype=object)
# print(x)


# Cleaning text data
for i in range(len(X)):
  string = X[i]
  string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
  string = re.sub(r"\'s", " \'s", string)
  string = re.sub(r"\'ve", " \'ve", string)
  string = re.sub(r"n\'t", " n\'t", string)
  string = re.sub(r"\'re", " \'re", string)
  string = re.sub(r"\'d", " \'d", string)
  string = re.sub(r"\'ll", " \'ll", string)
  string = re.sub(r",", " , ", string)
  string = re.sub(r"!", " ! ", string)
  string = re.sub(r"\(", " \( ", string)
  string = re.sub(r"\)", " \) ", string)
  string = re.sub(r"\?", " \? ", string)
  string = re.sub(r"\s{2,}", " ", string)
  X[i] = string

X_train, X_test = X[:100], X[100:]
y_train, y_test = y[:100], y[100:]
tfidf = TfidfVectorizer(strip_accents=None, lowercase=False, preprocessor=None)
param_grid = [{'vect__ngram_range': [(1,1)],
                'vect__stop_words': [stop, None],
                'vect__tokenizer': [tokenizer, tokenizer_porter],
                'clf__penalty': ['l1', 'l2'],
                'clf__C': [1.0, 10.0]},
               {'vect__ngram_range': [(1,1)],
                'vect__stop_words': [stop, None],
                'vect__tokenizer': [tokenizer, tokenizer_porter],
                'vect__use_idf':[False],
                'vect__norm':[None],
                'clf__penalty': ['l1', 'l2'],
                'clf__C': [1.0, 10.0]}]


lr_tfidf = Pipeline([('vect', tfidf), ('clf', LogisticRegression(random_state=0))])
gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid, scoring='accuracy', cv=5, verbose=1, n_jobs=-1)
print(gs_lr_tfidf.fit(X_train, y_train))
print(gs_lr_tfidf.best_params_)
print(gs_lr_tfidf.best_score_)
print(gs_lr_tfidf.best_estimator_)


result = gs_lr_tfidf.best_estimator_.score(X_test, y_test)
print(result)


# for i in range(len(X)):
#   string = [porter.stem(word) for word in X[i].split()]
#   X[i] = string
#

# Transform words into feature vector
# count_vec = CountVectorizer()
# bag = count_vec.fit_transform(X)
#
# tfidf = TfidfTransformer()
# np.set_printoptions(precision=2)
# tfidf_docs = tfidf.fit_transform(count_vec.fit_transform(X)).toarray()
# print(len(tfidf_docs))