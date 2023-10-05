from application import create_app, db
from application.blueprints.users.model import Users
from application.blueprints.rooms.model import Rooms
from application.blueprints.likes.model import Likes


app = create_app()

with app.app_context():
    db.drop_all()
    print('Dropping database')

    db.create_all()
    print('Creating database')

    print('Seeding database')

    entry1 = Users(username = "user1", email = "1@gmail.com", password="ZXKCASASFAFA", avatar_image="https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png")
    entry2 = Users(username = "user2", email = "2@gmail.com", password="DSFSAREGER", avatar_image="https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png")
    entry3 = Users(username = "user3", email = "3@gmail.com", password="GFDGSRGEW", avatar_image="https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png")
    entry4 = Users(username = "user4", email = "4@gmail.com", password="FSDF943KDSFAJE", avatar_image="https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png")
    entry5 = Users(username = "user5", email = "5@gmail.com", password="5dskfroir", avatar_image="https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png")
    entry6 = Users(username = "user6", email = "6@gmail.com", password="sakdsa382aweqw", avatar_image="https://interior-cloud-store.s3.amazonaws.com/avatar-images/profile.png")
    entry7 = Rooms(name="My personal room", dimensions="12 ft x 18 ft", description="My new room for my new house", theme="Art Deco" , category="FILLER", cover_image='https://interior-cloud-store.s3.amazonaws.com/environment-maps/0/px.png', user_id=1)
    entry8 = Rooms(name="My living room", dimensions="12 ft x 18 ft", description="My new living room for my new house", theme="Bohemian" ,category="FILLER", cover_image='https://interior-cloud-store.s3.amazonaws.com/environment-maps/2/px.png', user_id=2)
    entry9 = Rooms(name="My bathroom", dimensions="12 ft x 18 ft", description="My new bathroom for my new house", theme="12 ft x 18 ft" ,category="FILLER", cover_image='https://interior-cloud-store.s3.amazonaws.com/environment-maps/2/px.png', user_id=3)
    entry10 = Likes(user_id=1, room_id=1)
    entry11 = Likes(user_id=3, room_id=3)
    entry12 = Likes(user_id=4, room_id=2)
    entry13 = Likes(user_id=1, room_id=2)
    entry14 = Likes(user_id=3, room_id=2)
    entry15 = Likes(user_id=1, room_id=3)


    db.session.add_all([entry1,entry2,entry3,entry4,entry5,entry6,entry7, entry8,entry9,entry10, entry11, entry12, entry13, entry14, entry15])

    db.session.commit()
