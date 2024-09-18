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
    none='None'

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
    base_url="http://www.asset23d.ir/api/"
    cmd_url = "http://www.asset23d.ir/api/CMD"
    headers = {
    "Content-Type": "application/json"
}
    getPropertyListCmd={"cmd": "get_all_property_list"}
    PropObj="finalObj"
    TypePropObj=list
    


class Common_UID():
    def new(UID):
         return str(uuid.uuid5(uuid.NAMESPACE_DNS, UID))
             

class Common_Time():
    def Now():
        itime = datetime.now().replace(microsecond=0)
        return itime
    
    def ParseStringToDateTime(date_time_str):
        try:
            if not isinstance(date_time_str, str):
                date_time_str = str(date_time_str)
            dt = parser.parse(date_time_str)
            return dt

        except (ValueError, parser.ParserError) as e:
               print(f"Error parsing time string '{date_time_str}': {e}")
               return None

        
class RequestHandler():
    
    def getRequest(url, params=None, type:str = 'Json', **kwargs ):
        if type == 'Json':
            try:
                response = requests.get(url, params=params,**kwargs)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                return e
            
    def postRequest(url, headers=None, data=None,type:str = 'Json', **kwargs):
        if type=='Json':
            try:
                response=requests.post(url,headers=headers, data=data)
                response.raise_for_status()
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        return response_data
                    # final_obj = response_data.get('finalObj', None)
                    # if final_obj is not None:
                    except json.JSONDecodeError:
                        return("Error: JSON response could not be decoded")
                        #return None
                else:
                    return(f"Error: Unable to fetch property list, Status Code: {response.status_code}")
                    #return None
            except requests.exceptions.RequestException as e:
                return(f"Error: {e}")
                #return None
    def CheckCmdResponseIsExist(response, uniqueOBJ,type ):
        final_obj = response.get(uniqueOBJ, None)
        if final_obj is not None:

            #if type==list:
            if isinstance(final_obj, type):
                #if final_obj==type:
                    return True,final_obj
            else:
                print(f"Error: Expected a {type} in the {uniqueOBJ} data")
                return False

class timeFrame():
    combined_data=[[None, None] for _ in range(86400)]

    def checkDataIsList(self,data, list):
        if not isinstance(data, list):
            return ProcesStatus.not_accepted_format
        else:
            return True

    def isNull(values1,values2):
        if not values1 or not values2:
            return False


class calculation():

    def calculate_average(sum=None, length= None,values1=None):
        average = None
        if sum==None and length==None and values1!=None:
            if len(values1)!=0:
                average = sum(values1) / len(values1)
        elif sum!=None and length!=None and values1==None:
            if length!=0:
                average= sum/length

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

        
class SubjectItem():
    def jsonify_value(self, subject_item):
        return json.dumps(subject_item.__dict__)






