from .SchedulingStrategy import *
from ..process.Status import *
import time

# round robin
class RR(SchedulingStrategy):
    def run(self, scheduler):
        processes = scheduler.get_processes()
        quantum_time = scheduler.get_quantumTime()

        for process in processes:
            if process.getBurstTime() != 0 and process.getArrivalTime() <= scheduler.get_elapsedTime():
                process.setStatus(Status.READY)

        # check if no process is running
        if not any(process.getStatus() == Status.RUNNING for process in processes):
            # choose the process that arrived first and set it to running
            for process in processes:
                if (
                    process.getStatus() == Status.READY
                    and process.getArrivalTime() <= scheduler.get_elapsedTime()
                ):
                    process.setStatus(Status.RUNNING)
                    break

        for process in processes:

            if (
                process.getStatus() == Status.RUNNING
                and process.getArrivalTime() <= scheduler.get_elapsedTime()
            ):
                process.execute(scheduler)
                process.setcompleted_quantum(process.getcompleted_quantum()+ 1)

                # Move the process to the end of the queue
                if(process.getcompleted_quantum() == quantum_time):
                    process.setcompleted_quantum(0)
                    processes.remove(process)
                    processes.append(process)
                return process

        # if processes do not arrive yet, increment the elapsed time by the quantum time
        scheduler.set_elapsedTime(
            scheduler.get_elapsedTime() + scheduler.get_quantumTime()
        )
        if scheduler.isLive():
            time.sleep(scheduler.get_quantumTime())

        return None

