import sys
from datetime import datetime

from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import LogisticRegressionCV, SGDClassifier, RidgeCV, LinearRegression, LassoCV, ElasticNetCV, \
    Perceptron, PassiveAggressiveClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
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

execution = Execution()
instance_meta = {}


def create_corpus(configuration):
    return Corpus(binary_classification=configuration[0], include_user_history=configuration[1],
                  ngram=configuration[2])


def main(classifier=None, configuration_id=0):
    if classifier is None:
        for index in range(0, len(classifiers)):
            run_classifier_with_id(index, configuration_id)
    elif classifier == "all-gcloud":
        super.instance_meta = gcloud.get_metadata()
        run_after_progress()
    else:
        run_classifier_with_id(int(classifier), configuration_id)


def run_classifier_with_id(classifier_id, configuration_id):
    configuration = configurations[configuration_id]
    result = {"classifier": classifier_names[classifier_id], "classifier_id": classifier_id,
              "configuration_id": configuration_id, "binary_classification": configuration[0],
              "include_user_history": configuration[1], "ngram": configuration[2], "started_at": datetime.now(),
              "meta": instance_meta}
    execution.write_progress(result)
    corpus = create_corpus(configuration)
    executor = ClassifierExecutor(classifiers[classifier_id], binary_classification=configuration[0])
    try:
        result['result'] = executor.execute(corpus.get_training(), corpus.get_test())
        print "%s\n%s" % (classifier_names[classifier_id], str(result["result"]))
    except Exception as e:
        print "%s: %s" % (classifier_names[classifier_id], e)
        result['exception'] = str(sys.exc_info())
    result['ended_at'] = datetime.now()
    result['execution_time'] = str(result['ended_at'] - result['started_at'])
    execution.write_execution_result(result)


def run_after_progress():
    progress = execution.get_last_progress()
    if progress is None:
        run_classifier_with_id(0, 0)
        return run_after_progress()
    elif progress["configuration_id"] + 1 < len(configurations):
        run_classifier_with_id(progress["classifier_id"], progress["configuration_id"] + 1)
    elif progress["classifier_id"] + 1 < len(classifiers):
        run_classifier_with_id(progress["classifier_id"] + 1, 0)
        return run_after_progress()
    else:
        return 0


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
