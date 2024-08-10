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

    def Update(self,CurentRelation,lastRelation):
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
     def __init__(self,Surce,Desi) -> None:
          self.uid = com.Common_UID.new(Surce+Desi)
          self.ibehave = V2RelationBehave()
          self.CurentRelation = self.ibehave.Get(self.uid)

          if self.CurentRelation == com.ProcesStatus.Null:
               self.CurentRelation = self.ibehave.New(Surce,Desi)
               self.CurentRelation = self.ibehave.Save(self.CurentRelation)

     def checkRelation():
          combined_data= [[None,None] for _ in range (86400)]
          def evalData(self, curentRelation):
               if curentRelation.EndTime.day==com.Common_Time.Now.day:
                    return True
               else:
                    return com.ProcesStatus.eval_false_data
          #if evalData==True:
          # def create_compare_list(list1 ,list2):  
          #      combined_data= [[None,None] for _ in range (86400)]

          def process_data(data,combined_list, index):
               if not isinstance(data, list):
                    return(com.ProcesStatus.not_accepted_format)
               sum_count = [[0, 0] for _ in range(86400)]

               for entry in data:
                    et_seconds = com.Common_Time.time_to_seconds(entry.get('et'))
                    ut_seconds = com.Common_Time.time_to_seconds(entry.get('ut'))
                    value = float(entry.get('va'))

                    update_sum_count(et_seconds, ut_seconds, value, sum_count)

               total_sum, total_count = calculate_sum_count(sum_count)
               average = total_sum / total_count if total_count > 0 else 0

               update_combined_data(sum_count, combined_data, index, average)
               interpolate_missing_values(combined_data, index)

          def update_sum_count(et_seconds, ut_seconds, value, sum_count):
               for sec in range(et_seconds, ut_seconds + 1):
                    if sec < 86400:
                         sum_count[sec][0] += value
                         sum_count[sec][1] += 1

          def calculate_sum_count(sum_count):
               total_sum = 0
               total_count = 0
               for sec in range(86400):
                    total_sum += sum_count[sec][0]
                    total_count += sum_count[sec][1]
               return total_sum, total_count

          def update_combined_data(sum_count, combined_data, index, average):
               for sec in range(86400):
                    if sum_count[sec][1] > 0:
                         combined_data[sec][index] = (sum_count[sec][0] / sum_count[sec][1]) - average
                    else:
                         combined_data[sec][index] = None


          def interpolate_missing_values(combined_data, index):
               last_value = None
               last_value_index = None

               for i in range(86400):
                    if combined_data[i][index] is not None:
                         if last_value is not None:
                              step = (combined_data[i][index] - last_value) / (i - last_value_index)
                              for j in range(last_value_index + 1, i):
                                   combined_data[j][index] = round(last_value + step * (j - last_value_index), 4)
                         last_value = combined_data[i][index]
                         last_value_index = i

          def find_common_range(data1, data2):
               start1, end1 = find_range(data1)
               start2, end2 = find_range(data2)
               common_start = max(start1, start2)
               common_end = min(end1, end2)
               return common_start, common_end

          def find_range(data):
               start = next((i for i in range(len(data)) if data[i] is not None), None)
               end = next((i for i in range(len(data) - 1, -1, -1) if data[i] is not None), None)
               return start, end


          def calculate_covariance(combined_data, common_start, common_end):
   
               watt_values = [combined_data[i][0] for i in range(common_start, common_end + 1) if combined_data[i][0] is not None]
               ampere_values = [combined_data[i][1] for i in range(common_start, common_end + 1) if combined_data[i][1] is not None]

   
               if not watt_values or not ampere_values:
                    return 0  
   
               average_watt = sum(watt_values) / len(watt_values)
               average_ampere = sum(ampere_values) / len(ampere_values)

               covariance_sum = 0
               count = 0

               for i in range(common_start, common_end + 1):
                    if combined_data[i][0] is not None and combined_data[i][1] is not None:
                         watt_deviation = combined_data[i][0] - average_watt
                         ampere_deviation = combined_data[i][1] - average_ampere
                         covariance_sum += watt_deviation * ampere_deviation
                         count += 1
   
               if count != len(watt_values) or count != len(ampere_values):
                    raise ValueError("Mismatch between count and lengths of watt_values or ampere_values")

               return covariance_sum / (count - 1) if count > 1 else 0

               
          def getDataLog():
               pass
        
          def CreateTimeFrame():
               pass
        

iV2RelationStatus = V2RelationStatus('A','B')
MyTestRelarion = iV2RelationStatus.CurentRelation

# print('Step 1:',curenttestUID)
# print('Step 2:',GetTestRelation)
print('Step StartTime:',MyTestRelarion['StartTime'])

