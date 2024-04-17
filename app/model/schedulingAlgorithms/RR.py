
from .SchedulingStrategy import *
from ..process.Status import *
import time


# round robin
class RR(SchedulingStrategy):
    def run(self, scheduler):
        #processes = sorted(scheduler.get_processes(), key=lambda x: x.arrivalTime)
        processes = scheduler.get_processes()
        quantum_time = scheduler.get_quantumTime()


        for process in processes:
            if process.getBurstTime() != 0:
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
                    if process.getBurstTime() >= quantum_time:
                        if scheduler.isLive:
                            time.sleep(quantum_time)

                        scheduler.set_elapsedTime(scheduler.get_elapsedTime() + quantum_time)
                        process.setBurstTime(process.getBurstTime() - quantum_time)

                    else:
                        time.sleep(process.getBurstTime())
                        scheduler.set_elapsedTime(scheduler.get_elapsedTime() + process.getBurstTime())
                        process.setBurstTime(0)

                    if process.getBurstTime() == 0:
                        process.setStatus(Status.COMPLETED)
                        process.setCompletionTime(scheduler.get_elapsedTime())
                     

                    # Move the process to the end of the queue
                   
                    processes.remove(process)
                    processes.append(process)
                    break

       
