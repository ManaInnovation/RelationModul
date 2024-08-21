import json
import os
from datetime import datetime
import CommonFunction as com
import math
import Entity
from dateutil import parser



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

     uid_watt = "6PEW67J130A4J262J246R7K671UJ0FJ40"
     uid_ampere = "011W72B147CW0KV08O55GA2MTX5X4HDK4"
     timestamp = "2024-07-27 11:58:23"
     base_url = "http://www.asset23d.ir/api/OBJVALUE"

     def __init__(self, Surce, Desi) -> None:
          self.uid = com.Common_UID.new(Surce+Desi)
          self.ibehave = V2RelationBehave()
          self.CurentRelation = self.ibehave.Get(self.uid)

          if self.CurentRelation == com.ProcesStatus.Null:
               self.CurentRelation = self.ibehave.New(Surce,Desi)
               self.CurentRelation = self.ibehave.Save(self.CurentRelation)
          
          self.DataProperty1=com.ProcesStatus.Null
          self.DataProperty2=com.ProcesStatus.Null
          self.combined_data = [[None, None] for _ in range(86400)]
          
          self.IdealMinTime=15
          self.StartProcess()
          #self.StartProcess2()
          
          


     def StartProcess(self):
          
          # self.DataProperty1 = self.getData(self.CurentRelation['source'])
          # self.DataProperty2 = self.getData(self.CurentRelation['destination'])
          SurceUID = "6PEW67J130A4J262J246R7K671UJ0FJ40"
          DesiUID = "011W72B147CW0KV08O55GA2MTX5X4HDK4"
          DataProperty1 = self.getData(SurceUID)
          DataProperty2 = self.getData(DesiUID)

          self.setDataToArray(DataProperty1,DataProperty2)
          self.FindBlankRange(0)
          self.FindBlankRange(1)
          print(self.combined_data)
          smaller_array=self.createSyncTimeFrame(15)
          self.covariance(smaller_array)

          #smaller_array=self.createSyncTimeFrame(second_d,15)
          #print(smaller_array)
          #cov=self.covariance(smaller_array)
          #print(cov)
     
     def StartProcess2(self):
          pass



     def CheckData(PropOption):
          #if com.Common_Time.Now == PropOption.ut:


          pass
          #if com.Common_Time.Now ==   

     def getData(self,uid):
          params = {"UID": uid,# "date": com.Common_Time.Now() 
                    "date": "2024-07-27 12:12:12"
               }
          response = com.RequestHandler.getRequest(com.CommonConfig.objvalue_url, params=params)
          #print(response)
          return response
     
     def time_to_seconds(self,date_time_str=None):
          try:
               if date_time_str is None:
                    dt=datetime.now()
               else:
                    dt = parser.parse(date_time_str)

               return dt.hour * 3600 + dt.minute * 60 + dt.second
          except (ValueError, parser.ParserError) as e:
               print(f"Error parsing time string '{date_time_str}': {e}")
               return None
          
     
     def setDataToArray(self, data1, data2):

          for entry1 in data1:
               et_seconds1 = self.time_to_seconds(entry1.get('et'))
               ut_seconds1 = self.time_to_seconds(entry1.get('ut'))
               value1 = float(entry1.get('va'))
               for i in range (et_seconds1, ut_seconds1):
                self.combined_data[i][0]=value1
               #self.combined_data[ut_seconds1][0]=value1

          for entry2 in data2:
               et_seconds2 = self.time_to_seconds(entry2.get('et'))
               ut_seconds2 = self.time_to_seconds(entry2.get('ut'))
               value2 = float(entry2.get('va'))
               for j in range (et_seconds2, ut_seconds2):
                self.combined_data[j][1]=value2
               #self.combined_data[ut_seconds2][1]=value2
        
     def FindBlankRange(self,index):
        CheckTrigger = False
        narojelo=False
        last_full=None
        first_full = None
        first_blank = None
        last_blank = None
        finalDataBlock=86400
        data_length = len(self.combined_data)
        B=[]
        f=[]
        Count_blanks=[]
        count=0
        
        for i in range(0,data_length):
            if self.combined_data[i][index] is not None:
                    if CheckTrigger==False:
                        first_full=i
                        CheckTrigger=True
                        for j in range(first_full, data_length):
                              if self.combined_data[j][index] is None:
                                   #first_blank=j
                                   B.append(j)

                              if self.combined_data[j][index] is not None:
                                   f.append(j)
                                   last_full=f[-1]
                
                        break

                                          
        count= len(B)
        if count>0:
            n=0
            while(n <= count-1):
                k=n
                while( k<=count-1 and (B[k]+1) in B):
                    k=k+1

                                        
                if k <= count-1: 
                    next_index = B[k] + 1
                    prev_index = B[n] - 1
                    if next_index <= last_full and prev_index >= 0 :
                        delta=(self.combined_data[B[k]+1][index] - self.combined_data[B[n]-1][index])/ ((B[k]+1) - (B[n]-1))
                        narojelo=False
                    else:
                        narojelo=True
                        
                    if narojelo==False:
                        while n<=k:
                                self.combined_data[B[n]][index]= self.combined_data[B[n]-1][index]+delta
                                n=n+1
                    else:
                        break

     def FindBlankRangeversion2(self,index):
          pass


     def createSyncTimeFrame(self,IdealMinTime):
          CurrentTime= com.Common_Time.Now()
          NowSec=self.time_to_seconds(CurrentTime)
          len(self.combined_data)
          StartSecTime=NowSec-(IdealMinTime*60)
          syncdata=self.combined_data[StartSecTime:NowSec]
          #return syncdata

     def covariance(self, syncdata):
          data1=[]
          data2=[]
          sum1=0
          sum2=0
          dev1=[]
          dev2=[]
          totalSum=0
          for i in range(len(syncdata)):
               data1.append(syncdata[i][0])   
               data2.append(syncdata[i][1])
               count1=len(data1)
               count2=len(data2)
               #len(data1)==len(data2)?==len(syncdata)?
          for j in range(len(data1)):
               sum1+=data1[j]
               sum2+=data2[j]
          
          avg1 =sum1/len(data1)
          avg2 =sum2/len(data2)

          for k in range(len(syncdata)):
               
               #d1=dev1.append(data1[k]-avg1)
               #d2=dev2.append(data2[k]-avg2)
               multiply= ((data1[k]-avg1) * (data2[k]-avg2) )
               #multiply=(dev1.append(syncdata[k][0]-avg1)) * (dev2.append(syncdata[k][1]-avg2))
               totalSum= multiply+totalSum

          cov= totalSum/(len(syncdata)-1)
          #print(len(syncdata))
          return cov


     def checkStatus(self,covariance):
          self.LastRelation=self.CurentRelation

          if covariance == 0:
               self.CurentRelation.direction=com.ProcesStatus.conver
          elif covariance < 0:
               self.CurentRelation.direction=com.ProcesStatus.disver
          else:
               self.CurentRelation.direction=com.ProcesStatus.inactive

          if self.CurentRelation.direction==self.LastRelation.direction:
               self.CurentRelation.EndTime=self.LastRelation.EndTime
          else:
               changeStatus(self,CurentRelation,self.LastRelation)


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
     SurceUID = "6PEW67J130A4J262J246R7K671UJ0FJ40"
     DesiUID = "011W72B147CW0KV08O55GA2MTX5X4HDK4"
     RelationStatus=V2RelationStatus(SurceUID, DesiUID)
     test=RelationStatus.StartProcess2()
     #print(test)
