from mongoDB import MongoDB


class Questions:

    def __init__(self):
        collection_name = 'questions'
        self.questionCollection = MongoDB.connect(collection_name)

    def addQuestion(self, questions):
        self.questionCollection.insert_one(questions)

    def getLastQuestionId(self):
        if len(list(self.questionCollection.find())) is not 0:
            last_question = list(self.questionCollection.find({}).sort("questionId", -1).limit(1))
            return last_question[0]["questionId"]
        else:
            return 0

    def getTotalCountOfQuestions(self):
        count = self.questionCollection.find({}).count()
        return count

    def getCompleteListOfQuestions(self):
        questionList = list(self.questionCollection.find({}, {'_id': 0}))
        return questionList

    def searchQuestionId(self, questionId):
        questionIdCount = self.questionCollection.find({"questionId": questionId}).count()
        return questionIdCount

    def getQuestionDetailsById(self, questionId):
        questionDesc = self.questionCollection.find({"questionId": questionId})[0]["questionDesc"]
        return questionDesc
