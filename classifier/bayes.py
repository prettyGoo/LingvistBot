import numpy.random as nprand
import os, os.path

import nltk
from nltk.classify import apply_features
from nltk.corpus import brown


class Bayes(object):

    def __init__(self):
        print('Start init bayes')
        self.docs = self.construct_docs()  # ([word,], label)
        nprand.shuffle(self.docs)

        brown_words = brown.words()
        news_words = []#self.extract_words_from_files('news')
        reviews_words = self.extract_words_from_files('reviews')
        government_words = self.extract_words_from_files('government')
        hobbies_words = self.extract_words_from_files('hobbies')

        freq_words = nltk.FreqDist(w.lower() for w in brown_words + news_words + reviews_words + government_words + hobbies_words)
        all_words = [w for w in freq_words if len(w) > 4 and freq_words[w] > 5]
        print(len(all_words))

        self.word_features = list(all_words)[:2500]
        featuresets = apply_features(self.document_features, self.docs, labeled=True)
        print(len(featuresets))
        self.train_set, self.test_set = featuresets[70:], featuresets[:70]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        print('End init bayes')

    def construct_docs(self):
        docs = []
        brown_categories = ['hobbies', 'news', 'government', 'reviews']
        for brown_category in brown_categories:
            for fileid in brown.fileids(brown_category):
                docs.append((list(brown.words(fileid)), brown_category))

            files_n = len([name for name in os.listdir('./%s' % brown_category)])
            for i in range(1, files_n + 1):
                file = open('{}/{}_0{}.txt'.format(brown_category, brown_category, i))
                words = file.read().replace('\n', ' ').split(' ')
                docs.append((list(words), '%s' % brown_category))

        # my_categories = ['hobbies', 'news', 'government', 'reviews']
        return docs

    def shuffle_docs(self):
        nprand.shuffle(self.docs)

    def document_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features['{}'.format(word)] = (word in document_words)
        return features

    def extract_words_from_files(self, category):
        words_to_return = []
        files_n = len([name for name in os.listdir('./%s' % category)])
        for i in range(1, files_n + 1):
            file = open('{}/{}_0{}.txt'.format(category, category, i))
            words = file.read().replace('\n', ' ').split(' ')
            for w in words:
                words_to_return.append(w)
        return words_to_return

    def get_accuracy(self):
        return nltk.classify.accuracy(self.classifier, self.test_set)

    def classify(self, features):
        return self.classifier.classify(features)

    def train(self, text, label):
        words = text.replace('\n', ' ').replace(',', '').replace('.', '').split(' ')
        doc = (list(words), label)
        train_set = apply_features(self.document_features, doc, labeled=True)
        print(train_set)
        self.classifier.train(train_set)
