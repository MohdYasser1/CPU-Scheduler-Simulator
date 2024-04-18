from model.schedulingAlgorithms.SchedulingStrategy import *
from model.schedulingAlgorithms.FCFS import *
from model.process.Status import *


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


print("Scheduler.py has been loaded")
