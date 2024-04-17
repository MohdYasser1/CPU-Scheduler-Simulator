'''
import sys
import os
# Add the parent directory to the Python path using forward slashes or raw string literal
parent_dir = r'C:/Users/ahmed/OneDrive/Desktop/CSE 25/Senior 1/SPRING 2024/Operating Systems/project/CPU-Scheduler-Simulator'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), parent_dir)))

'''
from app.controller.Scheduler import *
from app.model.process.Process import *
from app.model.schedulingAlgorithms.RR import *

p1 = Process(1, 5, 1, 0)
p2 = Process(2, 8, 1, 1)
p3 = Process(3, 7, 1, 2)
p4 = Process(4, 3, 1, 3)
p5 = Process(5, 6, 1, 4)
p6 = Process(6, 4, 1, 6)

processes = [p1, p2, p3, p4, p6]

SchedulingStrategy = RR()
scheduler = Scheduler(SchedulingStrategy, processes,2)

while True:
    print("=====================================")
    print(f"Elapsed Time: {scheduler.get_elapsedTime()}")

    if scheduler.get_elapsedTime() == 8:
        scheduler.add_process(p5)
      
    currentProcesses = scheduler.get_processes()
    for process in currentProcesses:
        print(process)

    if not scheduler.has_processes():
        break

    scheduler.progress()

print("=====================================")
print(f"Average turnaround time: {scheduler.getAverageTurnaroundTime()}")
print(f"Average waiting time: {scheduler.getAverageWaitingTime()}")
