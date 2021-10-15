from flask import Flask, jsonify, request
from flask_restful import Api, Resource
# from pymongo import MongoClient
import questions

from mongoDB import MongoDB

app = Flask(__name__)
api = Api(app)

questions = questions.Questions()


class storeQuestion(Resource):
    def post(self):
        postedData = request.get_json()
        questionDescription = postedData["questionDescription"]

        lastQuestionId = questions.getLastQuestionId()

        questions.addQuestion({
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
        questionCount = questions.getTotalCountOfQuestions()

        if questionCount == 0:
            retJson = {
                "status": 200,
                "message": "You have not added any questions"
            }

            return jsonify(retJson)

        question = questions.getCompleteListOfQuestions()

        retJson = {
            "status": 200,
            "questionsList": question
        }

        return jsonify(retJson)

        # return jsonify([question for question in questionList])


class getQuestionById(Resource):
    def get(self, questionId):
        searchedQuestionId = questions.searchQuestionId(questionId)

        if searchedQuestionId == 0:
            retJson = {
                "status": 301,
                "message": "This questionId doesn't exist"
            }
            return jsonify(retJson)

        questionDetails = questions.getQuestionDetailsById(questionId)

        retJson = {
            "status": 200,
            "questionId": questionId,
            "questionDesc": questionDetails
        }

        return jsonify(retJson)


api.add_resource(storeQuestion, '/api/v1/question')
api.add_resource(getQuestionById, '/api/v1/question/<int:questionId>')
api.add_resource(getQuestionList, '/api/v1/questions')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
