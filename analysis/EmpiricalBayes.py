from tweetmotif.twokenize import tokenize


class EmpiricalBayes:
    def __init__(self):
        self.data_count = 0
        self.training_data_count = 0
        self.location_counts = dict()
        self.location_token_counts = dict()
        self.location_token_total_counts = dict()

    def get_location_token_count(self, location, token):
        return self.location_token_counts[location][token] \
            if location in self.location_token_counts and token in self.location_token_counts[location] \
            else None

    def increment_location_token_count(self, location, token):
        if location not in self.location_token_counts:
            self.location_token_counts[location] = dict()
        if token not in self.location_token_counts[location]:
            self.location_token_counts[location][token] = 0
        self.location_token_counts[location][token] += 1

    def get_location_count(self, location):
        return self.location_counts[location] if location in self.location_counts else None

    def increment_location_count(self, location):
        if location not in self.location_counts:
            self.location_counts[location] = 0
        self.location_counts[location] += 1

    def get_location_token_total_count(self, location):
        return self.location_token_total_counts[location] if location in self.location_token_total_counts else None

    def increment_location_token_total_count(self, location, by):
        if location not in self.location_token_total_counts:
            self.location_token_total_counts[location] = 0
        self.location_token_total_counts[location] += by

    def train(self, docs, document_size):
        self.training_data_count = document_size
        count = 0
        for doc in docs:
            location = doc['place']['full_name']
            tokens = tokenize(reduce(lambda r, item: r + item['text'].lower() + " ", doc["timeline"], ''))
            self.increment_location_count(location)
            self.increment_location_token_total_count(location, len(tokens))
            for token in tokens:
                self.increment_location_token_count(location, token)
            count += 1
            if count % 100 == 0:
                print "training: " + str(count)

    def test_collective(self, docs):
        correct = 0
        count = 0
        for doc in docs:
            location = doc['place']['full_name']
            tokens = tokenize(reduce(lambda r, item: r + item['text'].lower() + " ", doc["timeline"], ''))
            max_val = None
            result = ""
            for loc in self.location_counts.keys():
                location_posterior = self.get_location_count(loc) / self.training_data_count
                for token in tokens:
                    location_token_count = self.get_location_token_count(loc, token)
                    if location_token_count is not None:
                        location_posterior *= location_token_count / self.get_location_token_total_count(loc)
                if max_val is None or location_posterior > max_val:
                    max_val = location_posterior
                    result = loc
            if result == location or result is location:
                correct += 1
            count += 1
            if count % 50 == 0:
                print "testing: " + str(count) + " corrects: " + str(correct)
        return correct

    def test_singular(self, docs):
        print "not ready yet"
        correct = 0
        count = 0
        for doc in docs:
            location = doc['place']['full_name']
            max_val = None
            result = ""
            for item in doc["timeline"]:  # for each status in timeline
                tokens = tokenize(item['text'].lower())  # tokenize the status text
                for loc in self.location_counts.keys():  # cross check locations and statuses
                    prior = self.get_location_count(loc) / self.training_data_count  # prior
                    likelihood = 1  #initial likelihood
                    for token in tokens:  # likelihood product
                        token_count = self.get_location_token_count(loc, token)
                        if token_count is not None:
                            likelihood *= (token_count / self.get_location_token_total_count(loc))
                    posterior = prior * likelihood
                    if max_val is None or posterior > max_val:
                        max_val = posterior
                        result = loc
            if result == location or result is location:
                correct += 1
            count += 1
            if count % 50 == 0:
                print "testing: " + str(count) + " corrects: " + str(correct)
        return correct
