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

        # brown_words = nltk.FreqDist(w.lower() for w in brown.words())
        # news_words = nltk.FreqDist(w.lower() for w in self.news_words())
        # music_words = nltk.FreqDist(w.lower() for w in self.music_words())
        brown_words = brown.words()
        news_words = []#self.news_words()
        reviews_words = self.reviews_words()
        government_words = self.government_words()

        freq_words = nltk.FreqDist(w.lower() for w in brown_words + news_words + reviews_words + government_words)
        all_words = [w for w in freq_words if len(w) > 4 and freq_words[w] > 5]
        print(len(all_words))

        self.word_features = list(all_words)[:2500]
        featuresets = apply_features(self.document_features, self.docs, labeled=True)
        self.train_set, self.test_set = featuresets[70:], featuresets[:70]
        self.classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        print('End init bayes')

    def construct_docs(self):
        docs = []
        categories = ['hobbies', 'news', 'government', 'reviews']
        for category in categories:
            for fileid in brown.fileids(category):
                docs.append((list(brown.words(fileid)), category))

        # for i in range(1, 8):
        #     file = open('news/news_0{}.txt'.format(i))
        #     words = file.read().replace('\n', ' ').split(' ')
        #     docs.append((list(words), 'news'))

        files_n = len([name for name in os.listdir('./reviews')])
        for i in range(1, files_n + 1):
            file = open('reviews/reviews_0%s.txt' % i)
            words = file.read().replace('\n', ' ').split(' ')
            docs.append((list(words), 'reviews'))

        files_n = len([name for name in os.listdir('./government')])
        for i in range(1, files_n + 1):
            file = open('government/government_0%s.txt' % i)
            words = file.read().replace('\n', ' ').split(' ')
            docs.append((list(words), 'government'))

        return docs

    def shuffle_docs(self):
        nprand.shuffle(self.docs)

    def document_features(self, document):
        document_words = set(document)
        features = {}
        for word in self.word_features:
            features['{}'.format(word)] = (word in document_words)
        return features

    def news_words(self):
        words_to_return = []
        files_n = len([name for name in os.listdir('./news')])
        for i in range(1, files_n + 1):
            file = open('news/news_0%s.txt' % i)
            words = file.read().replace('\n', ' ').split(' ')
            for w in words:
                words_to_return.append(w)
        return words_to_return

    def reviews_words(self):
        words_to_return = []
        files_n = len([name for name in os.listdir('./reviews')])
        for i in range(1, files_n + 1):
            file = open('reviews/reviews_0%s.txt' % i)
            words = file.read().replace('\n', ' ').split(' ')
            for w in words:
                words_to_return.append(w)
        return words_to_return

    def government_words(self):
        words_to_return = []
        files_n = len([name for name in os.listdir('./government')])
        for i in range(1, files_n + 1):
            file = open('government/government_0%s.txt' % i)
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
