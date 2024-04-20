# import sys
# import os
# # Add the parent directory to the Python path using forward slashes or raw string literal
# parent_dir = r'C:/Users/ahmed/OneDrive/Desktop/CSE 25/Senior 1/SPRING 2024/Operating Systems/project/CPU-Scheduler-Simulator/app'
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), parent_dir)))

from app.model.schedulingAlgorithms.SchedulingStrategy import *
from app.model.schedulingAlgorithms.FCFS import *
from app.model.process.Status import *


class Scheduler:

    def __init__(
        self,
        strategy: SchedulingStrategy = FCFS(),
        processes=list(),
        quantumTime=1,
        live=True,
    ):
        self.strategy = strategy
        self.processes = processes
        self.quantumTime = quantumTime
        self.elapsedTime = 0
        self.live = live

    def set_strategy(self, strategy: SchedulingStrategy):
        self.strategy = strategy

    def get_strategy(self):
        return self.strategy

    def set_processes(self, processes):
        self.processes = processes

    def get_processes(self):
        return self.processes

    def set_quantumTime(self, quantumTime):
        self.quantumTime = quantumTime

    def get_quantumTime(self):
        return self.quantumTime

    def set_elapsedTime(self, elapsedTime):
        self.elapsedTime = elapsedTime

    def get_elapsedTime(self):
        return self.elapsedTime

    def set_live(self, live):
        self.live = live

    def isLive(self):
        return self.live

    def add_process(self, process):
        self.processes.append(process)

    def has_processes(self):
        if any(process.getStatus() != Status.COMPLETED for process in self.processes):
            return True
        return False

    def progress(self):
        return self.strategy.run(self)

    def getAverageTurnaroundTime(self):
        total = 0
        for process in self.processes:
            total += process.getTurnaroundTime()
        return total / len(self.processes)

    def getAverageWaitingTime(self):
        total = 0
        for process in self.processes:
            total += process.getWaitingTime()
        return total / len(self.processes)

    # call after initialization and scheduler progress() directly
    def updateProcessStatus(self):
        for process in self.processes:
            if (
                process.getArrivalTime() <= self.elapsedTime
                and process.getStatus() == Status.NOT_ARRIVED
            ):
                process.setStatus(Status.READY)


print("Scheduler.py has been loaded")
