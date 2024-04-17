from .SchedulingStrategy import *
from ..process.Status import *
import time


# preemptive shortest job first
class PSJF(SchedulingStrategy):
    def run(self, scheduler):

        # check if there are any running processes from the previous iteration
        # if there are, pause them and set to ready
        for process in scheduler.get_processes():
            if process.getStatus() == Status.RUNNING:
                process.setStatus(Status.READY)

        processes = sorted(scheduler.get_processes(), key=lambda x: x.burstTime)

        # check if no process is running
        if not any(process.getStatus() == Status.RUNNING for process in processes):
            # choose the process with the shortest burst time and set it to running
            for process in processes:
                if (
                    process.getStatus() == Status.READY
                    and process.getArrivalTime() <= scheduler.get_elapsedTime()
                ):
                    process.setStatus(Status.RUNNING)
                    break

        # execute the running process
        for process in processes:
            if (
                process.getStatus() == Status.RUNNING
                and process.getArrivalTime() <= scheduler.get_elapsedTime()
            ):
                process.execute(scheduler)
                return process
