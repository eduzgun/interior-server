from application import app, db
from application.blueprints.rooms.model import Rooms

app.app_context().push()

class Users(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String, nullable=False)
    rooms = db.relationship('Rooms', backref='users')
    


    def __repr__(self):
        return f"Users(id: {self.id}, username: {self.username} )"
    
    @property
    def json(self):
        return { "id": self.id, "username": self.username, "password": self.password}

