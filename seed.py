from application import db
from application.blueprints.users.users import Users

# id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     start_date = db.Column(db.Date, nullable=False)
#     end_date = db.Column(db.Date, nullable=False)
#     country= db.Column(db.String(100), nullable=False)
#     network = db.Column(db.String(100), nulable=False)

db.drop_all()
print('Dropping database')

db.create_all()
print('Creating database')

print('Seeding database')

entry1 = Users(username = "user1", email = "1@gmail.com", password="2014-10-07")
entry2 = Users(username = "user2", email = "2@gmail.com", password="2011-04-17")
entry3 = Users(username = "user3", email = "3@gmail.com", password="2016-07-15")
entry4 = Users(username = "user4", email = "4@gmail.com", password="2015-07-05")
entry5 = Users(username = "user5", email = "5@gmail.com", password="2010-07-25")
entry6 = Users(username = "user6", email = "6@gmail.com", password="2013-03-03")

db.session.add_all([entry1,entry2,entry3,entry4,entry5,entry6])

db.session.commit()
