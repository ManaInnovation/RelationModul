import json
import os
from datetime import datetime

#  ,[type]
#       ,[UID]
#       ,[source]
#       ,[destination]
#       ,[config]
#       ,[status]
#       ,[time]
#       ,[value]
#       ,[option]



class EntityDirection:
    def __init__(self,direction,StartTime,EndTime,Status):
        self.direction=direction
        self.StartTime=StartTime # End time
        self.EndTime=EndTime # start time
        self.Status = Status

    def to_dict(self):
        return{
            "uid": self.uid,
            "source": self.source,
            "distination": self.distination,
            "direction": self.direction,
            "UpdateTime":self.StartTime,
            "EventTime": self.EndTime,
            "Active":self.Status,
        }


class EntityRelation:
    def __init__(self, uid, source,distination):
        self.uid=uid
        self.source=source
        self.distination=distination
        self.directionlist=[]
        

    def to_dict(self):
        return{
            "uid": self.uid,
            "source": self.source,
            "distination": self.distination,
            "direction": self.direction,
            "UpdateTime":self.UpdateTime,
            "EventTime": self.EventTime,
            "Active":self.Active,
            "passive":self.Passive
        }


mydirection = EntityDirection('1','24','24',True)

myentity = EntityRelation('12345','1234','12345')
myentity.directionlist.append(mydirection)

myentity.
hh = json.dump(myentity)
print(hh)

class TotalRelation:
    def __init__(self, uid, type, time, RelationNumber):
        self.uid=uid
        self.type=type
        self.time = time
        self.RelationNumber= RelationNumber


