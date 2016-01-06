import sys
from datetime import datetime

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import GradientBoostingClassifier, AdaBoostClassifier
from sklearn.gaussian_process import GaussianProcess
from sklearn.linear_model import LogisticRegressionCV, SGDClassifier, RidgeCV, LinearRegression, LassoCV, ElasticNetCV, \
    MultiTaskLassoCV, BayesianRidge, ARDRegression, Perceptron, PassiveAggressiveClassifier
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.neighbors import KNeighborsClassifier, RadiusNeighborsClassifier
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

import gcloud
from analysis.SKLearn import ClassifierExecutor, Corpus
from data.Execution import Execution

classifiers = [
    LinearRegression(),
    RidgeCV(alphas=[.1, .5, 1, 5, 10]),
    LassoCV(),
    ElasticNetCV(),
    MultiTaskLassoCV(),
    BayesianRidge(),
    ARDRegression(),
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
    LinearDiscriminantAnalysis(),
    LinearDiscriminantAnalysis(solver="lsqr"),
    LinearDiscriminantAnalysis(solver="eigen"),
    SVC(kernel='poly'),
    SVC(kernel='sigmoid'),
    SVC(kernel='precomputed'),
    NuSVC(),
    LinearSVC(),
    KNeighborsClassifier(n_neighbors=8, weights="uniform"),
    KNeighborsClassifier(n_neighbors=8, weights="distance"),
    RadiusNeighborsClassifier(weights="uniform"),
    RadiusNeighborsClassifier(weights="distance"),
    GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="absolute_exponential"),
    GaussianProcess(regr="constant", optimizer="Welch", corr="absolute_exponential"),
    GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="absolute_exponential"),
    GaussianProcess(regr="linear", optimizer="Welch", corr="absolute_exponential"),
    GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="absolute_exponential"),
    GaussianProcess(regr="quadratic", optimizer="Welch", corr="absolute_exponential"),
    GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="squared_exponential"),
    GaussianProcess(regr="constant", optimizer="Welch", corr="squared_exponential"),
    GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="squared_exponential"),
    GaussianProcess(regr="linear", optimizer="Welch", corr="squared_exponential"),
    GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="squared_exponential"),
    GaussianProcess(regr="quadratic", optimizer="Welch", corr="squared_exponential"),
    GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="generalized_exponential"),
    GaussianProcess(regr="constant", optimizer="Welch", corr="generalized_exponential"),
    GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="generalized_exponential"),
    GaussianProcess(regr="linear", optimizer="Welch", corr="generalized_exponential"),
    GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="generalized_exponential"),
    GaussianProcess(regr="quadratic", optimizer="Welch", corr="generalized_exponential"),
    GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="cubic"),
    GaussianProcess(regr="constant", optimizer="Welch", corr="cubic"),
    GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="cubic"),
    GaussianProcess(regr="linear", optimizer="Welch", corr="cubic"),
    GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="cubic"),
    GaussianProcess(regr="quadratic", optimizer="Welch", corr="cubic"),
    GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="linear"),
    GaussianProcess(regr="constant", optimizer="Welch", corr="linear"),
    GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="linear"),
    GaussianProcess(regr="linear", optimizer="Welch", corr="linear"),
    GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="linear"),
    GaussianProcess(regr="quadratic", optimizer="Welch", corr="linear"),
    GaussianNB(), MultinomialNB(), BernoulliNB(),
    DecisionTreeClassifier(),
    GradientBoostingClassifier(n_estimators=150, learning_rate=1.0, max_depth=1, random_state=0),
    AdaBoostClassifier(n_estimators=150),
]

