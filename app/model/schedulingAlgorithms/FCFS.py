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
                if (
                    process.getStatus() == Status.READY
                    and process.getArrivalTime() <= scheduler.get_elapsedTime()
                ):
                    process.setStatus(Status.RUNNING)
                    return process

        # execute the running process
        for process in processes:
            if process.getStatus() == Status.RUNNING:
                process.execute(scheduler)
                return process

        # if processes do not arrive yet, increment the elapsed time by the quantum time
        scheduler.set_elapsedTime(
            scheduler.get_elapsedTime() + scheduler.get_quantumTime()
        )
        if scheduler.isLive():
            time.sleep(scheduler.get_quantumTime())

        return None
