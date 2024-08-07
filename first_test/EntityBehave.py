import json
import os
from datetime import datetime
import CommonFunction as com
import Entity


class V2RelationBehave():
    def New(self,Surce,Desi):
        uid = com.Common_UID.new(Surce+Desi)
        start_time = com.Common_Time.Now()
        new_relation = Entity.EntityRelation(uid, Surce, Desi, com.ProcesStatus.Null, com.ProcesStatus.Default, 
                                             start_time, start_time, com.ProcesStatus.Null, com.ProcesStatus.Null, 
                                             com.ProcesStatus.Default)
        self.Save(new_relation)
        return new_relation

    def Update(self,CurentRelation):
        pass

    def Get(self, UID , path='D:/EachEntityRelation'):
         try:
            with open(os.path.join(path,UID+'.json'), 'r') as file:
                    CurentRelation = json.load(file)
         except:
              CurentRelation = com.ProcesStatus.Null
            
         return CurentRelation

    def Remove(self,UID):
        pass

    def Save(self, CurentRelation , path='D:/EachEntityRelation'):
            with open(os.path.join(path,CurentRelation.uid+'.json'), 'w') as file:
                json.dump(CurentRelation.__dict__, file)
        
            return CurentRelation
    
class V2RelationStatus():
     def __init__(self,Surce,Desi) -> None:
          self.uid = com.Common_UID.new(Surce+Desi)
          self.ibehave = V2RelationBehave()
          self.CurentRelation = self.ibehave.Get(self.uid)

          if self.CurentRelation == com.ProcesStatus.Null:
               self.CurentRelation = self.ibehave.New(Surce,Desi)
               self.CurentRelation = self.ibehave.Save(self.CurentRelation)

     def checkProRelation():
          pass
     
     def getDataLog():
          pass
        
     def CreateTimeFrame():
          pass
        

class V2RelationStatusV2(V2RelationStatus):
     def __init__(self,uid) -> None:
          self.uid = uid
          self.ibehave = V2RelationBehave()
          self.CurentRelation = self.ibehave.Get(self.uid)
          super().__init__(self.CurentRelation['source'], self.CurentRelation['destination'])

iV2RelationStatus = V2RelationStatus('A','B')
MyTestRelarion = iV2RelationStatus.CurentRelation

# print('Step 1:',curenttestUID)
# print('Step 2:',GetTestRelation)
print('Step StartTime:',MyTestRelarion['StartTime'])
