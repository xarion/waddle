from data.MongoDB import db


class Execution:
    def __init__(self):
        self.mongodb = db

    def write_execution_result(self, result):
        self.mongodb.results_collection.insert_one(result)

    def write_progress(self, progress):
        self.mongodb.progress_collection.insert_one(progress)

    def get_last_progress(self):
        return self.mongodb.progress_collection.find_one({"$query": {}, "$orderby": {"classifier_id": -1}})
