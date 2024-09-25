import json
import os
from datetime import datetime
import CommonFunction as com
import math
import Entity
import copy
from dateutil import parser
import pickle
import statistics
import time
import schedule

IdealMinTime=5


class V2RelationBehave():
    def New(self,Surce,Desi):
          uid = com.Common_UID.new(Surce + Desi)
          path='D:/EachEntityRelation2'
          file_name = os.path.join(path, uid + '.json')
          if not os.path.exists(file_name):
               new_relation = Entity.CurentEntityRelation(
                    start_time=com.Common_Time.Now(),  
                    end_time=com.Common_Time.Now(),    
                    direction=Entity.RelationDirection.InActive,
                    status=Entity.RelationStatus.null,  
                    SubjectList=[]  
               )
               self.last_entity_relation = Entity.LastEntityRelation(
                              uid=com.Common_UID.new(Surce + Desi),
                              source=Surce,
                              destination=Desi,
                              CurentRelation=new_relation,
                              LastRelation=[]
                              
                         )
               self.Save(self.last_entity_relation )              
          else:
               self.last_entity_relation = self.Get(Surce, Desi, path)
               if self.last_entity_relation != com.ProcesStatus.Null:
                    new_relation = self.last_entity_relation.CurentRelation
               else:
                    new_relation = com.ProcesStatus.Null

          return new_relation

    def Remove(self,UID):
        pass
          
    def Save(self, CurentRelation , path='D:/EachEntityRelation2'):
          # if not os.path.exists(path):
          #      os.makedirs(path)
          dir_path = os.path.dirname(os.path.realpath(__file__))
          file_name = os.path.join(dir_path, CurentRelation.uid + '.json')
          with open(file_name, 'w') as file:
               json.dump(CurentRelation, file, default=self.default_serializer,indent=4)
     
          return CurentRelation
    
    def default_serializer(self, obj, seen=None):
     if isinstance(obj, datetime):
          return obj.isoformat()
     elif isinstance(obj, Entity.CurentEntityRelation):
          return {
               'start_time': obj.start_time.isoformat() if isinstance(obj.start_time, datetime) else obj.start_time,
               'end_time': obj.end_time.isoformat() if isinstance(obj.end_time, datetime) else obj.end_time,
               'direction': obj.direction,
               'status': obj.status,
               'SubjectList': [self.default_serializer(item, seen) for item in obj.SubjectList]
          }
     elif isinstance(obj, Entity.SubjectItem):
          return {
               'name': obj.name,
               'value': obj.value,
               'type': obj.type
          }
     elif isinstance(obj, Entity.LastEntityRelation):
          return {
               'uid': obj.uid,
               'source': obj.source,
               'destination': obj.destination,
               'config': obj.config,
               'option': obj.option,
               'CurentRelation': self.default_serializer(obj.CurentRelation, seen),
               'LastRelation': [self.default_serializer(rel, seen) for rel in obj.LastRelation]
          }
     else:
          raise TypeError(f"Type {type(obj)} not serializable")


    def Get(self, Surce, Desi, path='D:/EachEntityRelation2'):
         uid = com.Common_UID.new(Surce + Desi)
         file_name = os.path.join(path, uid + '.json')
         try:
               with open(file_name, 'r') as file:

                    data = json.load(file)
               
                    curent_relation_data = data.get('CurentRelation', {})
                    CurentRelation = self.reconstruct_curent_entity_relation(curent_relation_data) #dict to object
                    last_relation_data = data.get('LastRelation', [])
                    LastRelation = [self.reconstruct_curent_entity_relation(rel) for rel in last_relation_data]
                    last_entity_relation = Entity.LastEntityRelation(
                uid=data.get('uid'),
                source=data.get('source'),
                destination=data.get('destination'),
                config=data.get('config'),
                option=data.get('option'),
                CurentRelation=CurentRelation,
                LastRelation=LastRelation
            )
         except FileNotFoundError:
               print(f"File not found: {file_name}")  # Debugging line
               last_entity_relation = com.ProcesStatus.Null
         except json.JSONDecodeError as e:
               print(f"JSON decode error: {e}")  
               last_entity_relation = com.ProcesStatus.Null
         except Exception as e:
               print(f"Unexpected error: {e}")  
               last_entity_relation = com.ProcesStatus.Null
          
         return last_entity_relation
    def reconstruct_curent_entity_relation(self,data):
          return Entity.CurentEntityRelation(
               start_time=parser.isoparse(data.get('start_time')) if 'start_time' in data else None,
               end_time=parser.isoparse(data.get('end_time')) if 'end_time' in data else None,
               direction=data.get('direction'),
               status=data.get('status'),
               SubjectList=[self.reconstruct_subject_item(item) for item in data.get('SubjectList', [])]
          )

    def reconstruct_subject_item(self,data):
          return Entity.SubjectItem(
               name=data.get('name'),
               value=data.get('value'),
               type=data.get('type')
          )

