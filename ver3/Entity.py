import json
import os
from datetime import datetime

class EntityRelationOld:
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


class TotalRelation:
    def __init__(self, uid, type, time, RelationNumber):
        self.uid=uid
        self.type=type
        self.time = time
        self.RelationNumber= RelationNumber