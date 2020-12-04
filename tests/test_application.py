#1: Import libraries need for the test
from application.models import Entry
import datetime as datetime
import pytest
from flask import json
 
#Unit Tests

# Validity testing
@pytest.mark.parametrize("entrylist",[
    [18000, 170, 70,  1, 100, 80, 1, 1, 1, 1, 2, 0], # Test basic integers
    [13337, 180, 80,  1, 90, 70, 1, 1, 1, 1, 2, 0] # Test basic integers
])
# Test Entry Class
def test_EntryClass(entrylist,capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_entry = Entry(  age= entrylist[0], 
                            height = entrylist[1],
                            weight= entrylist[2],
                            gender = entrylist[3],
                            s_blood_pressure  = entrylist[4],  
                            d_blood_pressure = entrylist[5],
                            cholesterol = entrylist[6],
                            glucose = entrylist[7], 
                            smoking = entrylist[8], 
                            alcohol = entrylist[9], 
                            physical = entrylist[10], 
                            prediction = entrylist[11],
                            predicted_on = now  ) 
 
        assert new_entry.age == entrylist[0]
        assert new_entry.height == entrylist[1]
        assert new_entry.weight == entrylist[2]
        assert new_entry.gender == entrylist[3]
        assert new_entry.s_blood_pressure == entrylist[4]
        assert new_entry.d_blood_pressure == entrylist[5]
        assert new_entry.cholesterol == entrylist[6]
        assert new_entry.glucose == entrylist[7]
        assert new_entry.smoking == entrylist[8]
        assert new_entry.alcohol == entrylist[9]
        assert new_entry.physical == entrylist[10]
        assert new_entry.prediction == entrylist[11]
        assert new_entry.predicted_on == now


# Expected Failsure testing for Entry class
@pytest.mark.xfail(reason='unexpected values in label encoded fields')
@pytest.mark.parametrize("entrylist",[
    [21.1, 200.2, 80.3, 0.4, 1.1, 70.7, 88.8, 1.1, 1.1, 1.9, 1.1, 2.1, 1.1]   #Test float arguments
    [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -13] # Test negative 
    [17000, 170, 80, 4, 80, 100, 7, 8, 9, 10, 11, 12, 13] # Test labels that don't exist for label encoded variables
])
def test_EntryClass(entrylist,capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_entry = Entry(  age= entrylist[0], 
                            height = entrylist[1],
                            weight= entrylist[2],
                            gender = entrylist[3],
                            s_blood_pressure  = entrylist[4],  
                            d_blood_pressure = entrylist[5],
                            cholesterol = entrylist[6],
                            glucose = entrylist[7], 
                            smoking = entrylist[8], 
                            alcohol = entrylist[9], 
                            physical = entrylist[10], 
                            prediction = entrylist[11],
                            predicted_on = now  ) 
 
        assert new_entry.age == entrylist[0]
        assert new_entry.height == entrylist[1]
        assert new_entry.weight == entrylist[2]
        assert new_entry.gender == entrylist[3]
        assert new_entry.s_blood_pressure == entrylist[4]
        assert new_entry.d_blood_pressure == entrylist[5]
        assert new_entry.cholesterol == entrylist[6]
        assert new_entry.glucose == entrylist[7]
        assert new_entry.smoking == entrylist[8]
        assert new_entry.alcohol == entrylist[9]
        assert new_entry.physical == entrylist[10]
        assert new_entry.prediction == entrylist[11]
        assert new_entry.predicted_on == now


# Unit test for User Class
# Validity Testing
@pytest.mark.parametrize('userlist', [
    ['asdfasdf', 'lskdjfsldkfjksdl'], # Valid user
    ['sheen', 'sheenhern'] # Valid user
])
def test_UserClass(userlist, capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_user = User(  username= entrylist[0], 
                          password = entrylist[1],
                          created_on = now  ) 
 
        assert new_user.username == userlist[0]
        assert new_user.password == userlist[1]


@pytest.mark.xfail(reason='user already exists')
@pytest.mark.parametrize("userlist",[
    ['sheen', 'sheenhern'],
    ['asdfasdf', 'lskdjfsldkfjksdl']
])
def test_UserClass(userlist, capsys):
    with capsys.disabled():
        now = datetime.datetime.utcnow()
        new_user = User(  username= entrylist[0], 
                          password = entrylist[1],
                          created_on = now  ) 
 
        assert new_user.username == userlist[0]
        assert new_user.password == userlist[1]


# Test add API
@pytest.mark.parametrize("entrylist",[
    [18000, 170, 70,  1, 100, 80, 1, 1, 1, 1, 2, 0],  #Test integer arguments
    [21.1, 200.2, 80.3, 0.4, 1.1, 70.7, 88.8, 1.1, 1.1, 1.9, 1.1, 2.1, 1.1]   #Test float arguments
])

def test_addAPI(client, entrylist, capsys):
    with capsys.disabled():
        data = {  'age': entrylist[0], 
                  'height' : entrylist[1],
                  'weight': entrylist[2],
                  'gender' : entrylist[3],
                  's_blood_pressure' : entrylist[4],  
                  'd_blood_pressure' : entrylist[5],
                  'cholesterol' : entrylist[6],
                  'glucose' : entrylist[7], 
                  'smoking' : entrylist[8], 
                  'alcohol' : entrylist[9], 
                  'physical' : entrylist[10], 
                  'prediction' : entrylist[11] }

        response = client.post('/api/add', data=json.dumps(data), content_type="application/json")

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body["id"]


@pytest.mark.parametrize("id", [1,2])
def test_deleteAPI(client, id, capsys): 
    with capsys.disabled():
        response = client.get(f'/api/delete/{id}')
        ret = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers['Content-Type'] == "application/json"
        response_body = json.loads(response.get_data(as_text=True))
        assert response_body['result'] == 'ok'


def test_getAllEntryAPI(client, capsys):
    response = client.get('/api/getAllEntry')
    ret = json.loads(response.get_data(as_text=True))
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "application/json"
    assert 
