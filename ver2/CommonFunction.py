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
    passive='passive'
    active='active'
    none='none'
    conver='convergent'
    disver='disvergent'
    inactive='inactive'
class Common_UID():
    def new(UID):
         return str(uuid.uuid5(uuid.NAMESPACE_DNS, UID))
             

class Common_Time():
    def Now():
        itime = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        return itime
    def time_to_seconds(time_str):
        try:
            dt = parser.parse(time_str)
            return dt.hour * 3600 + dt.minute * 60 + dt.second
        except (ValueError, parser.ParserError) as e:
            print(f"Error parsing time string '{time_str}': {e}")
            return None
    
class requests():
    def fetch_data(base_url, uid, timestamp):
        params = {
            "UID": uid,
            "date": timestamp
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for UID {uid} at {timestamp}: {e}")
            return None
