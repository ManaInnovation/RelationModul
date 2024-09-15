import json
import os
from datetime import datetime
import CommonFunction as com
import uuid


class V2RelationStatus():

    uid_watt = "6PEW67J130A4J262J246R7K671UJ0FJ40"
    uid_ampere = "011W72B147CW0KV08O55GA2MTX5X4HDK4"
    timestamp = "2024-07-27 11:58:23"
    base_url = "http://www.asset23d.ir/api/OBJVALUE"

    def __init__(self):
        self.combined_data=[[None, None],[None, None],[7, None],[None, None],[5, None],[None, None],[None, None],
                            [None, None],[0, None],[None, None],[15, None],[17, None],[None, None],[None, None],[None, None],[None, None],[20, None],[None, None]]
          
          
        self.StartProcess()

    def StartProcess(self):

          #combined_data = [[None, None] for _ in range(86400)]
        exe=self.new("example")
        exe2=self.new("hello")
        print(exe+exe2)
        #self.FindBlankRange(1)
        #print(datetime.now())

    class CurentEntityRelation:
      def __init__(self,start_time:str=com.Common_Time.Now(),end_time:str=com.Common_Time.Now(),
                   direction: str = RelationDirection.InActive,status: str = RelationStatus.null,SubjectList:list=com.ProcesStatus.Null):
        self.start_time = start_time
        self.end_time =end_time
        self.direction =direction
        self.status = status
        self.SubjectList = SubjectList if SubjectList else []

      def to_dict(self):
        return {
            "start_time": self.start_time.isoformat() if isinstance(self.start_time, datetime) else self.start_time,
            "end_time": self.end_time.isoformat() if isinstance(self.end_time, datetime) else self.end_time,
            "direction": self.direction,
            "status": self.status,
            "SubjectList": self.SubjectList
        }

      @classmethod
      def from_dict(cls, data):
        return cls(
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            direction=data.get("direction"),
            status=data.get("status"),
            SubjectList=data.get("SubjectList", [])
        )
              
if __name__=="__main__":
    RelationStatus=V2RelationStatus()
    #test=RelationStatus.StartProcess()