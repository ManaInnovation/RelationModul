import json
import os
from datetime import datetime

class V2RelationStatus():

    uid_watt = "6PEW67J130A4J262J246R7K671UJ0FJ40"
    uid_ampere = "011W72B147CW0KV08O55GA2MTX5X4HDK4"
    timestamp = "2024-07-27 11:58:23"
    base_url = "http://www.asset23d.ir/api/OBJVALUE"

    def __init__(self):
        self.combined_data=[[None, None],[None, None],[7, None],[None, None],[5, None],[None, None],[None, None],
                            [None, None],[0, None],[None, None],[15, None],[17, None],[None, None]]
          
          
        self.StartProcess()

    def StartProcess(self):

          #combined_data = [[None, None] for _ in range(86400)]
        self.FindBlankRange(0)
        print(self.combined_data)
        #self.FindBlankRange(1)
        print(datetime.now())

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
                            khali_hast=True
                            
                            
                            
                        else:
                            if khali_hast==True:
                                self.GapFiller(first_blank ,last_blank ,index)
                                khali_hast=False
                                i=j-1
                                break
                        
                            
            i+=1
                                    
                            
    def GapFiller(self,start,end,index):
        delta=0
        BeforeBlank=self.combined_data[start-1][index]
        AfterBlank=self.combined_data[end+1][index]
        delta=(AfterBlank-BeforeBlank)/((end+1)-(start-1))
        for k in range (start,end+1):
            self.combined_data[k][index]=self.combined_data[k-1][index]+delta
        
      
      
  
if __name__=="__main__":
    RelationStatus=V2RelationStatus()
    test=RelationStatus.StartProcess()