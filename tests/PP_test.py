import sys
import os
# Add the parent directory to the Python path using forward slashes or raw string literal
parent_dir = r'C:/Users/ahmed/OneDrive/Desktop/CSE 25/Senior 1/SPRING 2024/Operating Systems/project/CPU-Scheduler-Simulator'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), parent_dir)))

from app.controller.Scheduler import *
from app.model.process.Process import *
from app.model.schedulingAlgorithms.PP import *

#NPP with 5 Processes
print("///// Test(1) /////")

p1 = Process(1, 5, 1, 0)
p2 = Process(2, 8, 1, 1)
p3 = Process(3, 7, 4, 0)
p4 = Process(4, 3, 2, 0)
p5 = Process(5, 4, 2, 1)
p6 = Process(6, 4, 0, 7)

processes = [p1, p2, p3, p4, p5]
SchedulingStrategy = PP()
scheduler = Scheduler(SchedulingStrategy, processes)

while True:
    print("=====================================")
    print(f"Elapsed Time: {scheduler.get_elapsedTime()}")
    currentProcesses = scheduler.get_processes()

    if scheduler.get_elapsedTime() == 7:
            scheduler.add_process(p6)

    for process in currentProcesses:
        print(process)

    if not scheduler.has_processes():
        break

    scheduler.progress()

print("=====================================")
print(f"Average turnaround time: {scheduler.getAverageTurnaroundTime()}")
print(f"Average waiting time: {scheduler.getAverageWaitingTime()}")


