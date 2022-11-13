from flask import Flask, request, render_template
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

# name, info(dict) pair
games = {}

class Game(Resource):
    # Info of game
    # game_name: str
    def get(self, name):
        return games[name]
    # Modify of info of game
    # info: dict
    def post(self, name, info):
        games[name] = info
        
api.add_resource(Game, "/game/<str: name>")
        

if __name__ == "__main__":
    app.run(debug=True)