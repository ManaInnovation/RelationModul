import json
import os
from datetime import datetime
import statistics
import schedule
import time

class V2RelationStatus():
    uid_watt = "6PEW67J130A4J262J246R7K671UJ0FJ40"
    uid_ampere = "011W72B147CW0KV08O55GA2MTX5X4HDK4"
    timestamp = "2024-07-27 11:58:23"
    base_url = "http://www.asset23d.ir/api/OBJVALUE"

    def __init__(self):
        self.candidate_data = [[1, 300], [2, 600], [3, 900]]
        #self.startprocess()

    
    def startprocess(self):
        self.covariancever1()

    def covariancever1(self):
        DataProperty1 = []
        DataProperty2 = []
        totalSum = 0

        # Extracting the first and second elements from candidate_data into separate lists
        for i in range(len(self.candidate_data)):
            DataProperty1.append(self.candidate_data[i][0])
            DataProperty2.append(self.candidate_data[i][1])

        # Calculate the means of both datasets
        avg1 = statistics.mean(DataProperty1)
        avg2 = statistics.mean(DataProperty2)

        # Calculate covariance
        for k in range(len(self.candidate_data)):
            multiply = (DataProperty1[k] - avg1) * (DataProperty2[k] - avg2)
            totalSum += multiply
        cov = totalSum / (len(self.candidate_data) - 1)
        print(f"Covariance: {cov}")
        return cov

    def run(self):
        """Run the main process for this class, which is covariance calculation."""
        print("Starting covariance calculation process...")
        self.covariancever1()

def run_tasks():
    current_time = datetime.now()
    start_time = datetime.now().replace(hour=11, minute=33, second=0, microsecond=0)  # Start time
    end_time = datetime.now().replace(hour=11, minute=35, second=0, microsecond=0)    # End time

    # Check if current time is within the allowed range
    if start_time <= current_time <= end_time:
        print(f"Running tasks at {current_time}")
        relation_status = V2RelationStatus()  # Create instance
        relation_status.startprocess()                 # Trigger the run method
    else:
        print(f"Out of time range at {current_time}. Stopping the scheduler.")
        return schedule.CancelJob  # This will stop the scheduling loop

# Schedule the task to run every 1 minute
job = schedule.every(1).minutes.do(run_tasks)

if __name__ == "__main__":
    print("Scheduler started...")

    while True:
        schedule.run_pending()  # Check for any scheduled tasks
        
        # Check if the job has been canceled
        if job in schedule.jobs:
            time.sleep(1)  # Keep checking for pending jobs every second
        else:
            print("Job cancelled. Exiting program.")
            break  # Exit the loop and stop the program
