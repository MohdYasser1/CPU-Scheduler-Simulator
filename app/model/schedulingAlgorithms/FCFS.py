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
                if process.getBurstTime() >= scheduler.get_quantumTime():
                    if scheduler.isLive:
                        time.sleep(scheduler.get_quantumTime())

                    scheduler.set_elapsedTime(
                        scheduler.get_elapsedTime() + scheduler.get_quantumTime()
                    )
                    process.setBurstTime(
                        process.getBurstTime() - scheduler.get_quantumTime()
                    )

                else:
                    time.sleep(process.getBurstTime())
                    scheduler.set_elapsedTime(
                        scheduler.get_elapsedTime() + process.getBurstTime()
                    )
                    process.setBurstTime(0)

                if process.getBurstTime() == 0:
                    process.setStatus(Status.COMPLETED)
                    process.setCompletionTime(scheduler.get_elapsedTime())

                break
