import json
import os
import uuid
import requests
from datetime import datetime
from dateutil import parser

class ProcesStatus():
    Null = 'Null'
    Default = 'Default'
    eval_false_data="The date of data is past"
    not_accepted_format="Unexpected data format"
    data_is_Null="data is null"
    passive='passive'
    active='active'
    none='none'

    conver='convergent'
    disver='disvergent'
    inactive='inactive'

class ControlReturn():

    def __init__(self, GivenObject, message:str = 'Null', control:bool = False):
        self.GivenObject= GivenObject
        self. message= message
        self. control = control


class CommonConfig():
    objvalue_url="http://www.asset23d.ir/api/OBJVALUE"
    


class Common_UID():
    def new(UID):
         return str(uuid.uuid5(uuid.NAMESPACE_DNS, UID))
             

class Common_Time():
    def Now():
        itime = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        return itime
    
    # def time_to_seconds(time_str):
    #     try:
    #         dt = parser.parse(time_str)
    #         return dt.hour * 3600 + dt.minute * 60 + dt.second
    #     except (ValueError, parser.ParserError) as e:
    #         print(f"Error parsing time string '{time_str}': {e}")
    #         return None
    
class RequestHandler():
    
    def getRequest(url, params=None, type:str = 'Json', **kwargs ):
        if type == 'Json':
            try:
                response = requests.get(url, params=params,**kwargs)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                return e
            
    def postRequest(url, data=None, json=None, **kwargs):
        pass


class timeFrame():
    combined_data=[[None, None] for _ in range(86400)]

    def checkDataIsList(self,data, list):
        if not isinstance(data, list):
            return ProcesStatus.not_accepted_format
        else:
            return True

   
    

    def find_range(self,data):
        start = next((i for i in range(len(self.data)) if data[i] is not None), None)
        end = next((i for i in range(len(self.data) - 1, -1, -1) if data[i] is not None), None)
        return start, end


    def find_common_range(self,data1, data2):
        start1, end1 = find_range(self,data1)
        start2, end2 = find_range(self,data2)
        common_start = max(start1, start2)
        common_end = min(end1, end2)
        return common_start, common_end
    

    def isNull(values1,values2):
        if not values1 or not values2:
            return False


class calculation():

    def calculate_average(values1):
        average = sum(values1) / len(values1)
        return average
    
    
class FileControl():
    def SaveJson(path,filename,data):
        formatted_data = {str(i): value for i, value in enumerate(data)}
        file_path = f"{path}/{filename}.json"
        with open(file_path, 'w') as json_file:
            json.dump(formatted_data, json_file,indent=4)

        
    #     data = {
    #     "id": frame.id,
    #     "hashcode": frame.hashcode,
    #     "start": frame.start.strftime("%m/%d/%Y %I:%M:%S %p"),
    #     "end": frame.end.strftime("%m/%d/%Y %I:%M:%S %p"),
    #     "Duration": str(frame.duration),
    #     "Type": frame.type,
    #     "SubjectList": [{"name": subj.name, "value": subj.value} for subj in frame.subject_list]
    # }
    # with open(filename, 'w') as f:
    #     json.dump(frame_data, f, indent=4)

    def Savetext(path,file):
        pass

    def OpenJson(path,file):
        pass

    def Opentext(path,file):
        pass

        

    