class V2RelationStatus():
     def __init__(self, Surce, Desi,covarcnf:Entity.CovarCnf) -> None:

          self.Surce=Surce
          self.Desi=Desi
          self.covarcnf=covarcnf
          self.cov=None
     
          self.DataProperty1=com.ProcesStatus.Null
          self.DataProperty2=com.ProcesStatus.Null
          self.combined_data = [[None, None] for _ in range(86400)]
          self.candidate_data=[]  

          self.MyBehave=V2RelationBehave()
         
          self.current_entity_relation=self.MyBehave.New(self.Surce,self.Desi)
          self.last_entity_relation=self.MyBehave.Get(self.Surce, self.Desi)
              
          
          
     def StartProcess(self):
          DataProperty1 = self.getData(self.Surce)
          DataProperty2 = self.getData(self.Desi)

          self.setDataToArray(DataProperty1,DataProperty2)
     
          start_sec,now_sec=self.createSyncTimeFrame()
          self.CreateCandidateData(start_sec,now_sec)
          self.covariance()
          self.create_current_relation_v1()
     
  

     def getData(self,uid):
          params = {"UID": uid,
                    "date": datetime.now().replace(microsecond=0)  
               }
          response = com.RequestHandler.getRequest(com.CommonConfig.objvalue_url, params=params)
          #print(response)
          return response
     
          
     def setDataToArray(self, data1, data2):

          self.FillArray(data1,0)
          self.FillArray(data2,1)

     def FillArray(self, data, index):
          for entry in data:
               et_seconds = com.Common_Time.time_to_seconds(entry.get('et'))
               ut_seconds = com.Common_Time.time_to_seconds(entry.get('ut'))
               va = entry.get('va')
               if va is not None:
                    try:
                         value = float(va)
                    except ValueError:
                         value = None  
                         print(f"Warning: 'va' value '{va}' is not a valid float.")
               else:
                    value = None 
               for j in range (et_seconds, ut_seconds+1):
                self.combined_data[j][index]=value

     def CreateCandidateData(self,start,now):
          for i in range(start, now):
               if self.combined_data[i][0]!=None and self.combined_data[i][1] != None:
                    self.candidate_data.append([self.combined_data[i][0], self.combined_data[i][1], i])

     def createSyncTimeFrame(self):
          CurrentTime= com.Common_Time.Now()
          NowSec=com.Common_Time.time_to_seconds(CurrentTime)
          len(self.combined_data)
          StartSecTime=NowSec-(IdealMinTime*60)
          return StartSecTime,NowSec
          
     def covariance(self):
        if not self.candidate_data:
          print("No data available for covariance calculation.")
          return None
        DataProperty1=[]
        DataProperty2=[]
        totalSum=0
        k=0
        for i in range(len(self.candidate_data)):
               value1 = self.candidate_data[i][0]
               value2 = self.candidate_data[i][1]
        
               if value1 is not None and value2 is not None:
                    DataProperty1.append(value1)
                    DataProperty2.append(value2)

        if len(DataProperty1) < 2 or len(DataProperty2) < 2:
          print("Not enough data points to compute covariance.")
          return None

        avg1 =statistics.mean(DataProperty1)
        avg2 =statistics.mean(DataProperty2)

        for k in range(len(self.candidate_data)):              
            multiply= ((DataProperty1[k]-avg1) * (DataProperty2[k]-avg2) )
            totalSum+= multiply
        self.cov= totalSum/(len(self.candidate_data)-1)

     def create_current_relation_v0(self):               
               if self.last_entity_relation == com.ProcesStatus.Null:
                    self.MyBehave.New(self.Surce,self.Desi)
          
               else:
                    new_current_relation = copy.deepcopy(self.current_entity_relation)
                    new_current_relation.direction = self.direction_range()
          
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
                         print(self.current_entity_relation)

                         self.check_status()    
                    else:
                         self.update1()


     def create_current_relation(self):               
               if self.last_entity_relation == com.ProcesStatus.Null:
                    self.MyBehave.New(self.Surce,self.Desi)
          
               else:

                    self.current_entity_relation.direction = self.direction_range()
          
                    if self.last_entity_relation.CurentRelation.direction!= self.current_entity_relation.direction:
                         self.last_entity_relation.LastRelation.append(copy.deepcopy(self.last_entity_relation.CurentRelation))
                         self.current_entity_relation.status=Entity.RelationStatus.Active
                         self.current_entity_relation.start_time=self.last_entity_relation.CurentRelation.end_time

                         CovarianceItem = Entity.SubjectItem(name="Covariance", value=self.cov, type="float")
                         self.current_entity_relation.SubjectList.append(CovarianceItem)
                         print(self.current_entity_relation)

                         self.check_status()    
                    else:
                         self.update1()

     def create_current_relation_v1(self):               
               if self.last_entity_relation == com.ProcesStatus.Null:
                    self.MyBehave.New(self.Surce,self.Desi)
          
               else:
                    self.current_entity_relation.direction = self.direction_range()
          
                    if self.last_entity_relation.CurentRelation.direction!= self.current_entity_relation.direction:
                         self.last_entity_relation.LastRelation.append(copy.deepcopy(self.last_entity_relation.CurentRelation))
                         self.current_entity_relation=Entity.CurentEntityRelation(
                              start_time=self.last_entity_relation.CurentRelation.end_time,
                              end_time=com.Common_Time.Now(),
                              direction=self.direction_range(),  
                              status=Entity.RelationStatus.Active,
                              SubjectList=[]
                         )
                         CovarianceItem = Entity.SubjectItem(name="Covariance", value=self.cov, type="float")
                         self.current_entity_relation.SubjectList.append(CovarianceItem)
                         print(self.current_entity_relation)

                         self.check_status()    
                    else:
                         self.update1()

     def direction_range(self):
          if self.cov == None:
               return Entity.RelationDirection.InActive
          if self.cov >= self.covarcnf.Convergent:
               return Entity.RelationDirection.Convergent
          if self.cov <= self.covarcnf.Divergent:
               return Entity.RelationDirection.Divergent
          if self.covarcnf.Divergent<self.cov<self.covarcnf.Convergent:
               return Entity.RelationDirection.InActive

     def check_status(self):
               if self.last_entity_relation.LastRelation:
                    if self.last_entity_relation.LastRelation[-1].direction ==Entity.RelationDirection.InActive and \
                         self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.null:
                              self.state1()


                    elif self.last_entity_relation.LastRelation[-1].direction==Entity.RelationDirection.InActive and \
                         self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.Pasive:
                              self.state2()

                    elif self.last_entity_relation.LastRelation[-1].direction ==Entity.RelationDirection.Divergent and \
                         self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.Active:
                              self.state3()

                    elif self.last_entity_relation.LastRelation[-1].direction ==Entity.RelationDirection.Convergent and \
                         self.last_entity_relation.CurentRelation.status==Entity.RelationStatus.Active:
                              self.state4()
                         
     def state1(self):     
          if self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               
               
          elif self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               

          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status= Entity.RelationStatus.null
               self.update1()
                     

     def state2(self):
          if self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               
          elif self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               
          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status= Entity.RelationStatus.Pasive
               self.update1()
     

     def state3(self):
          if self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               
          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status = Entity.RelationStatus.Pasive
               self.update2()
               

          elif self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status= Entity.RelationStatus.Active
               self.update1()
                 

     def state4(self):
          if self.current_entity_relation.direction == Entity.RelationDirection.Divergent:
               self.current_entity_relation.status = Entity.RelationStatus.Active 
               self.update2()
               
          elif self.current_entity_relation.direction == Entity.RelationDirection.InActive:
               self.current_entity_relation.status = Entity.RelationStatus.Pasive
               self.update2()
               

          elif self.current_entity_relation.direction == Entity.RelationDirection.Convergent:
               self.current_entity_relation.status= Entity.RelationStatus.Active
               self.update1()
                  

     def update1(self):
          self.last_entity_relation.CurentRelation.end_time=com.Common_Time.Now()
          #lastcov=self.last_entity_relation.CurentRelation.SubjectList[-1].value

          if self.last_entity_relation.CurentRelation.SubjectList[-1].value !=self.cov:
               CovarianceItem = Entity.SubjectItem(name="Covariance", value=self.cov, type="float")
               self.current_entity_relation.SubjectList.append(CovarianceItem)
          self.current_entity_relation.end_time=com.Common_Time.Now()
          self.last_entity_relation.CurentRelation=copy.deepcopy(self.current_entity_relation)
          self.MyBehave.Save(self.last_entity_relation)

     def update2(self):
          self.last_entity_relation.CurentRelation=copy.deepcopy(self.current_entity_relation)
          # self.current_entity_relation.start_time=self.last_entity_relation.CurentRelation.end_time
          self.MyBehave.Save(self.last_entity_relation)
     
       
