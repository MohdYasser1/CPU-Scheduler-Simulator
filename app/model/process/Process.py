class Process:
    def __init__(
        self, processId, burstTime, priority=1, arrivalTime=0, completionTime=0
    ):
        self.processId = processId
        self.burstTime = burstTime
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.completionTime = completionTime

    def __str__(self):
        return f"Process ID: {self.processId}, Burst Time: {self.burstTime}, Priority: {self.priority}, Arrival Time: {self.arrivalTime}, Completion Time: {self.completionTime}"

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

    def getWaitingTime(self):
        return self.completionTime - self.burstTime
