import json
import os
import CommonFunction as com
from datetime import datetime

class RelationStatus:
      null :str = 'null'
      Pasive :str = 'Pasive'
      Active :str = 'Active'


class RelationDirection:
      InActive :str = 'InActive'
      Convergent :str = 'Convergent'
      Divergent :str = 'Divergent'


class CovarCnf:
      Convergent :float =0.5
      Divergent :float =-0.5

      def __init__(self) -> None:
            assert self.Convergent > self.Divergent


class CurentEntityRelation:
      def __init__(self,start_time:str=com.Common_Time.Now(),end_time:str=com.Common_Time.Now(),
                   direction: str = RelationDirection.InActive,status: str = RelationStatus.null,SubjectList:list=com.ProcesStatus.Null):
        self.start_time = start_time
        self.end_time =end_time
        self.direction =direction
        self.status = status
        self.SubjectList = SubjectList if SubjectList else []
        


class LastEntityRelation:
        def __init__(self,uid: str = com.ProcesStatus.none,source: str = com.ProcesStatus.none,destination: str = com.ProcesStatus.none,
                     config: str = com.ProcesStatus.none,option: str = com.ProcesStatus.none ,
                     CurentRelation: CurentEntityRelation = any, LastRelation:list = com.ProcesStatus.none):
             
            self.uid =uid
            self.source =source
            self.destination =destination
            self.config =config
            self.option =option
            self.CurentRelation =CurentRelation
            self.LastRelation =LastRelation


class SubjectItem:
      def __init__(self,name: str, value: str ,type: str):

            self.name=name
            self.value=value
            self.type=type
      
class TotalRelation:
    def __init__(self, uid, type, time, RelationNumber):
        self.uid=uid
        self.type=type
        self.time = time
        self.RelationNumber= RelationNumber