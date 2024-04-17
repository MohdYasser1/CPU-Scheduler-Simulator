from app.controller.Scheduler import *
from app.model.process.Process import *
from app.model.schedulingAlgorithms.PSJF import *

# PSJF with 5 Processes
print("///// Test(1) /////")

p1 = Process(1, 5, 1, 0)
p2 = Process(2, 8, 1, 1)
p3 = Process(3, 2, 1, 2)
p4 = Process(4, 3, 1, 3)
p5 = Process(5, 4, 1, 4)

processes = [p1, p2, p3, p4, p5]
SchedulingStrategy = PSJF()
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

# PSJF with 3 Processes and the first Process is the largest one
print("///// Test(2) /////")

p1 = Process(1, 8, 1, 0)
p2 = Process(2, 5, 1, 1)
p3 = Process(3, 7, 1, 2)

processes = [p1, p2, p3]
SchedulingStrategy = PSJF()
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

# PSJF with 4 Processes
print("///// Test(3) /////")

p1 = Process(1, 7, 1, 0)
p2 = Process(2, 4, 1, 2)
p3 = Process(3, 1, 1, 4)
p4 = Process(4, 4, 1, 5)


processes = [p1, p2, p3, p4]
SchedulingStrategy = PSJF()
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
