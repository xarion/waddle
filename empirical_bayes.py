from analysis.EmpiricalBayes import EmpiricalBayes

from data.Data import Data

training_factor = 0.6

data = Data(training_factor)
bayes = EmpiricalBayes()
bayes.train(data.get_training_data(), data.training_doc_count)

collective_matches = bayes.test_collective(data.get_test_data())

singular_matches = bayes.test_singular(data.get_test_data())

total_tested = data.doc_count - data.training_doc_count
print "collective matches: %d" % collective_matches
print "collective precision: %f" % (float(collective_matches) / total_tested)

print "singular matches: %d" % singular_matches
print "singular precision: %f" % (float(singular_matches) / total_tested)
# collective matches: 100
# collective precision: 0.113985
# singular matches: 100
# singular precision: 0.093985
