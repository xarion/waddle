import numpy
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from settings import locations
from data.Data import Data


class ClassifierExecutor:
    def __init__(self, classifier, binary_classification=False):
        self.classifier = classifier
        self.binary_classification = binary_classification

    def execute(self, training, test):
        self.classifier.fit(training['tfidfs'], training['document_labels'])
        predicted = self.classifier.predict(test['tfidfs'])
        result = {"precision": numpy.mean(predicted == test['document_labels']), "predicted": {}, "actual": {}}

        for location in locations.keys():
            result["predicted"][location] = numpy.count_nonzero(predicted == locations[location])
            result["actual"][location] = numpy.count_nonzero(test['document_labels'] == locations[location])
        return result


class DataVectorizer:
    def __init__(self, ngram_range=(1, 2), binary_classification=False):
        self.vectorizer = CountVectorizer(min_df=1, ngram_range=ngram_range)
        self.tfidf_transformer = TfidfTransformer()
        self.binary_classification = binary_classification

    def convert(self, training_docs, test_docs):
        training_corpus = self.__create_corpus__(training_docs)
        test_corpus = self.__create_corpus__(test_docs)

        training_corpus['tfidfs'] = self.tfidf_transformer.fit_transform(
                self.vectorizer.fit_transform(training_corpus['documents']))
        test_corpus['tfidfs'] = self.tfidf_transformer.transform(self.vectorizer.transform(test_corpus['documents']))
        return {"training": training_corpus, "test": test_corpus}

    @staticmethod
    def __create_corpus__(docs):
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


class Corpus:
    def __init__(self, binary_classification=False):
        self.underlying = None
        self.initialized = False
        self.binary_classification = binary_classification

    def get(self):
        if not self.initialized:
            data = Data()
            vectorizer = DataVectorizer(binary_classification=self.binary_classification)
            self.underlying = vectorizer.convert(data.get_training_data(), data.get_test_data())
            self.initialized = True
        return self.underlying

    def get_training(self):
        return self.get()["training"]

    def get_test(self):
        return self.get()["test"]
