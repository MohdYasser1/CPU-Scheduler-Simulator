from .SchedulingStrategy import *
from ..process.Status import *
import time


# non-preemptive shortest job first
class NPSJF(SchedulingStrategy):
    def run(self, scheduler):
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
