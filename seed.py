from application import db
from application.blueprints.users.model import Users
from application.blueprints.rooms.model import Rooms



db.drop_all()
print('Dropping database')

db.create_all()
print('Creating database')

print('Seeding database')

entry1 = Users(username = "user1", password="2014-10-07")
entry2 = Users(username = "user2", password="2011-04-17")
entry3 = Users(username = "user3", password="2016-07-15")
entry4 = Users(username = "user4", password="2015-07-05")
entry5 = Users(username = "user5", password="2010-07-25")
entry6 = Users(username = "user6", password="2013-03-03")
entry7 = Rooms(name="trial1", dimensions=3, description="Trial", theme="trial1", user_id=1)

db.session.add_all([entry1,entry2,entry3,entry4,entry5,entry6,entry7])

db.session.commit()
