import numpy as np

from data.MongoDB import db

# history = db.results_collection.find(
#             {"binary_classification": False, "ngram": 2, "include_user_history": False}).sort(
#             "classifier_id", 1)
#
# history_means = []
# for result in history:
#     if "result" in result:
#         history_means.append(np.mean(map(float, result["result"]["f1score"])))
#     else:
#         history_means.append(.5)
#
# nohistory = db.results_collection.find(
#             {"binary_classification": False, "ngram": 2, "include_user_history": False}).sort(
#             "classifier_id", 1)
#
# nohistory_means = []
# for result in nohistory:
#     if "result" in result:
#         nohistory_means.append(np.mean(map(float, result["result"]["f1score"])))
#     else:
#         nohistory_means.append(.5)
#
# for i in range(0, len(classifier_names)):
#     if nohistory_means[i] < history_means[i]:
#         print classifier_names[i]
#         print nohistory_means[i] - history_means[i]
#
# print np.mean(history_means) - np.mean(nohistory_means)
from sklearn_comparison import configurations

results = db.results_collection.find({"binary_classification": True, "include_user_history": True})

resultz = []

for result in results:
    if "result" in result:
        resultz.append({"f1": np.mean(map(float, result["result"]["f1score"])), "precision": np.mean(map(float, result["result"]["precision"])), "recall": np.mean(map(float, result["result"]["recall"])), "classifier": result["classifier"], "configuration": configurations[result["configuration_id"]]})



def get_value(d):
    return d["f1"]


fin = sorted(resultz, key=get_value)

print fin
