from application import app, db


app.app_context().push()

class Rooms(db.Model):
    __tablename__='rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dimensions = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=False)
    theme = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    


    def __repr__(self):
        return f"Rooms(id: {self.id}, name: {self.name} )"
    
    @property
    def json(self):
        return { "id": self.id, "name": self.name, "dimensions": self.dimensions, "description": self.description, "user_id": self.user_id}
