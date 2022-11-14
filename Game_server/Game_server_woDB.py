from flask import Flask
from flask_restx import Api, Resource, abort, reqparse

# Initialize the app
app = Flask(__name__)
api = Api(app)

# Stored data (game_id: [game_name: str, game_info: str, 
# eval_users: int, rate: float, {user_name:comment}:dict])
games = {}


class Game(Resource):
    def __init__(self):
        self.game_put_args = reqparse.RequestParser()
        self.game_put_args.add_argument("name", type=str, help="Name of Game")
        self.game_put_args.add_argument("info", type=str, help="Info of Game")
        
    def isExistGame(self, game_id):
        if game_id not in games:
            abort(404, message="Could not find such game...")
        
    def isnotExistGame(self, game_id):
        if game_id in games:
            abort(409, message="Game already exists...")    
        
    def get(self, game_id):
        self.isExistGame(game_id)
        return games[game_id]
    
    def put(self, game_id, game_name, game_info):
        self.isnotExistGame(game_id)
        
        games[game_id] = [game_name, game_info, 0, 0.0, {}]
        return 202, 