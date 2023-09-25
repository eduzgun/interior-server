from application import app, db


app.app_context().push()

class Likes(db.Model):
    __tablename__='likes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'))
    

    


    def __repr__(self):
        return f"Likes(id: {self.id}, user_id: {self.user_id}, room_id: {self.room_id} )"
    
    @property
    def json(self):
        return { "id": self.id, "user_id": self.user_id, "room_id": self.room_id}
