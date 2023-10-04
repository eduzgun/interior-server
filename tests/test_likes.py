def test_get_likes(test_client):
    '''
    GIVEN the GET /likes route is defined
    WHEN the likes are requested
    THEN check that the response is valid and contains "likes"
    '''
    response = test_client.get('/likes')
    assert response.status_code == 200
    assert "likes" in response.json


def test_create_duplicate_like(test_client):
    '''
    GIVEN the POST /likes route is defined
    WHEN a duplicate like is created
    THEN check that the response status code is 400
    '''
    user_id = 1  
    room_id = 1  

    test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})

    response = test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})
    assert response.status_code == 400

def test_get_likes_by_user(test_client):
    '''
    GIVEN the GET /likes/user/<id> route is defined
    WHEN the likes for a specific user are requested
    THEN check that the response status code is 200 and contains "data"
    '''
    user_id = 1  
    response = test_client.get(f'/likes/user/{user_id}')
    assert response.status_code == 200
    assert "data" in response.json

def test_get_likes_by_room(test_client):
    '''
    GIVEN the GET /likes/room/<id> route is defined
    WHEN the likes for a specific room are requested
    THEN check that the response status code is 200 and contains "data"
    '''
    room_id = 1  
    response = test_client.get(f'/likes/room/{room_id}')
    assert response.status_code == 200
    assert "data" in response.json

def test_delete_like(test_client):
    '''
    GIVEN the DELETE /likes/<user_id>/<room_id> route is defined
    WHEN a like is created and then deleted
    THEN check that the response status code is 204
    '''
    user_id = 1  
    room_id = 1  

    test_client.post('/likes', json={"user_id": user_id, "room_id": room_id})

    response = test_client.delete(f'/likes/{user_id}/{room_id}')
    assert response.status_code == 204
