from pymongo import MongoClient


class MongoDB:
    @classmethod
    def connect(cls, collection_name):
        client = MongoClient("mongodb://db:27017")
        db = client.QuestionsDatabase
        questions = db[collection_name]
        return questions
