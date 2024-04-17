import time
from .Status import *


class Process:
    def __init__(
        self, processId, burstTime, priority=1, arrivalTime=0, completionTime=0
    ):
        self.processId = processId
        self.burstTime = burstTime
        self.workingTime = burstTime
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.completionTime = completionTime
        self.status = Status.READY

    def __str__(self):
        return f"Process ID: {self.processId}, Burst Time: {self.burstTime}, Priority: {self.priority}, Arrival Time: {self.arrivalTime}, Completion Time: {self.completionTime}, Status: {self.status}"

    def setProcessId(self, processId):
        self.processId = processId

    def getProcessId(self):
        return self.processId

    def setBurstTime(self, burstTime):
        self.burstTime = burstTime

    def getBurstTime(self):
        return self.burstTime

    def setPriority(self, priority):
        self.priority = priority

    def getPriority(self):
        return self.priority

    def setArrivalTime(self, arrivalTime):
        self.arrivalTime = arrivalTime

    def getArrivalTime(self):
        return self.arrivalTime

    def setCompletionTime(self, completionTime):
        self.completionTime = completionTime

    def getCompletionTime(self):
        return self.completionTime

    def getTurnaroundTime(self):
        return self.completionTime - self.arrivalTime

    def getWaitingTime(self):
        return self.completionTime - self.arrivalTime - self.workingTime

    def execute(self, scheduler):
        if self.burstTime >= scheduler.get_quantumTime():
            if scheduler.isLive:
                time.sleep(scheduler.get_quantumTime())
            scheduler.set_elapsedTime(
                scheduler.get_elapsedTime() + scheduler.get_quantumTime()
            )
            self.burstTime -= scheduler.get_quantumTime()

        else:
            if scheduler.isLive():
                time.sleep(self.burstTime)
            scheduler.set_elapsedTime(scheduler.get_elapsedTime() + self.burstTime)
            self.burstTime = 0

        if self.burstTime == 0:
            self.status = Status.COMPLETED
            self.completionTime = scheduler.get_elapsedTime()

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status
