import json
import os
import uuid
from datetime import datetime

class ProcesStatus():
    Null = 'Null'
    Default = 'Default'

class Common_UID():
    def new(UID):
         return str(uuid.uuid5(uuid.NAMESPACE_DNS, UID))
             

class Common_Time():
    def Now():
        itime = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        return itime