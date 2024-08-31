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
            assert self.Convergent < self.Divergent


class CurentEntityRelation:
      #   init
        start_time : str = any
        end_time : str = any
        direction : str = any
        status : str = com.ProcesStatus.Null
        SubjectList : list = any
        


class LastEntityRelation:
        uid : str = any
        source : str = any
        destination : str = any
        config : str = any
        option : str = any
        CurentRelation : CurentEntityRelation = any
        LastRelation :list = any



class SubjectItem:
      # init
      '''create right init here'''
      name: str = any
      value: str = any
      type: str = any
      
class TotalRelation:
    def __init__(self, uid, type, time, RelationNumber):
        self.uid=uid
        self.type=type
        self.time = time
        self.RelationNumber= RelationNumber