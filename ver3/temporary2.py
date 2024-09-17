import json
import os
from datetime import datetime
import CommonFunction as com
import uuid
import statistics

class V2RelationStatus():

    uid_watt = "6PEW67J130A4J262J246R7K671UJ0FJ40"
    uid_ampere = "011W72B147CW0KV08O55GA2MTX5X4HDK4"
    timestamp = "2024-07-27 11:58:23"
    base_url = "http://www.asset23d.ir/api/OBJVALUE"

    def __init__(self):
        self.candidate_data=[[1, 300],[2, 600],[3, 900]]
        self.StartProcess()

    def StartProcess(self):
         self.covariancever1()

  
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

        # DataSum1=sum(DataProperty1)
        # DateSum2=sum(DataProperty2)
        avg1 =statistics.mean(DataProperty1)
        avg2 =statistics.mean(DataProperty2)

        for k in range(len(self.candidate_data)):              
            multiply= ((DataProperty1[k]-avg1) * (DataProperty2[k]-avg2) )
            totalSum+= multiply
        cov= totalSum/(len(self.candidate_data)-1)
        print(cov)
        return cov
if __name__=="__main__":
    RelationStatus=V2RelationStatus()
    #test=RelationStatus.StartProcess()