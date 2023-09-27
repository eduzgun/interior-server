from application import app, db
from application.blueprints.rooms.model import Rooms
from application.blueprints.likes.model import Likes



app.app_context().push()

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    rooms = db.relationship('Rooms', backref='users')
    likes = db.relationship('Likes', backref='users')
   

    


    def __repr__(self):
        return f"Users(id: {self.id}, username: {self.username} )"
    
    @property
    def json(self):
        return { "id": self.id, "username": self.username, "email": self.email, "password": self.password}

