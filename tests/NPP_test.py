
from app.controller.Scheduler import *
from app.model.process.Process import *
from app.model.schedulingAlgorithms.NPP import *

#NPP with 5 Processes
print("///// Test(1) /////")

p1 = Process(1, 5, 1, 0)
p2 = Process(2, 8, 3, 0)
p3 = Process(3, 7, 4, 0)
p4 = Process(4, 3, 2, 0)
p5 = Process(5, 4, 5, 0)

processes = [p1, p2, p3, p4, p5]
SchedulingStrategy = NPP()
scheduler = Scheduler(SchedulingStrategy, processes)

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



# # NPSJF with 3 Processes and the first Process is the largest one
# print("///// Test(2) /////")

# p1 = Process(1, 1, 2, 0)
# p2 = Process(2, 7, 1, 2)
# p3 = Process(3, 7, 3, 1)

# processes = [p1, p2, p3]
# SchedulingStrategy = NPP()
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
