from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from mongoDB import db
import bcrypt

# from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

# client = MongoClient("mongodb://db:27017")
# db = client.QuestionsDatabase
questions = db['questions']


def getLastQuestionId(question):
    if len(list(question.find())) is not 0:
        last_question = list(question.find({}).sort("questionId", -1).limit(1))
        return last_question[0]["questionId"]
    else:
        return 0


class storeQuestion(Resource):
    def post(self):
        postedData = request.get_json()
        questionDescription = postedData["questionDescription"]

        lastQuestionId = getLastQuestionId(questions)

        questions.insert({
            'questionId': lastQuestionId + 1,
            'questionDesc': questionDescription
        })

        retJson = {
            "status": 200,
            "message": "Question saved successfully"
        }

        return jsonify(retJson)


class getQuestionList(Resource):
    def get(self):
        questionCount = questions.find({}).count()

        if questionCount == 0:
            retJson = {
                "status": 200,
                "message": "You have not added any questions"
            }

            return jsonify(retJson)

        question = list(questions.find({}, {'_id': 0}))

        retJson = {
            "status": 200,
            "questionsList": question
        }

        return jsonify(retJson)

        # return jsonify([question for question in questionList])


class getQuestionById(Resource):
    def get(self, questionId):
        searchedQuestionId = questions.find({"questionId": questionId}).count()

        if searchedQuestionId == 0:
            retJson = {
                "status": 301,
                "message": "This questionId doesn't exist"
            }
            return jsonify(retJson)

        question = questions.find({
            "questionId": questionId,
        })[0]["questionDesc"]

        retJson = {
            "status": 200,
            "questionId": questionId,
            "questionDesc": question
        }

        return jsonify(retJson)


api.add_resource(storeQuestion, '/api/v1/question')
api.add_resource(getQuestionById, '/api/v1/question/<int:questionId>')
api.add_resource(getQuestionList, '/api/v1/questions')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
