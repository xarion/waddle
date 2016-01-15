import matplotlib
from matplotlib import pyplot as plt

from data.MongoDB import db

binary_classification = False

matplotlib.rcParams.update({'font.size': 3})

baseline = None
if binary_classification:
    baseline = 1. / 2
else:
    baseline = 1. / 8

mean_line_props = dict(linestyle='--', color='r')
median_line_props = dict(linestyle='None')


def plot(ngram, history, sub_index, axes, title):
    binary_classification_result_docs = db.results_collection.find(
            {"binary_classification": binary_classification, "ngram": ngram, "include_user_history": history}).sort(
            "classifier_id", 1)

    precision_results = []
    recall_results = []
    f1score_results = []

    labels = list()
    empty_results = None
    for result in binary_classification_result_docs:
        if "result" in result:
            precision_results.append(map(float, result["result"]["precision"]))
            recall_results.append(map(float, result["result"]["recall"]))
            f1score_results.append(map(float, result["result"]["f1score"]))
            if empty_results is None:
                empty_results = [.0] * len(result["result"]["precision"])
        else:
            precision_results.append(empty_results)
            recall_results.append(empty_results)
            f1score_results.append(empty_results)

        labels.append(result["classifier_id"])

    axes[0][sub_index].set_title(title)

    axes[0][sub_index].boxplot(precision_results, labels=labels, showmeans=True, meanline=True,
                               meanprops=mean_line_props, medianprops=median_line_props)
    axes[0][sub_index].plot([0, 23], [baseline, baseline], "g-")
    axes[0][sub_index].set_ylabel('Precision')
    axes[0][sub_index].set_ylim([0, 1])

    axes[1][sub_index].boxplot(recall_results, labels=labels, showmeans=True, meanline=True, meanprops=mean_line_props,
                               medianprops=median_line_props)
    axes[1][sub_index].plot([0, 23], [baseline, baseline], "g-")
    axes[1][sub_index].set_ylabel('Recall')
    axes[1][sub_index].set_ylim([0, 1])

    axes[2][sub_index].boxplot(f1score_results, labels=labels, showmeans=True, meanline=True, meanprops=mean_line_props,
                               medianprops=median_line_props)
    axes[2][sub_index].plot([0, 23], [baseline, baseline], "g-")
    axes[2][sub_index].set_ylabel('F1Score')
    axes[2][sub_index].set_ylim([0, 1])


fig, axs = plt.subplots(nrows=3, ncols=4)

plot(1, False, 0, axs, "ngram=1, No User History")
plot(2, False, 1, axs, "ngram=2, No User History")
plot(1, True, 2, axs, "ngram=1, With User History")
plot(2, True, 3, axs, "ngram=2, With User History")

# plt.show()

if binary_classification:
    fig.savefig('docs/figures/binary.eps', format='eps', dpi=1000)
else:
    fig.savefig('docs/figures/multi_class.eps', format='eps', dpi=1000)
