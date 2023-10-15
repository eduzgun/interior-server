from flask import current_app
from application import db
from application.blueprints.likes.model import Likes


#current_app.app_context().push()

class Rooms(db.Model):
    __tablename__='rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    dimensions = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    # cover_image = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fetchUID = db.Column(db.String(100),nullable=False)
    likes = db.relationship('Likes', backref='rooms', cascade='all, delete-orphan')
  
    

    


    def __repr__(self):
        return f"Rooms(id: {self.id}, name: {self.name}, dimensions: {self.dimensions},description: {self.description}, theme: {self.theme}, category: {self.category}, user_id:{self.user_id}, fetchUID:{self.fetchUID} )"
    
    @property
    def json(self):
        return { "id": self.id, "name": self.name, "dimensions": self.dimensions, "description": self.description, "theme": self.theme, "category": self.category, "user_id": self.user_id, "fetchUID": self.fetchUID}
