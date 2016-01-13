import random
import sys
from datetime import datetime
from time import sleep

from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegressionCV, SGDClassifier, Perceptron, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

import gcloud
from analysis.SKLearn import ClassifierExecutor, Corpus
from data.Execution import Execution

classifiers = [
    LogisticRegressionCV(),
    SGDClassifier(loss="hinge"),
    SGDClassifier(loss="log"),
    SGDClassifier(loss="modified_huber"),
    SGDClassifier(loss="squared_hinge"),
    SGDClassifier(loss="perceptron"),
    SGDClassifier(loss="squared_loss"),
    SGDClassifier(loss="huber"),
    SGDClassifier(loss="epsilon_insensitive"),
    SGDClassifier(loss="squared_epsilon_insensitive"),
    Perceptron(),
    PassiveAggressiveClassifier(loss="hinge"),
    PassiveAggressiveClassifier(loss="squared_hinge"),
    SVC(kernel='poly'),
    SVC(kernel='sigmoid'),
    LinearSVC(),
    KNeighborsClassifier(n_neighbors=8, weights="uniform"),
    KNeighborsClassifier(n_neighbors=8, weights="distance"),
    MultinomialNB(),
    BernoulliNB(),
    DecisionTreeClassifier(),
    AdaBoostClassifier(n_estimators=170),
]

classifier_names = [
    'LogisticRegressionCV()',
    'SGDClassifier(loss="hinge")',
    'SGDClassifier(loss="log")',
    'SGDClassifier(loss="modified_huber")',
    'SGDClassifier(loss="squared_hinge")',
    'SGDClassifier(loss="perceptron")',
    'SGDClassifier(loss="squared_loss")',
    'SGDClassifier(loss="huber")',
    'SGDClassifier(loss="epsilon_insensitive")',
    'SGDClassifier(loss="squared_epsilon_insensitive")',
    'Perceptron()',
    'PassiveAggressiveClassifier(loss="hinge")',
    'PassiveAggressiveClassifier(loss="squared_hinge")',
    'SVC(kernel="poly")',
    'SVC(kernel="sigmoid")',
    'LinearSVC()',
    'KNeighborsClassifier(n_neighbors=8, weights="uniform")',
    'KNeighborsClassifier(n_neighbors=8, weights="distance")',
    'MultinomialNB()',
    'BernoulliNB()',
    'DecisionTreeClassifier()',
    'AdaBoostClassifier(n_estimators=170)',
]

# array of tuples configuring, binary_classification, include_user_history, ngram parameters respectively
configurations = [
    (False, False, 1),
    (True, False, 1),
    (False, True, 1),
    (True, True, 1),
    (False, False, 2),
    (True, False, 2),
    (False, True, 2),
    (True, True, 2),
]


class Main:
    def __init__(self):
        self.instance_meta = {}
        self.execution = Execution()

    @staticmethod
    def create_corpus(configuration):
        return Corpus(binary_classification=configuration[0], include_user_history=configuration[1],
                      ngram=configuration[2])

    def start(self, classifier=None, configuration_id=0):
        if classifier is None:
            for index in range(0, len(classifiers)):
                self.run_classifier_with_id(index, configuration_id)
        elif classifier == "all-gcloud":
            sleep(random.random() * 10)  # instead of locking tables, this is much easier to avoid collusion
            self.instance_meta = gcloud.get_metadata()
            self.run_after_progress()
        else:
            self.run_classifier_with_id(int(classifier), int(configuration_id))

    def run_classifier_with_id(self, classifier_id, configuration_id):
        configuration = configurations[configuration_id]
        result = {"classifier": classifier_names[classifier_id], "classifier_id": classifier_id,
                  "configuration_id": configuration_id, "binary_classification": configuration[0],
                  "include_user_history": configuration[1], "ngram": configuration[2], "started_at": datetime.now(),
                  "meta": self.instance_meta}
        self.execution.write_progress(result)
        corpus = self.create_corpus(configuration)
        executor = ClassifierExecutor(classifiers[classifier_id], binary_classification=configuration[0])
        try:
            result['result'] = executor.execute(corpus.get_training(), corpus.get_test())
            print "%s\n%s" % (classifier_names[classifier_id], str(result["result"]))
        except Exception as e:
            print "%s: %s" % (classifier_names[classifier_id], e)
            result['exception'] = str(sys.exc_info())
        result['ended_at'] = datetime.now()
        result['execution_time'] = str(result['ended_at'] - result['started_at'])
        self.execution.write_execution_result(result)

    def run_after_progress(self):
        progress = self.execution.get_last_progress()
        if progress is None:
            self.run_classifier_with_id(0, 0)
            return self.run_after_progress()
        elif progress["configuration_id"] + 1 < len(configurations):
            self.run_classifier_with_id(progress["classifier_id"], progress["configuration_id"] + 1)
            return self.run_after_progress()
        elif progress["classifier_id"] + 1 < len(classifiers):
            self.run_classifier_with_id(progress["classifier_id"] + 1, 0)
            return self.run_after_progress()
        else:
            return 0


if __name__ == "__main__":
    m = Main()
    if len(sys.argv) > 2:
        m.start(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        m.start(sys.argv[1])
    else:
        m.start()
