import os, os.path
import re

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV


from nltk.stem.porter import PorterStemmer
from nltk.corpus import brown
from nltk.corpus import stopwords


X = np.array([], dtype=object)
y = np.array([], dtype=object)

brown_categories = ['hobbies', 'news', 'government', 'reviews']

for brown_category in brown_categories:
  for fileid in brown.fileids(brown_category):
    doc = ''
    for w in brown.words(fileid):
      doc += '%s ' % w
    X = np.append(X, doc)
    y = np.append(y, brown_category)

    files_n = len([name for name in os.listdir('../%s' % brown_category)])
    for i in range(1, files_n + 1):
      file = open('../{}/{}_0{}.txt'.format(brown_category, brown_category, i))
      doc = file.read()
      X = np.append(X, doc)
      y = np.append(y, '%s' % brown_category)


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


stop = stopwords.words('english')
for i in range(len(X)):
  text = X[i]
  clean_text = ''
  for w in text.split():
    if w not in stop:
      clean_text += "%s " % w
  X[i] = clean_text


count_vec = CountVectorizer()

tfidf = TfidfTransformer()
np.set_printoptions(precision=3)
X_tfidf = tfidf.fit_transform(count_vec.fit_transform(X)).toarray()


X_train, X_test = X_tfidf[:140], X_tfidf[140:]
y_train, y_test = y[:140], y[140:]

classifier = LogisticRegression(penalty='l1', C=15.0, random_state=0)
classifier.fit_transform(X_train, y_train)
accuracy = classifier.score(X_test, y_test)