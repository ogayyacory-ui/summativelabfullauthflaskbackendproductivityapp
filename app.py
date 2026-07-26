from flask import Flask
from flask_restful import Api
from config import Config
from extensions import db, bcrypt, migrate, jwt, cors
from routes.auth import RegisterResource, LoginResource, MeResource
from routes.note import NoteListResource, NoteDetailResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register Flask-RESTful routes
    api = Api(app)
    api.add_resource(RegisterResource, '/register')
    api.add_resource(LoginResource, '/login')
    api.add_resource(MeResource, '/me')
    api.add_resource(NoteListResource, '/notes')
    api.add_resource(NoteDetailResource, '/notes/<int:note_id>')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)