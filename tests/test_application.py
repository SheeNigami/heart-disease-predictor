#1: Import libraries need for the test
from application.models import Entry
import datetime as datetime
import pytest
from flask import json
 
#Unit Test
#2: Parametrize section contains the data for the test
@pytest.mark.parametrize("entrylist",[
    [18000, 170, 70,  1, 100, 80, 1, 1, 1, 1, 2, 0],  #Test integer arguments
    [21.1, 200.2, 80.3, 0.4, 1.1, 70.7, 88.8, 1.1, 1.1, 1.9, 1.1, 2.1, 1.1]   #Test float arguments
])
#3: Write the test function pass in the arguments
def test_EntryClass(entrylist,capsys):
    with capsys.disabled():
        print(entrylist)
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

