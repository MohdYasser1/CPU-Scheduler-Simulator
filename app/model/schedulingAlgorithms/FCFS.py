from .SchedulingStrategy import *
from ..process.Status import *
import time


class FCFS(SchedulingStrategy):
    def run(self, scheduler):
        processes = sorted(scheduler.get_processes(), key=lambda x: x.arrivalTime)

        # check if no process is running
        if not any(process.getStatus() == Status.RUNNING for process in processes):
            # choose the process that arrived first and set it to running
            for process in processes:
                if process.getStatus() == Status.READY:
                    process.setStatus(Status.RUNNING)
                    break

        # execute the running process
        for process in processes:
            if process.getStatus() == Status.RUNNING:
                process.execute(scheduler)
                return process
