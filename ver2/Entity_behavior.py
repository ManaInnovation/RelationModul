import json
import os
from datetime import datetime
import uuid

class EntityRelation:
    def __init__(self, uid, source, destination, direction, config, start_time, end_time, status, value, option):
        self.uid = uid
        self.source = source
        self.destination = destination
        self.direction = direction
        self.config = config
        self.StartTime = start_time
        self.EndTime = end_time
        self.status = status
        self.value = value
        self.option = option
        self.direction_history = []  

    def to_dict(self):
        return {
            "uid": self.uid,
            "source": self.source,
            "destination": self.destination,
            "direction": self.direction,
            "config": self.config,
            "StartTime": self.StartTime,
            "EndTime": self.EndTime,
            "status": self.status,
            "value": self.value,
            "option": self.option,
            "direction_history": self.direction_history
        }

class FunctionReturn:
    def __init__(self, success, message, data=None):
        self.success = success
        self.message = message
        self.data = data

class V2Relation:
    def __init__(self):
        self.EntityRelationList = []  
        self.Logs = []  
        self.initial_null_created = False  

    def generate_uid(self, source, destination):
      
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{source}-{destination}"))
    
    def NewEntityRelation(self, source, destination):
        uid = self.generate_uid(source, destination)
        start_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

        
        new_relation = EntityRelation(uid, source, destination, "null", "default", start_time, None, "null", 0, "default")

        
        existing_relation = self.get_relation_by_uid(uid)
        if existing_relation:
           
            self.Logs.append({
                "type": existing_relation.direction,
                "EndTime": existing_relation.EndTime
            })

     
        if not self.initial_null_created:
            self.EntityRelationList = [new_relation] 
            self.initial_null_created = True 
            new_relation.EndTime = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

            self.SaveEntityRelations()  
            return FunctionReturn(True, "Successfully created and saved new Entity Relation.", new_relation.to_dict())
        else:
            return FunctionReturn(False, "A null relation has already been created.", None)

    def UpdateRelation(self, current_relation):
        if not isinstance(current_relation, EntityRelation):
            raise TypeError("The argument must be an instance of EntityRelation")

       
        existing_relation = self.get_relation_by_uid(current_relation.uid)
        if existing_relation:
            
            self.Logs.append({
                "type": existing_relation.direction,
                "EndTime": existing_relation.EndTime
            })

        current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        current_relation.EndTime = current_time

        
        self.EntityRelationList = [current_relation] 

        self.SaveEntityRelations()  
        return FunctionReturn(True, "Successfully updated Entity Relation.", current_relation)

    def get_relation_by_uid(self, uid):
        for relation in self.EntityRelationList:
            if relation.uid == uid:
                return relation
        return None

    def SaveEntityRelations(self, path='D:/EachEntityRelation'):
        
        if self.EntityRelationList:
            relation_data = self.EntityRelationList[0].to_dict()
            relation_data["direction_history"] = self.Logs 

            with open(os.path.join(path, 'relations.json'), 'w') as file:
                json.dump(relation_data, file, indent=4)

        return FunctionReturn(True, "Successfully saved entity relations with logs.")

if __name__ == "__main__":
    v2relation = V2Relation()

    
    new_relation = v2relation.NewEntityRelation("A", "B")
    print("New Relation Created:")
    print(new_relation.message)

    
    new_relation_data = new_relation.data

    
    update_relation_convergent = EntityRelation(
        new_relation_data["uid"],
        "A",
        "B",
        "disvergent",
        "default",
        new_relation_data["StartTime"],
        datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "active",
        100,
        "default"
    )
    updated_convergent = v2relation.UpdateRelation(update_relation_convergent)
    print("Relation Updated to Convergent:")
    print(updated_convergent.message)

    
    update_relation_disvergent = EntityRelation(
        updated_convergent.data.uid,
        "A",
        "B",
        "inactive",
        "default",
        updated_convergent.data.EndTime,
        datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "active",
        200,
        "default"
    )
    updated_disvergent = v2relation.UpdateRelation(update_relation_disvergent)
    print("Relation Updated to Disvergent:")
    print(updated_disvergent.message)

    
    update_relation_inactive = EntityRelation(
        updated_disvergent.data.uid,
        "A",
        "B",
        "nonconvergent",
        "default",
        updated_disvergent.data.EndTime,
        datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        "passive",
        0,
        "default"
    )
    updated_inactive = v2relation.UpdateRelation(update_relation_inactive)