classifier_names = [
    'LinearRegression()',
    'RidgeCV(alphas=[.1, .5, 1, 5, 10])',
    'LassoCV()',
    'ElasticNetCV()',
    'MultiTaskLassoCV()',
    'BayesianRidge()',
    'ARDRegression()',
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
    'LinearDiscriminantAnalysis()',
    'LinearDiscriminantAnalysis(solver="lsqr")',
    'LinearDiscriminantAnalysis(solver="eigen")',
    'SVC(kernel="poly")',
    'SVC(kernel="sigmoid")',
    'SVC(kernel="precomputed")',
    'NuSVC()',
    'LinearSVC()',
    'KNeighborsClassifier(n_neighbors=8, weights="uniform")',
    'KNeighborsClassifier(n_neighbors=8, weights="distance")',
    'RadiusNeighborsClassifier(weights="uniform")',
    'RadiusNeighborsClassifier(weights="distance")',
    'GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="absolute_exponential")',
    'GaussianProcess(regr="constant", optimizer="Welch", corr="absolute_exponential")',
    'GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="absolute_exponential")',
    'GaussianProcess(regr="linear", optimizer="Welch", corr="absolute_exponential")',
    'GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="absolute_exponential")',
    'GaussianProcess(regr="quadratic", optimizer="Welch", corr="absolute_exponential")',
    'GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="squared_exponential")',
    'GaussianProcess(regr="constant", optimizer="Welch", corr="squared_exponential")',
    'GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="squared_exponential")',
    'GaussianProcess(regr="linear", optimizer="Welch", corr="squared_exponential")',
    'GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="squared_exponential")',
    'GaussianProcess(regr="quadratic", optimizer="Welch", corr="squared_exponential")',
    'GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="generalized_exponential")',
    'GaussianProcess(regr="constant", optimizer="Welch", corr="generalized_exponential")',
    'GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="generalized_exponential")',
    'GaussianProcess(regr="linear", optimizer="Welch", corr="generalized_exponential")',
    'GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="generalized_exponential")',
    'GaussianProcess(regr="quadratic", optimizer="Welch", corr="generalized_exponential")',
    'GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="cubic")',
    'GaussianProcess(regr="constant", optimizer="Welch", corr="cubic")',
    'GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="cubic")',
    'GaussianProcess(regr="linear", optimizer="Welch", corr="cubic")',
    'GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="cubic")',
    'GaussianProcess(regr="quadratic", optimizer="Welch", corr="cubic")',
    'GaussianProcess(regr="constant", optimizer="fmin_cobyla", corr="linear")',
    'GaussianProcess(regr="constant", optimizer="Welch", corr="linear")',
    'GaussianProcess(regr="linear", optimizer="fmin_cobyla", corr="linear")',
    'GaussianProcess(regr="linear", optimizer="Welch", corr="linear")',
    'GaussianProcess(regr="quadratic", optimizer="fmin_cobyla", corr="linear")',
    'GaussianProcess(regr="quadratic", optimizer="Welch", corr="linear")',
    'GaussianNB()',
    'MultinomialNB()',
    'BernoulliNB()',
    'DecisionTreeClassifier()',
    'GradientBoostingClassifier(n_estimators=150, learning_rate=1.0, max_depth=1, random_state=0)',
    'AdaBoostClassifier(n_estimators=150)',
]

execution = Execution()
instance_meta = gcloud.get_metadata()
corpus = Corpus()

def main(classifier=None):
    if classifier is None:
        for index in range(0, len(classifiers)):
            run_classifier_with_id(index)
    elif classifier == "all-gcloud":
        run_after_progress()
    else:
        run_classifier_with_id(int(classifier))


def run_classifier_with_id(classifier_id):
    executor = ClassifierExecutor(classifiers[classifier_id])
    result = {"classifier": classifier_names[classifier_id], "classifier_id": classifier_id,
              "started_at": datetime.now(), "meta": instance_meta}
    execution.write_progress(result)
    try:
        precision = executor.execute(corpus.get_training(), corpus.get_test())
        print "%s: %.4f" % (classifier_names[classifier_id], precision)
        result['precision'] = precision
    except Exception as e:
        print "%s: %s" % (classifier_names[classifier_id], e)
        result['exception'] = str(e)
    result['ended_at'] = datetime.now()
    result['execution_time'] = str(result['ended_at'] - result['started_at'])
    execution.write_execution_result(result)


def run_after_progress():
    progress = execution.get_last_progress()
    if progress is None:
        run_classifier_with_id(0)
        return run_after_progress()
    elif progress["classifier_id"] + 1 < len(classifiers):
        run_classifier_with_id(progress["classifier_id"] + 1)
        return run_after_progress()
    else:
        return 0


if __name__ == "__main__":
    print sys.argv[1]
    if len(sys.argv) > 0:
        main(sys.argv[1])
    else:
        main()
