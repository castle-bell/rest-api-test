from flask import Flask, request
from flask_restx import Api, Resource
from collections import defaultdict

app = Flask(__name__)
api = Api(app)

usersInfo = {}
usersStat = defaultdict(bool)

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world!"}

@api.route('/hello/<string:name>', methods=['POST'])  # url pattern으로 name 설정
class Hello(Resource):
    def post(self, name):  # 멤버 함수의 파라미터로 name 설정
        return {"message" : "Welcome, %s!" % name}


#sign up
#회원가입을 한 사람들의 login string과 비밀번호의 dict로 저장한 걸 global로 하고
@api.route('/signup', methods=['get'])
class Signup(Resource):
    def get(self):
        id = request.args.get('id', None)
        pw = request.args.get('pw', None)

        if id is None:
            return "sign up failed"

        if id in usersInfo.keys():
            return "You already have same id"

        if len(pw) < 4:
            return "Too short pw"

        usersInfo[id] = pw
        usersStat[id]
        return "success : %s" % len(usersInfo)

#global에서 체크해서 접속 제한 or 맞을 경우 상태 
@api.route('/login', methods=['get'])
class Login(Resource):
    def get(self):
        id = request.args.get('id', None)
        pw = request.args.get('pw', None)

        if not id in usersInfo.keys():
            return "Invalid Id"

        if not pw == usersInfo[id]:
            return "Invalid pw"

        if not usersStat[id] == False:
            return "Already login!"

        usersStat[id] = True
        return "Login success!"

# #logout
@api.route('/logout', methods=['get'])
class Logout(Resource):
    def get(self):
        id = request.args.get('id', None)
        
        if not usersStat[id] == True:
            return "Please login first"
        
        if not id in usersInfo.keys():
            return "There is no such id"

        usersStat[id] = False
        return "Logout"

# if __name__ == "__main__": 
#     app.run(debug=True, host='0.0.0.0', port=80)