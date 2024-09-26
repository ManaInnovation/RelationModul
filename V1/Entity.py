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

      def __str__(self):
        return (f"CurentEntityRelation(start_time={self.start_time}, "
                f"end_time={self.end_time}, direction={self.direction}, "
                f"status={self.status}, SubjectList={self.SubjectList})")


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
            self.LastRelation =LastRelation if isinstance(LastRelation, list) else []

        def __str__(self):
            curent_relation_str = str(self.CurentRelation) if self.CurentRelation else "None"
            last_relation_str = ", ".join(str(rel) for rel in self.LastRelation) if self.LastRelation else "[]"
            return (f"LastEntityRelation(uid={self.uid}, source={self.source}, "
                  f"destination={self.destination}, config={self.config}, "
                  f"option={self.option}, CurentRelation={curent_relation_str}, "
                  f"LastRelation=[{last_relation_str}])")


class SubjectItem:
      def __init__(self,name: str, value: str ,type: str):

            self.name=name
            self.value=value
            self.type=type

      def __repr__(self):
        return f"SubjectItem(name={self.name}, value={self.value}, type={self.type})"
      
class TotalRelation:
    def __init__(self, uid, type, time, RelationNumber):
        self.uid=uid
        self.type=type
        self.time = time
        self.RelationNumber= RelationNumber

class Property:
    def __init__(self, id, object_id, field_id, field_relation_id, prop_type, UID, option):
        self.id = id
        self.object_id = object_id
        self.field_id = field_id
        self.field_relation_id = field_relation_id
        self.prop_type = prop_type
        self.UID = UID
        self.option = option

    def __str__(self):
        return (f"ID: {self.id}, Object ID: {self.object_id}, "
                f"Field ID: {self.field_id}, Field Relation ID: {self.field_relation_id}, "
                f"Type: {self.prop_type}, UID: {self.UID}, Option: {self.option}")