class V2RelationMatrix():
     def __init__(self,) -> None:
          self.property_list=[]
          self.ValidUt=[]
          self.Array3d=[]
         

     def StartProcess(self):
          self.GetPropertyList()
          self.EvaluateData()
          self.Matrix()

          
     def GetPropertyList(self,):
          response=self.GetData()
          CheckObjResponse,objResponse=com.RequestHandler.CheckCmdResponseIsExist(response, com.CommonConfig.PropObj,com.CommonConfig.TypePropObj)
          if CheckObjResponse==True:
               for prop_data in objResponse:
                    if isinstance(prop_data, dict):
                                prop = Entity.Property(
                                    id=prop_data.get('id'),
                                    object_id=prop_data.get('object_id'),
                                    field_id=prop_data.get('field_id'),
                                    field_relation_id=prop_data.get('field_relation_id'),
                                    prop_type=prop_data.get('type'),
                                    UID=prop_data.get('UID'),
                                    option=prop_data.get('option')
                                )
                                self.property_list.append(prop)
                    else:
                         print("Warning: Skipping non-dict item in finalObj")
             


     def GetData(self,):
          command = com.CommonConfig.getPropertyListCmd
          response = com.RequestHandler.postRequest(com.CommonConfig.cmd_url, headers=com.CommonConfig.headers
                                                         , data=json.dumps(command))
         
          return response

     def EvaluateData(self):
          for prop in self.property_list:
                if hasattr(prop, 'option') and prop.option not in [None, "NULL"]:
                    option_data = json.loads(prop.option)
                    if 'ut' in option_data:
                         CheckRange=self.CheckUt(option_data['ut'])
                         if CheckRange==True:
                              self.ValidUt.append([prop.id,prop.UID,option_data['ut']])

          
     def CheckUt(self,ut_str):
          ut_dateItime=com.Common_Time.ParseStringToDateTime(ut_str)
          if isinstance(ut_dateItime, datetime) and ut_dateItime.date() == com.Common_Time.Now().date():
               CurrentTime= com.Common_Time.Now()
               NowSec=com.Common_Time.time_to_seconds(CurrentTime)
               StartSecTime=NowSec-(IdealMinTime*60)

               UtSecond=com.Common_Time.time_to_seconds(ut_dateItime)

               if UtSecond<=NowSec and UtSecond>=StartSecTime:
                return True
                
     def Matrix(self):
          num_items = len(self.ValidUt)
          if len(self.ValidUt)>1:
               for i in range (num_items):
                    uid_i = self.ValidUt[i][1]
                    for j in range(i+1,num_items):
                         uid_j=self.ValidUt[j][1]
                         self.RelationStatus=V2RelationStatus(uid_i,uid_j,covarcnf)
                         self.RelationStatus.StartProcess()

                         self.Array3d.append([uid_i,uid_j,self.RelationStatus.current_entity_relation.direction])
                         self.SaveMatrix(self.Array3d)

          # print(self.Array3d)
     
     def SaveMatrix(self, Array3d , path='D:/EachEntityRelation3'):
          #uid = com.Common_UID.new(Surce + Desi)
          dir_path = os.path.dirname(os.path.realpath(__file__))

          # if not os.path.exists(path):
          #      os.makedirs(path)
          file_name = os.path.join(dir_path ,'relationmatrix.json')
          try:
               with open(file_name, 'w') as file:
                    json.dump(Array3d, file)
          except IOError as e:
               print(f"An error occurred while saving the matrix: {e}")
          
          #return CurentRelation
     
