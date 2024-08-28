import json
import os
from datetime import datetime

class RelationStatus:
      null :str = 'null'
      Pasive :str = 'Pasive'
      Active :str = 'Active'


class RelationDirection:
      InActive :str = 'InActive'
      Convergent :str = 'Convergent'
      Divergent :str = 'Divergent'


class CurentEntityRelation:
        uid : str = any
        source : str = any
        destination : str = any
        direction : str = any
        config : str = any
        start_time : str = any
        end_time : str = any
        status : str = any
        value : str = any
        option : str = any


class LastEntityRelation:
        CurentRelation : CurentEntityRelation = any
        LastRelation :CurentEntityRelation = []



class SubjectItem:
      name: str = any
      value: str = any
      type: str = any
      
class TotalRelation:
    def __init__(self, uid, type, time, RelationNumber):
        self.uid=uid
        self.type=type
        self.time = time
        self.RelationNumber= RelationNumber