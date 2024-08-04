import json
import requests
import numpy as np 
import zipfile
import io
import pandas as pd
import traceback
import json
import os
from datetime import datetime
from Entity import EntityRelation
from dateutil import parser

def convert_to_json(my_dict):
    try:
        json_string=json.dumps(my_dict)
        return json_string
    except TypeError as e:
        print(f"error to convert dict to json: {e}")
        return None

def convert_to_dict(json_data):
    try:
        python_dict=json.loads(json_data)
        return python_dict
    except json.JSONDecodeError as e:
        print("error!")
        return None
    

def post_request(url, headers, data):
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during POST request: {e}")
        return None


def get_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during GET request: {e}")
        return None

class FunctionReturn:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "success":self.success,
            "message":self.message,
            "data":self.data
        }
    
    def __str__(self):
        return json.dumps(self.to_dict(), indent=4)


class V2Relation:
    def __init__(self):
        self.EntityRelationList=[]

    def NewEntityRelation(self,uid, source,distination,direction,UpdateTime,EventTime,Active, Passive):
        NewEntityRelationObject= EntityRelation(uid,source,distination, direction, UpdateTime,EventTime,Active,Passive)
        self.EntityRelationList.append(NewEntityRelationObject)
        #return json.dumps(NewEntityRelationObject.to_dict(), indent=4) 
        return FunctionReturn(True, "successfully created new Entity Relation.", NewEntityRelationObject)

    def UpdateRelation(self, last_relation, current_relation):
        if not isinstance(last_relation, EntityRelation) or not isinstance(current_relation, EntityRelation):
            raise TypeError("Both arguments must be instances of EntityRelation")

        if last_relation.uid == current_relation.uid:
            for attr, value in current_relation.__dict__.items():
                if value is not None:
                    setattr(last_relation, attr, value)
            #return json.dumps(last_relation.to_dict(), indent=4)
            return FunctionReturn(True, "successfully update Entity Relation", last_relation)
        else:
            return FunctionReturn(False, "UIDs don't match")
        

    def DeleteRelation(self,uid):
        for relation in self.EntityRelationList:
            if relation.uid==uid:
                self.EntityRelationList.remove(relation)
                return FunctionReturn(True, "Successfully deleted entity relation")
        return FunctionReturn(False, "Entity relation not found")
        #         return True
        # return False

    def SaveEntityRelation(self, EntityRlationObject, path= 'D:/EntityRelation'):
        if not isinstance(EntityRlationObject, EntityRelation):
            raise TypeError("EntityRelationObject must be an instance of EntityRelation")
        
        #if path is None:
            #path='D:/EntityRelation'

        #event_time = datetime.strptime(EntityRlationObject.EventTime, '%Y-%m-%dT%H:%M:%SZ')
        try:
            event_time = parser.parse(EntityRlationObject.EventTime)
        except ValueError as e:
            raise ValueError(f"Invalid date format for EventTime: {e}")
        year = event_time.year
        month = event_time.month
        day = event_time.day
        
        dir_path = os.path.join(path, str(year), f'{month:02}', f'{day:02}')
        os.makedirs(dir_path, exist_ok=True)
        
        file_name = f'{year}-{month:02}-{day:02}-{EntityRlationObject.uid}.json'
        file_path = os.path.join(dir_path, file_name)
        
        with open(file_path, 'w') as file:
            json.dump(EntityRlationObject.to_dict(), file, indent=4)

        return FunctionReturn(True, "Successfully saved entity relation")
    

    def fetch_data(self, uid, date):
        url = f"{self.base_url}/api/OBJVALUE"
        params = {
            "UID": uid,
            "date": date
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