def run_tasks():
    current_time = datetime.now()
    start_time = datetime.now().replace(hour=16, minute=1, second=0, microsecond=0)  # Start time
    end_time = datetime.now().replace(hour=16, minute=52, second=0, microsecond=0)    # End time

  
    if start_time <= current_time <= end_time:
        print(f"Running tasks at {current_time}")

        relation_matrix = V2RelationMatrix()
        relation_matrix.StartProcess()
    else:
        print(f"Out of time range at {current_time}. Stopping the scheduler.")
        return schedule.CancelJob  

job = schedule.every(1).minutes.do(run_tasks)


covarcnf=Entity.CovarCnf()

# if __name__=="__main__":
#      covarcnf=Entity.CovarCnf()

#      print("Scheduler started...")
#      while True:
#         schedule.run_pending() 
#         if job in schedule.jobs:
#             time.sleep(1)
#         else:
#             print("Job cancelled. Exiting program.")
#             break  # Exit the loop and stop the program
#      # SurceUID = "05A3V2270U1QS37ECU8CFJR7T4IB3GQ71"
#      # DesiUID = "T22LRCKDW3LL2J77560LD0382D3N5B10E"



# if __name__=="__main__":
#      # covarcnf=Entity.CovarCnf()

#      # print("Scheduler started...")
#      relation_matrix = V2RelationMatrix()
#      relation_matrix.StartProcess()

     