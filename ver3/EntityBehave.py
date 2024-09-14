import json
import os
from datetime import datetime
import CommonFunction as com
import math
import Entity
import copy
from dateutil import parser



class V2RelationBehave():
    def New(self,Surce,Desi):
        
        """
        uid = com.Common_UID.new(Surce + Desi)
        start_time = com.Common_Time.Now()
        null_relation = Entity.CurentEntityRelation(
            start_time=start_time,
            end_time=start_time,
            direction=Entity.RelationDirection.InActive,
            status=Entity.RelationStatus.null,
            SubjectList=[]
        )
        # Initialize a new LastEntityRelation with the null relation
        self.last_entity_relation = Entity.LastEntityRelation(  #  for this we shoulld did one of 3 solution
            uid=uid,
            source=Surce,
            destination=Desi,
            CurentRelation=null_relation
        )
        self.Save(null_relation)  # Save the new relation to storage
        return null_relation
        """
    

     #    new_relation = Entity.CurentEntityRelation(uid, Surce, Desi, Entity.RelationDirection.InActive, com.ProcesStatus.Default, 
     #                                         start_time, start_time, Entity.RelationStatus.null, com.ProcesStatus.Null, 
     #                                         com.ProcesStatus.Default)
        #self.Save(new_relation)
        #return new_relation

    def Update(self,CurentRelation):
          #def active(none, passive):
               if self. curentdirection==com.ProcesStatus.none:
                    match self.direction: 
                         case com.ProcesStatus.inactive:
                              if CurentRelation. direction == com.ProcesStatus.inactive:
                                   self.EndTime= CurentRelation.EndTime
                                   #CurentRelation.status= com.ProcesStatus.passive
                              elif CurentRelation. direction == com.ProcesStatus.disver or CurentRelation. direction == com.ProcesStatus.conver:
                                   self.direction_history.append({
                                        "type": CurentRelation.direction,
                                        "EndTime": CurentRelation.EndTime
                                        })

                         case com.ProcesStatus.conver:  #ghabl active bashe
                              if CurentRelation. direction == com.ProcesStatus.inactive:
                                   self.direction_history.append({
                                        "type": CurentRelation.direction,
                                        "EndTime": CurentRelation.EndTime
                                        })

                                   self.status = com.ProcesStatus.passive
                                   self.EndTime= CurentRelation.EndTime

                              elif CurentRelation.direction==com.ProcesStatus.disver:
                                   self.direction_history.append({
                                        "type": CurentRelation.direction,
                                        "EndTime": CurentRelation.EndTime
                                        })
                                   self.status=com.ProcesStatus.active
                                   self.EndTime= CurentRelation.EndTime

                         case com.ProcesStatus.disver:
                              if CurentRelation. direction == com.ProcesStatus.inactive:
                                   self.direction_history.append({
                                        "type": CurentRelation.direction,
                                        "EndTime": CurentRelation.EndTime
                                        })

                                   self.status = com.ProcesStatus.passive
                                   self.EndTime= CurentRelation.EndTime

                              elif CurentRelation.direction==com.ProcesStatus.conver:
                                   self.direction_history.append({
                                        "type": CurentRelation.direction,
                                        "EndTime": CurentRelation.EndTime
                                        })
                                   self.status=com.ProcesStatus.active
                                   self.EndTime= CurentRelation.EndTime

          # if CurentRelation.direction == self.direction:
          #     self.EndTime= CurentRelation.EndTime
          # elif CurentRelation.direction!= self.direction:
          #      self.direction_history.append({
          #       "type": CurentRelation.direction,
          #       "EndTime": CurentRelation.EndTime
          #   })
              
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
     def __init__(self, Surce, Desi,covarcnf:Entity.CovarCnf) -> None:

          self.Surce=Surce
          self.Desi=Desi
          self.covarcnf=covarcnf

          # self.uid = com.Common_UID.new(Surce+Desi)
          # self.ibehave = V2RelationBehave()

          # self.CurentRelation = self.ibehave.Get(self.uid)

          # if self.CurentRelation == com.ProcesStatus.Null:
          #      self.CurentRelation = self.ibehave.New(Surce,Desi)
          #      self.CurentRelation = self.ibehave.Save(self.CurentRelation)
          
          self.DataProperty1=com.ProcesStatus.Null
          self.DataProperty2=com.ProcesStatus.Null
          self.combined_data = [[None, None] for _ in range(86400)]
          self.candidate_data=[]
          self.syncdata=[]

          self.last_relation = None  
          #self.current_relation = None 
          # self.last_entity_relation = Entity.LastEntityRelation()
          # self.current_entity_relation=Entity.CurentEntityRelation()

          self.last_entity_relation=None
          self.current_entity_relation=None
          

          # self.last_entity_relation.LastRelation.append(self.current_entity_relation)
          
          self.IdealMinTime=15
          self.StartProcess()
          #self.StartProcess2()
          
          self.combi1 = []
          self.combi2 = []
          
     def StartProcess(self):
          print("start process called")
          DataProperty1 = self.getData(self.Surce)
          DataProperty2 = self.getData(self.Desi)

          self.setDataToArray(DataProperty1,DataProperty2)
         
          #print(self.combined_data)
          start_sec,now_sec=self.createSyncTimeFrame()
          #print(start_sec,now_sec)
          self.CreateCandidateData(start_sec,now_sec)
          print(self.candidate_data)
          cov=self.covariance()
          self.cov=cov
          # check 
          #self.direction_range() 
          self.create_current_relation()
          self.check_status()

          # starttime = self.time_to_seconds()
          # self.OptimizeBlankRange(0)
          # self.OptimizeBlankRange(1)
          # endtime = self.time_to_seconds()
          # print("endtime-starttime:",endtime-starttime)
          # com.FileControl.SaveJson("D:/JsonData/tests/data1","data5.json", self.combined_data)
          # self.StartProcess2(0)
          # self.StartProcess2(1)

     def StartProcess2(self,index):
          tsom=0
          for i in range(0, len(self.combined_data)):
               if self.combined_data[i][index] is not None:
                    tsom+=self.combined_data[i][index]
          print(tsom)

     def CheckData(PropOption):
          #if com.Common_Time.Now == PropOption.ut:


          pass
          #if com.Common_Time.Now ==   

     def getData(self,uid):
          params = {"UID": uid,
                    "date": datetime.now().replace(microsecond=0)  
               }
          response = com.RequestHandler.getRequest(com.CommonConfig.objvalue_url, params=params)
          #print(response)
          return response
     
     def time_to_seconds(self,date_time_str=None):
          try:
               if date_time_str is None:
                    dt=datetime.now()
               else:
                    if not isinstance(date_time_str, str):
                         date_time_str = str(date_time_str)
                    dt = parser.parse(date_time_str)

               return dt.hour * 3600 + dt.minute * 60 + dt.second
          except (ValueError, parser.ParserError) as e:
               print(f"Error parsing time string '{date_time_str}': {e}")
               return None
          
     def setDataToArray(self, data1, data2):

          self.FillArray(data1,0)
          self.FillArray(data2,1)

     def FillArray(self, data, index):
          for entry in data:
               et_seconds = self.time_to_seconds(entry.get('et'))
               ut_seconds = self.time_to_seconds(entry.get('ut'))
               value = float(entry.get('va'))
               for j in range (et_seconds, ut_seconds+1):
                self.combined_data[j][index]=value

     def CreateCandidateData(self,start,now):
          for i in range(start, now):
               if self.combined_data[i][0]!=None and self.combined_data[i][1] != None:
                    self.candidate_data.append([self.combined_data[i][0], self.combined_data[i][1], i])

     def createSyncTimeFrame(self):
          CurrentTime= com.Common_Time.Now()
          NowSec=self.time_to_seconds(CurrentTime)
          len(self.combined_data)
          StartSecTime=NowSec-(self.IdealMinTime*60)
          return StartSecTime,NowSec
          #self.syncdata=self.combined_data[StartSecTime:NowSec]
          #return syncdata

     def covariancever1(self,):
        DataProperty1=[]
        DataProperty2=[]
        DataSum1=0
        DateSum2=0
        totalSum=0
        k=0
        for i in range(len(self.candidate_data)):
               DataProperty1.append(self.candidate_data[i][0])   
               DataProperty2.append(self.candidate_data[i][1])
               count1=len(DataProperty1)
               count2=len(DataProperty2)
               #len(data1)==len(data2)?==len(syncdata)?
        for j in range(len(DataProperty1)):
                DataSum1+=DataProperty1[j]
                DateSum2+=DataProperty2[j]
        avg1 =DataSum1/len(DataProperty1)
        avg2 =DateSum2/len(DataProperty2)
        for k in range(len(self.DataProperty1)):              
            multiply= ((DataProperty1[k]-avg1) * (DataProperty2[k]-avg2) )
            totalSum+= multiply
        cov= totalSum/(len(self.candidate_data)-1)
        print(cov)
        return cov

     def covariance(self):
          DataProperty1=[]
          DataProperty2=[]
          for i in range(len(self.candidate_data)):
               DataProperty1.append(self.candidate_data[i][0])   
               DataProperty2.append(self.candidate_data[i][1])
               count1=len(DataProperty1)
               count2=len(DataProperty2)
               #len(data1)==len(data2)?==len(syncdata)?

          totalSum=self.DataSum(DataProperty1,DataProperty2,len(DataProperty1),len(DataProperty2))
          cov= totalSum/(len(self.candidate_data)-1)
          print(cov)
          return cov

     def DataSum(self,data1,data2,length1,length2):
          DataSum1=0
          DataSum2=0
          for j in range(len(data1)):
               DataSum1+=data1[j]
               DataSum2+=data2[j]

          avg1=com.calculation.calculate_average(DataSum1,length1)
          avg2= com.calculation.calculate_average(DataSum2,length2)
          totalSum=self.Deviation(length1, data1,data2, avg1,avg2)
          return totalSum
     
     def Deviation(self,length1,DataProperty1,DataProperty2,avg1,avg2 ):
          totalSum=0
          for k in range(length1):              
               multiply= ((DataProperty1[k]-avg1) * (DataProperty2[k]-avg2))
               totalSum+= multiply
          return totalSum

     def create_current_relation(self):
          # ??
          """create or update the curent relation"""

          while(True):
               if self.last_entity_relation is None:
               # If there is no previous relation, create a null relation
                    uid = com.Common_UID.new(self.Surce + self.Desi)
                    start_time = com.Common_Time.Now()
                    self.current_entity_relation = Entity.CurentEntityRelation(
                         start_time=start_time,
                         end_time=start_time,
                         direction=Entity.RelationDirection.InActive,
                         status=Entity.RelationStatus.null,
                         SubjectList=[]
                    )
               # Initialize a new LastEntityRelation with the null relation                
                    self.last_entity_relation = Entity.LastEntityRelation(
                         uid=uid,
                         source=self.Surce,
                         destination=self.Desi,
                         CurentRelation=copy.deepcopy(self.current_entity_relation),
                         LastRelation=[]
                    )
               #self.Save(se)
               else:
                    new_current_relation = copy.deepcopy(self.current_entity_relation)
                    new_current_relation.direction = self.direction_range()
               #while self.last_entity_relation.CurentRelation:
                    self.current_entity_relation.direction=self.direction_range()
                    if self.last_entity_relation.CurentRelation.direction!= new_current_relation.direction:
                         self.last_entity_relation.LastRelation.append(copy.deepcopy(self.last_entity_relation.CurentRelation))
                         self.current_entity_relation=Entity.CurentEntityRelation(
                              start_time=com.Common_Time.Now(),
                              end_time=com.Common_Time.Now(),
                              direction=self.direction_range(),  
                              status=Entity.RelationStatus.Active,
                              SubjectList=[]
                         )
                         CovarianceItem = Entity.SubjectItem(name="Covariance", value=self.cov, type="float")
                         self.current_entity_relation.SubjectList.append(CovarianceItem)
                         self.last_entity_relation.CurentRelation = copy.deepcopy(new_current_relation)
                         self.check_status()
                         break                    
               #else:                  
          self.Save(self.last_entity_relation)

     def direction_range(self):
          # create Entity for parameter
          if self.cov> self.covarcnf.Convergent:
               return Entity.RelationDirection.Convergent
          if self.cov<-self.covarcnf.Divergent:
               return Entity.RelationDirection.Divergent
          else:
               return Entity.RelationDirection.InActive

     def check_status(self):

          print(self.last_entity_relation.LastRelation)
          for relation in self.last_entity_relation.LastRelation:
               #print(relation.status)
               if relation.direction ==Entity.RelationDirection.InActive and \
                    self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.null:
                         self.state1()


               elif relation.direction==Entity.RelationDirection.InActive and \
                    self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.Pasive:
                         self.state2()

               elif relation.direction ==Entity.RelationDirection.Divergent and \
                    self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.Active:
                         self.state3()

               elif relation.direction ==Entity.RelationDirection.Convergent and \
                    self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.Active:
                         self.state4()
                    
     def state1(self):     
          if self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               self.state3()
               
          elif self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               self.state4()

          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status= Entity.RelationStatus.null
               self.update1()
               self.state1      

     def state2(self):
          if self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               self.state3()
          elif self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               self.state4()
          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status= Entity.RelationStatus.Pasive
               self.update1()
               self.state2    

     def state3(self):
          if self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               self.state4()
          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status = Entity.RelationStatus.Pasive
               self.update2()
               self.state2()

          elif self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status= Entity.RelationStatus.Active
               self.update1()
               self.state3    

     def state4(self):
          if self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               self.state3()
          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status = Entity.RelationStatus.Pasive
               self.update2()
               self.state2()

          elif self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status= Entity.RelationStatus.Active
               self.update1()
               self.state4    

     def update1(self):
          self.last_entity_relation.CurentRelation.end_time=com.Common_Time.Now()
          self.Save(self.last_entity_relation)
          #update time
          #zakhire last

     def update2(self):
          self.last_entity_relation.LastRelation.append(self.last_entity_relation.CurentRelation)
          #  update start time with last end time
          self.last_entity_relation.CurentRelation=self.current_entity_relation
          self.Save(self.last_entity_relation)
          # last current to last last
          #curent to curent last
          
     def default_serializer(self,obj):
          if isinstance(obj, datetime):
               return obj.isoformat()
          elif isinstance(obj, Entity.CurentEntityRelation):
        # Convert the custom object to a dictionary
               return {
                    'start_time': obj.start_time.isoformat() if isinstance(obj.start_time, datetime) else obj.start_time,
                    'end_time': obj.end_time.isoformat() if isinstance(obj.end_time, datetime) else obj.end_time,
                    'direction': obj.direction,  # Assuming this is a serializable attribute
                    'status': obj.status,        # Assuming this is a serializable attribute
                    'SubjectList': [self.default_serializer(item) for item in obj.SubjectList]   # Assuming this is serializable
               }
          elif isinstance(obj, Entity.SubjectItem):
        # Convert SubjectItem to a dictionary
               return {
                    'name': obj.name,
                    'value': obj.value,
                    'type': obj.type
               }
          else:
               raise TypeError(f"Type {type(obj)} not serializable")
     

     def Save(self, CurentRelation , path='D:/EachEntityRelation2'):
            if not os.path.exists(path):
               os.makedirs(path)
            filename = com.Common_UID.new(self.Surce + self.Desi) + '.json'
            with open(os.path.join(path,filename), 'w') as file:
               json.dump(CurentRelation.__dict__, file, default=self.default_serializer,indent=4)
        
            return CurentRelation
     
     def custom_parser(self,dct):
          for key, value in dct.items():
               if isinstance(value, str):
                    try:
                         # Try to parse the string into a datetime object
                         dct[key] = parser.isoparse(value)
                    except (ValueError, parser.ParserError):
                         # If parsing fails, leave the value as is
                         pass
          return dct

     def load_json_with_dates(self,file_path):
          with open(file_path, 'r') as file:
               data = json.load(file, object_hook=self.custom_parser)  # Use the custom parser
          return data


     def checkLastRelationStatus():
          pass
     def changeStatus(self,CurentRelation,LastRelation):
          self.CurentRelation.direction_history.append({
                                        "type": CurentRelation.direction,
                                        "EndTime": CurentRelation.EndTime
                                        })
                
     def updateLastStatus():
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

# iV2RelationStatus = V2RelationStatus('A','B')
# MyTestRelarion = iV2RelationStatus.CurentRelation

#print('Step 1:',curenttestUID)
# print('Step 2:',GetTestRelation)
#print('Step StartTime:',MyTestRelarion['StartTime'])

class RelationMatrix():
     def getAllProperty():
          pass


     def evaluateData(self, curentRelation):
          if curentRelation.EndTime.day==com.Common_Time.Now.day:
               return True
          else:
               return com.ProcesStatus.eval_false_data
          
if __name__=="__main__":
     SurceUID = "HDB25SCC54Y32SD556VR6RD1S6N63KOH8"
     DesiUID = "38116L4OS4256W00S60GT08TIOV75L346"
     covarcnf=Entity.CovarCnf()
     RelationStatus=V2RelationStatus(SurceUID, DesiUID,covarcnf)
     #test=RelationStatus.StartProcess()
     #print(test)
