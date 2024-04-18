import sys
import os


import sys
import os
# Add the parent directory to the Python path using forward slashes or raw string literal
parent_dir = r'C:/Users/ahmed/OneDrive/Desktop/CSE 25/Senior 1/SPRING 2024/Operating Systems/project/CPU-Scheduler-Simulator'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), parent_dir)))



from app.controller.Scheduler import *
from app.model.process.Process import *
from app.model.schedulingAlgorithms.FCFS import *
import threading

# FCFS with 5 Processes
# print("///// Test(1) /////")

# p1 = Process(1, 5, 1, 0)
# p2 = Process(2, 8, 1, 1)
# p3 = Process(3, 7, 1, 2)
# p4 = Process(4, 3, 1, 3)
# p5 = Process(5, 4, 1, 4)

# processes = [p1, p2, p3, p4, p5]
# SchedulingStrategy = FCFS()
# scheduler = Scheduler(SchedulingStrategy, processes)

# while True:
#     print("=====================================")
#     print(f"Elapsed Time: {scheduler.get_elapsedTime()}")
#     currentProcesses = scheduler.get_processes()
#     for process in currentProcesses:
#         print(process)

#     if not scheduler.has_processes():
#         break

#     scheduler.progress()

# print("=====================================")
# print(f"Average turnaround time: {scheduler.getAverageTurnaroundTime()}")
# print(f"Average waiting time: {scheduler.getAverageWaitingTime()}")

# FCFS with 6 Processes and adding a Process in the middle of execution
# print("///// Test(2) /////")

# p1 = Process(1, 5, 1, 0)
# p2 = Process(2, 8, 1, 1)
# p3 = Process(3, 7, 1, 2)
# p4 = Process(4, 3, 1, 3)
# p5 = Process(5, 6, 1, 4)
# p6 = Process(6, 4, 1, 6)

# processes = [p1, p2, p3, p4, p6]

# SchedulingStrategy = FCFS()
# scheduler = Scheduler(SchedulingStrategy, processes)

# while True:
#     print("=====================================")
#     print(f"Elapsed Time: {scheduler.get_elapsedTime()}")

#     if scheduler.get_elapsedTime() == 7:
#         scheduler.add_process(p5)

#     currentProcesses = scheduler.get_processes()
#     for process in currentProcesses:
#         print(process)

#     if not scheduler.has_processes():
#         break

#     scheduler.progress()

# print("=====================================")
# print(f"Average turnaround time: {scheduler.getAverageTurnaroundTime()}")
# print(f"Average waiting time: {scheduler.getAverageWaitingTime()}")


#FCFS with 5 Processes and non live scheduler
print("///// Test(3) /////")

p1 = Process(1, 5, 1, 0)
p2 = Process(2, 8, 1, 1)
p3 = Process(3, 7, 1, 2)
p4 = Process(4, 3, 1, 3)
p5 = Process(5, 4, 1, 4)

processes = [p1, p2, p3, p4, p5]
SchedulingStrategy = FCFS()
scheduler = Scheduler(SchedulingStrategy, processes)
scheduler.set_live(False)

while True:
    if not scheduler.has_processes():
        break

    scheduler.progress()


print("=====================================")
print(f"Elapsed Time: {scheduler.get_elapsedTime()}")
currentProcesses = scheduler.get_processes()
for process in currentProcesses:
    print(process)

print("=====================================")
print(f"Average turnaround time: {scheduler.getAverageTurnaroundTime()}")
print(f"Average waiting time: {scheduler.getAverageWaitingTime()}")

# print("///// Test(3) /////")

# p1 = Process(1, 5, 1, 2)
# p2 = Process(2, 8, 1, 3)
# p3 = Process(3, 7, 1, 4)
# p4 = Process(4, 3, 1, 5)
# p5 = Process(5, 4, 1, 6)

# processes = [p1, p2, p3, p4, p5]
# SchedulingStrategy = FCFS()
# scheduler = Scheduler(SchedulingStrategy, processes)

# while True:
#     print("=====================================")
#     print(f"Elapsed Time: {scheduler.get_elapsedTime()}")
#     currentProcesses = scheduler.get_processes()
#     for process in currentProcesses:
#         print(process)

#     if not scheduler.has_processes():
#         break

#     scheduler.progress()

#     print("=====================================")
#     print(f"Average turnaround time: {scheduler.getAverageTurnaroundTime()}")
#     print(f"Average waiting time: {scheduler.getAverageWaitingTime()}")

'''
def run_scheduler(scheduler):
    while True:
        print("=====================================")
        print(f"Elapsed Time: {scheduler.get_elapsedTime()}")
        currentProcesses = scheduler.get_processes()
        for process in currentProcesses:
            print(process)

        if not scheduler.has_processes():
            break

        scheduler.progress()

    print("=====================================")
    print(f"Average turnaround time: {scheduler.getAverageTurnaroundTime()}")
    print(f"Average waiting time: {scheduler.getAverageWaitingTime()}")


# FCFS with 6 Processes while running the scheduler in the background using threads
print("///// Test(4) /////")

p1 = Process(1, 5, 1, 0)
p2 = Process(2, 8, 1, 1)
p3 = Process(3, 7, 1, 2)
p4 = Process(4, 3, 1, 3)
p5 = Process(5, 4, 1, 4)

processes = [p1, p2, p3, p4, p5]
SchedulingStrategy = FCFS()
scheduler = Scheduler(SchedulingStrategy, processes)

# Create and start the thread
thread = threading.Thread(target=run_scheduler, args=(scheduler,))
thread.start()

# Main thread continues here
print("Scheduler is running in the background...")
print("Main thread continues...")

# Wait for some time and add process to the scheduler while it is running
time.sleep(7)
scheduler.add_process(Process(6, 6, 1, 7))
'''