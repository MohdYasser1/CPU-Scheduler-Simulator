from .SchedulingStrategy import *
from ..process.Status import *
import time


# non preemptive priority
class NPP(SchedulingStrategy):
    def run(self, scheduler):
        processes = sorted(scheduler.get_processes(), key=lambda x: x.priority)

        
        for process in processes:
            if process.getStatus() == Status.NOT_ARRIVED and process.getArrivalTime() <= scheduler.get_elapsedTime():
                process.setStatus(Status.READY)

        # check if no process is running
        if not any(process.getStatus() == Status.RUNNING for process in processes):
            # choose the process with the highest priority and set it to running

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
        
        # if processes do not arrive yet, increment the elapsed time by the quantum time
        scheduler.set_elapsedTime(
        scheduler.get_elapsedTime() + scheduler.get_quantumTime()
        )
        if scheduler.isLive():
            time.sleep(scheduler.get_quantumTime())

        return None

