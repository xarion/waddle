import numpy
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

import settings


class ClassifierExecutor:
    def __init__(self, classifier):
        self.classifier = classifier

    def execute(self, training, test):
        self.classifier.fit(training['tfidfs'], training['document_labels'])
        predicted = self.classifier.predict(test['tfidfs'])
        return numpy.mean(predicted == test['document_labels'])


class DataVectorizer:
    def __init__(self, ngram_range=(1, 2)):
        self.vectorizer = CountVectorizer(min_df=1, ngram_range=ngram_range)
        self.tfidf_transformer = TfidfTransformer()

    def convert(self, training_docs, test_docs):
        training_corpus = self.__create_corpora__(training_docs)
        test_corpus = self.__create_corpora__(test_docs)

        training_corpus['tfidfs'] = self.tfidf_transformer.fit_transform(
                self.vectorizer.fit_transform(training_corpus['documents']))
        test_corpus['tfidfs'] = self.tfidf_transformer.transform(self.vectorizer.transform(test_corpus['documents']))
        return {"training": training_corpus, "test": test_corpus}

    def __create_corpora__(self, docs):
        documents = []
        document_labels = []
        for doc in docs:
            full_name = doc['place']['full_name']
            document_label_index = settings.locations[full_name]
            for tweet in doc['timeline']:
                documents.append(tweet['text'])
                document_labels.append(document_label_index)
        return {"document_labels": document_labels, "documents": documents}
