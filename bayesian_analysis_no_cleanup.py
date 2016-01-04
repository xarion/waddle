from analysis.EmpiricalBayes import EmpiricalBayes
from data import MongoDB, Data
from settings import mongod_config

training_factor = 0.6

mongodb = MongoDB(mongod_config)
data = Data(mongodb)
location_filter_query = data.get_location_filter_query()

doc_count = mongodb.tweets_collection.find({"$or": location_filter_query}).count()

training_doc_count = int(doc_count * training_factor)

training_data = mongodb.tweets_collection.find({"$or": location_filter_query}).limit(training_doc_count)

bayes = EmpiricalBayes()
bayes.train(training_data, training_doc_count)

test_data = mongodb.tweets_collection.find({"$or": location_filter_query}).skip(training_doc_count)
collective_matches = bayes.test_collective(test_data)

test_data = mongodb.tweets_collection.find({"$or": location_filter_query}).skip(training_doc_count)
singular_matches = bayes.test_singular(test_data)

total_tested = doc_count - training_doc_count
print "collective matches: %d" % collective_matches
print "collective precision: %f" % (float(collective_matches) / total_tested)

print "singular matches: %d" % singular_matches
print "singular precision: %f" % (float(singular_matches) / total_tested)
# collective matches: 100
# collective precision: 0.093985
# singular matches: 100
# singular precision: 0.093985
