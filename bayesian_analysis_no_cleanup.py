from analysis.EmpiricalBayes import EmpiricalBayes
from data import MongoDB
from settings import mongod_config

training_factor = 0.8

mongodb = MongoDB(mongod_config)
docs = mongodb.tweets_collection.find()
m = dict()
count = 0
for doc in docs:
    l = doc['place']['full_name']
    if l not in m:
        m[l] = 0
    m[l] += 1
    count += 1

for n in m.keys():
    if m[n] < count * 0.01:
        del m[n]

query = []

for n in m.keys():
    query.append({"place.full_name": n})

doc_count = mongodb.tweets_collection.find({"$or": query}).count()

training_doc_count = int(doc_count * training_factor)

training_data = mongodb.tweets_collection.find({"$or": query}).limit(training_doc_count)

bayes = EmpiricalBayes()
bayes.train(training_data, training_doc_count)

test_data = mongodb.tweets_collection.find({"$or": query}).skip(training_doc_count)
collective_matches = bayes.test_collective(test_data)

test_data = mongodb.tweets_collection.find({"$or": query}).skip(training_doc_count)
singular_matches = bayes.test_singular(test_data)

total_tested = doc_count - training_doc_count
print "collective matches: %d" % collective_matches
print "collective precision: %f" % (float(collective_matches) / total_tested)

print "singular matches: %d" % singular_matches
print "singular precision: %f" % (float(singular_matches) / total_tested)
# collective matches: 46
# collective precision: 0.086466
# singular matches: 46
# singular precision: 0.086466
