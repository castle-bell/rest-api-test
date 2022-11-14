from flask import Flask, render_template
from flask_restx import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)

# class GameModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False) # Max length of string
#     views = db.Column(db.Integer, nullable=False)
#     likes = db.Column(db.Integer, nullable=False)
    
#     def __repr__(self):
#         return "Game(name={name}, views={views}, likes={likes})"

# db.create_all()

# name, info(dict) pair
game_put_args = reqparse.RequestParser()
game_put_args.add_argument("name", type=str, help="Name of the game", required=True)
game_put_args.add_argument("views", type=int, help="Views of the game", required=True)
game_put_args.add_argument("likes", type=int, help="Likes of the game", required=True)

games = {}

class Game(Resource):
    def isExistId(self, game_id):
        if game_id not in games:
            abort(404, message="Could not find such game...")
    
    def alreadyExistId(self, game_id):
        if game_id in games:
            abort(409, message="Game already exists with that ID...")

    def get(self, game_id):
        self.isExistId(game_id)
        return games[game_id]

    def put(self, game_id):
        self.alreadyExistId(game_id)
        args = game_put_args.parse_args()
        games[game_id] = args
        return games[game_id], 201 # Status which denotes the created
    
    def delete(self, game_id):
        self.isExistId(game_id)
        del games[game_id]
        return '', 204
        
        
api.add_resource(Game, "/game/<int:game_id>")
        

if __name__ == "__main__":
    app.run(debug=True)