from flask import Flask, request
from config import Config
from extensions import db, bcrypt, migrate, jwt, cors
from route.auth import RegisterResource, LoginResource, MeResource, LogoutResource
from route.note import NoteListResource, NoteDetailResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # Register direct Flask routes instead of Flask-RESTful resources
    @app.route('/register', methods=['POST'])
    def register():
        return RegisterResource().post()

    @app.route('/login', methods=['POST'])
    def login():
        return LoginResource().post()

    @app.route('/me', methods=['GET'])
    def me():
        return MeResource().get()

    @app.route('/logout', methods=['POST'])
    def logout():
        return LogoutResource().post()

    @app.route('/notes', methods=['GET', 'POST'])
    def notes():
        resource = NoteListResource()
        if request.method == 'GET':
            return resource.get()
        return resource.post()

    @app.route('/notes/<int:note_id>', methods=['GET', 'PATCH', 'DELETE'])
    def note_detail(note_id):
        resource = NoteDetailResource()
        if request.method == 'GET':
            return resource.get(note_id)
        if request.method == 'PATCH':
            return resource.patch(note_id)
        return resource.delete(note_id)

    @app.route('/')
    def home():
        return {"message": "Welcome to the Productivity App API! Use /register, /login, /me, and /notes"}

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)