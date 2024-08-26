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
                            [None, None],[0, None],[None, None],[15, None],[17, None],[None, None],[None, None],[None, None],[None, None],[20, None],[None, None]]
          
          
        self.StartProcess()

    def StartProcess(self):

          #combined_data = [[None, None] for _ in range(86400)]
        self.OptimizeBlankRange(0)
        print(self.combined_data)
        #self.FindBlankRange(1)
        #print(datetime.now())

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
        if end + 1 < len(self.combined_data):
            AfterBlank = self.combined_data[end + 1][index]
            BeforeBlank=self.combined_data[start-1][index]
            delta=(AfterBlank-BeforeBlank)/((end+1)-(start-1))
            for k in range (start,end+1):
                self.combined_data[k][index]=self.combined_data[k-1][index]+delta
        
      
    def backupfindblankrange(self,index):
        CheckTrigger = False
        first_blank = None
        last_blank = None
        finalDataBlock=86400

        data_length = len(self.combined_data)
        i=0
          
        
        while(i<data_length):
            if self.combined_data[i][index] is not None:
                    if CheckTrigger==False:
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
                
                # Find the end of the None sequence in a single loop
                while i < data_length and self.combined_data[i][index] is None:
                    i += 1
                
                # Fill the gap if a sequence of None values was found
                self.GapFiller(first_blank, i - 1, index)
                    
                continue  # Skip the normal increment of i since we already incremented inside the loop

            i += 1
                                
if __name__=="__main__":
    RelationStatus=V2RelationStatus()
    #test=RelationStatus.StartProcess()