import sys

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import precision_recall_fscore_support

from data.Data import Data
from helpers import Dictrement
from settings import locations


class ClassifierExecutor:
    def __init__(self, classifier, binary_classification=False):
        self.classifier = classifier
        self.binary_classification = binary_classification
        if binary_classification:
            self.labels = [0, 1]
        else:
            self.labels = locations.values()

    def execute(self, training, test):
        self.classifier.fit(training['tfidfs'], training['document_labels'])
        predicted = self.classifier.predict(test['tfidfs'])
        measures = precision_recall_fscore_support(predicted, test['document_labels'], labels=self.labels)
        return {"precision": map(str, measures[0]),  # why can't you encode these floats py/mongo?
                "recall": map(str, measures[1]),
                "f1score": map(str, measures[2]),
                "support": map(str, measures[3]),
                "labels": str(self.labels)}


class DataVectorizer:
    def __init__(self, ngram_range=(1, 2), binary_classification=False, include_user_history=True):
        self.vectorizer = CountVectorizer(min_df=1, ngram_range=ngram_range)
        self.tfidf_transformer = TfidfTransformer()
        self.binary_classification = binary_classification
        self.include_user_history = include_user_history

    def convert(self, training_docs, test_docs):
        training_corpus = self.normalise(self.__create_corpus__(training_docs))
        test_corpus = self.normalise(self.__create_corpus__(test_docs))
        print sum(training_corpus["document_labels"])
        print len(training_corpus["document_labels"])
        print sum(test_corpus["document_labels"])
        print len(test_corpus["document_labels"])
        training_corpus['tfidfs'] = self.tfidf_transformer.fit_transform(
                self.vectorizer.fit_transform(training_corpus['documents']))
        test_corpus['tfidfs'] = self.tfidf_transformer.transform(self.vectorizer.transform(test_corpus['documents']))
        return {"training": training_corpus, "test": test_corpus}

    def normalise(self, docs):
        normalised_docs = {"document_labels": [], "documents": []}
        if self.binary_classification:
            positives = sum(docs["document_labels"])
            negatives = len(docs["document_labels"]) - positives
            positive_count = 0
            negative_count = 0
            limit = positives if positives < negatives else negatives
            count = 0
            while positive_count < limit or negative_count < limit:
                label = docs["document_labels"][count]
                positive_count += label
                negative_count += not label
                if (label and positive_count < limit) or (not label and negative_count < limit):
                    normalised_docs["document_labels"].append(label)
                    normalised_docs["documents"].append(docs["documents"][count])
                count += 1
        else:
            location_counts = Dictrement()
            for label in docs["document_labels"]:
                location_counts.increment(label)
            limit = sys.maxint
            for label in location_counts.underlying.keys():
                if location_counts.get(label) < limit:
                    limit = location_counts.get(label)
            count = 0
            number_of_docs = len(docs["document_labels"])
            new_counts = Dictrement()
            while count < number_of_docs:
                label = docs["document_labels"][count]
                if new_counts.get(label) < limit:
                    normalised_docs["document_labels"].append(label)
                    normalised_docs["documents"].append(docs["documents"][count])
                    new_counts.increment(label)
                count += 1

        return normalised_docs

    def __create_corpus_from_history__(self, docs):
        documents = []
        document_labels = []
        for doc in docs:
            full_name = doc['place']['full_name']

            if self.binary_classification:
                document_label_index = full_name == "Manhattan, NY"
            else:
                document_label_index = locations[full_name]

            for tweet in doc['timeline']:
                documents.append(tweet['text'])
                document_labels.append(document_label_index)
        return {"document_labels": document_labels, "documents": documents}

    def __create_corpus_from_tweets__(self, docs):
        documents = []
        document_labels = []
        for doc in docs:
            full_name = doc['place']['full_name']

            if self.binary_classification:
                document_label_index = full_name == "Manhattan, NY"
            else:
                document_label_index = locations[full_name]

            documents.append(doc['text'])
            document_labels.append(document_label_index)
        return {"document_labels": document_labels, "documents": documents}

    def __create_corpus__(self, docs):
        if self.include_user_history:
            return self.__create_corpus_from_history__(docs)
        else:
            return self.__create_corpus_from_tweets__(docs)


class Corpus:
    def __init__(self, binary_classification=False, include_user_history=True):
        self.underlying = None
        self.initialized = False
        self.binary_classification = binary_classification
        self.include_user_history = include_user_history

    def get(self):
        if not self.initialized:
            data = Data(include_user_history=self.include_user_history)
            vectorizer = DataVectorizer(binary_classification=self.binary_classification,
                                        include_user_history=self.include_user_history)
            self.underlying = vectorizer.convert(data.get_training_data(), data.get_test_data())
            self.initialized = True
        return self.underlying

    def get_training(self):
        return self.get()["training"]

    def get_test(self):
        return self.get()["test"]
