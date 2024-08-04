import json
import os
from datetime import datetime

class EntityRelation:
    def __init__(self, uid, source,distination,direction,UpdateTime,EventTime,Active, Passive):
        self.uid=uid
        self.source=source
        self.distination=distination
        self.direction=direction
        self.UpdateTime=UpdateTime
        self.EventTime=EventTime
        self.Active = Active
        self.Passive=Passive

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


class TotalRelation:
    def __init__(self, uid, type, time, RelationNumber):
        self.uid=uid
        self.type=type
        self.time = time
        self.RelationNumber= RelationNumber


