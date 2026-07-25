from extenstions import db, bcrypt
# User model for the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(10), nullable=False)

# Constructor to initialize the User object with username, email, and password
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
#check_password method to verify the password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
# to_dict method to convert the User object to a dictionary representation
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
