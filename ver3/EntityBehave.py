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
     def __init__(self, Surce, Desi) -> None:

          self.Surce=SurceUID
          self.Desi=Desi

          self.uid = com.Common_UID.new(Surce+Desi)
          self.ibehave = V2RelationBehave()
          self.CurentRelation = self.ibehave.Get(self.uid)

          if self.CurentRelation == com.ProcesStatus.Null:
               self.CurentRelation = self.ibehave.New(Surce,Desi)
               self.CurentRelation = self.ibehave.Save(self.CurentRelation)
          
          self.DataProperty1=com.ProcesStatus.Null
          self.DataProperty2=com.ProcesStatus.Null
          self.combined_data = [[None, None] for _ in range(86400)]
          self.candidate_data=[]
          self.syncdata=[]
          
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
          #print(self.candidate_data)
          cov=self.covariance()
          self.checkStatus(cov)
          self.direction_range(cov)
          self.current_relation(self.Surce,self.Desi)

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

     def FindBlankRange(self,index):
        CheckTrigger = False
        stop=False
        last_full=None
        first_full = None
        first_blank = None
        last_blank = None
        finalDataBlock=86400
        data_length = len(self.combined_data)
        Blanks=[]
        full=[]
        Count_blanks=[]
        count=0
        for i in range(0,data_length):
            if self.combined_data[i][index] is not None:
                    if CheckTrigger==False:
                        first_full=i
                        CheckTrigger=True
                        
                        break
                        
        for j in range(first_full, data_length):
            if self.combined_data[j][index] is None:
                Blanks.append(j)
                count= len(Blanks)
        
        for z in range(first_full,data_length):
            if self.combined_data[z][index] is not None:
                full.append(z)
                last_full=full[-1]
                
        if count>0:
            n=0
            while(n <= count-1):
                k=n
                while( k<=count-1 and (Blanks[k]+1) in Blanks):
                    k=k+1



                if k <= count-1: 
               
                    next_index = Blanks[k] + 1
                    prev_index = Blanks[n] - 1
                    if next_index <= last_full and prev_index >= 0 :
                        delta=(self.combined_data[Blanks[k]+1][index] - self.combined_data[Blanks[n]-1][index])/ ((Blanks[k]+1) - (Blanks[n]-1))
                        stop=False
                    else:
                        stop=True
                        
                   
                    #if prev_index <= last_full-1 and prev_index >= 0 :
                    if stop==False:
                        while n<=k:
                                self.combined_data[Blanks[n]][index]= self.combined_data[Blanks[n]-1][index]+delta
                                n=n+1
                               
                    else:
                        break
                        


     def FindBlankRangeversion2(self,index):
        CheckTrigger = False
        first_blank = None
        last_blank = None
        finalDataBlock=86400

        data_length = len(self.combined_data)
        i=0
          
        
        while(i<data_length):
            if self.combined_data[i][index] is not None:
                    if CheckTrigger==False:
                        first_full=i
                        CheckTrigger=True

                     
            if CheckTrigger==True:
                if self.combined_data[i][index] is None:
                    first_blank=i
               
                    for j in range(first_blank,data_length ):
                        if self.combined_data[j][index] is None:
                            last_blank=j
                            IsNone=True
                            
                        else:
                            if IsNone==True:
                                self.GapFiller(first_blank ,last_blank ,index)
                                IsNone=False
                                i=j-1
                                break
                     
            i+=1
                                    
     
     def OptimizeBlankRange(self, index):
        CheckTrigger = False
        first_blank = None
        data_length = len(self.combined_data)
        i = 0


        while i < data_length:
            if self.combined_data[i][index] is not None:
                if not CheckTrigger:
                    CheckTrigger = True

            if CheckTrigger and self.combined_data[i][index] is None:
                first_blank = i
                
                while i < data_length and self.combined_data[i][index] is None:
                    i += 1
                
                self.GapFiller(first_blank, i - 1, index)
                    
                continue

            i += 1

     def GapFiller(self,start,end,index):
        delta=0
        if end + 1 < len(self.combined_data):
          BeforeBlank=self.combined_data[start-1][index]
          AfterBlank=self.combined_data[end+1][index]
          delta=(AfterBlank-BeforeBlank)/((end+1)-(start-1))
          for k in range (start,end+1):
               self.combined_data[k][index]=self.combined_data[k-1][index]+delta                      



     def createSyncTimeFrame(self):
          CurrentTime= com.Common_Time.Now()
          NowSec=self.time_to_seconds(CurrentTime)
          len(self.combined_data)
          StartSecTime=NowSec-(self.IdealMinTime*60)
          return StartSecTime,NowSec
          #self.syncdata=self.combined_data[StartSecTime:NowSec]
          #return syncdata

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
               multiply= ((DataProperty1[k]-avg1) * (DataProperty2[k]-avg2) )
               totalSum+= multiply
          return totalSum



     def current_relation(self,surce,desi, covariance):
          self.current_relation=Entity.CurentEntityRelation()
          self.current_relation.uid=surce+desi
          self.current_relation.source=surce
          self.current_relation.destination=desi         
          self.current_relation.direction=self.direction_range(covariance)
          self.current_relation.status=com.ProcesStatus.Null
          self.current_relation.config=com.ProcesStatus.Null
          self.current_relation.start_time=com.ProcesStatus.Null
          self.current_relation.end_time=com.ProcesStatus.Null
          self.current_relation.value=com.SubjectItem.jsonify_value(Entity.SubjectItem(name="Covariance", value=covariance, type="float"))
          self.current_relation.option=com.ProcesStatus.Null


     def direction_range(self,covariance):
          if covariance>0.5:
               direction=Entity.RelationDirection.Convergent
          if covariance<-0.5:
               direction=Entity.RelationDirection.Divergent
          else:
               direction=Entity.RelationDirection.InActive
          return direction


     def check_status(self.current_relation.status, self.current_relation.direction):
          pass 



     # def checkStatus(self,covariance):
     #      self.LastRelation=self.CurentRelation

     #      if covariance == 0:
     #           self.CurentRelation.direction=com.ProcesStatus.conver
     #      elif covariance < 0:
     #           self.CurentRelation.direction=com.ProcesStatus.disver
     #      else:
     #           self.CurentRelation.direction=com.ProcesStatus.inactive

     #      if self.CurentRelation.direction==self.LastRelation.direction:
     #           self.CurentRelation.EndTime=self.LastRelation.EndTime
     #      else:
     #           self.changeStatus(self,self.CurentRelation,self.LastRelation)

     def state1():
          pass
     def state2():
          pass
     def state3():
          pass
     def state4():
          pass


     
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
     RelationStatus=V2RelationStatus(SurceUID, DesiUID)
     #test=RelationStatus.StartProcess()
     #print(test)
