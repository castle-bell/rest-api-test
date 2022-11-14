from flask import Flask, render_template
from flask_restx import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class GameModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # Max length of string
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return "Game(name={name}, views={views}, likes={likes})"

db.create_all()

# name, info(dict) pair
game_put_args = reqparse.RequestParser()
game_put_args.add_argument("name", type=str, help="Name of the game", required=True)
game_put_args.add_argument("views", type=int, help="Views of the game", required=True)
game_put_args.add_argument("likes", type=int, help="Likes of the game", required=True)

game_update_args = reqparse.RequestParser()
game_update_args.add_argument("name", type=str, help="Name of the game")
game_update_args.add_argument("views", type=int, help="Views of the game")
game_update_args.add_argument("likes", type=int, help="Likes of the game")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer,
}


class Game(Resource):
    @marshal_with(resource_fields) # Instead of returning instances, returning the serialized object
    def get(self, game_id):
        result = GameModel.query.filter_by(id=game_id).first() # Instance of GameModel
        if not result:
            abort(404, message="Could not find game with that id")
        
        return result

    @marshal_with(resource_fields)
    def put(self, game_id):
        args = game_put_args.parse_args()
        result = GameModel.query.filter_by(id=game_id).first()
        if result:
            abort(409, message="Video id taken...")
        
        game = GameModel(id=game_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(game) # Like github
        db.session.commit()
        return game, 201
    
    @marshal_with(resource_fields)
    def patch(self, game_id, ):
        args = game_update_args.parse_args()
        result = GameModel.guery.filter_by(id=game_id).first()
        if not result:
            abort(404, message="Game doesn't exist, cannot update")
        
        # Change the instances
        if args['name'] :
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
            
        db.session.commit()
        
        return result
    
    def delete(self, game_id):
        del games[game_id]
        return '', 204
        
        
api.add_resource(Game, "/game/<int:game_id>")
        

if __name__ == "__main__":
    app.run(debug=True)