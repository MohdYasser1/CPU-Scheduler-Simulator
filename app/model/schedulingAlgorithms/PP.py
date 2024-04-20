# from .SchedulingStrategy import *
# from ..process.Status import *
# import time

# # preemptive priority
# class PP(SchedulingStrategy):
#     def run(self, scheduler):
            # for process in processes:
            #             if process.getBurstTime() != 0 and process.getArrivalTime() <= scheduler.get_elapsedTime():
            #                 process.setStatus(Status.READY)

#         # Check if there are any running processes from the previous iteration.
#         # If there are, pause them and set their status to READY.
#         for process in scheduler.get_processes():
#             if process.getStatus() == Status.RUNNING:
#                 process.setStatus(Status.READY)

#         # Sort processes based on priority.
#         processes = sorted(scheduler.get_processes(), key=lambda x: x.priority)

#         # Check if no process is currently running.
#         if not any(process.getStatus() == Status.RUNNING for process in processes):
#             # Choose the process with the highest priority and set it to RUNNING.
#             for process in processes:
#                 if (
#                     process.getStatus() == Status.READY
#                     and process.getArrivalTime() <= scheduler.get_elapsedTime()
#                 ):
#                     process.setStatus(Status.RUNNING)
#                     break

#         # Execute the running process.
#         for process in processes:
#             if (
#                 process.getStatus() == Status.RUNNING
#                 and process.getArrivalTime() <= scheduler.get_elapsedTime()
#             ):
#                 # Check for equal-priority processes.
#                 equal_priority_processes = [
#                     p
#                     for p in processes
#                     if p.getStatus() == Status.READY
#                     and p.getArrivalTime() <= scheduler.get_elapsedTime()
#                     and p.priority == process.priority
#                 ]
#                 if equal_priority_processes:
#                     # Choose the process that arrived first.
#                     equal_priority_processes.append(process)
#                     next_process = min(
#                         equal_priority_processes, key=lambda x: x.getArrivalTime()
#                     )
#                     next_process.setStatus(Status.RUNNING)
#                     if(next_process != process):
#                          process.setStatus(Status.READY)

#                     next_process.execute(scheduler)
#                     return next_process
#                 else:
#                     process.execute(scheduler)
#                     return process
                
#         # if processes do not arrive yet, increment the elapsed time by the quantum time
#         scheduler.set_elapsedTime(
#             scheduler.get_elapsedTime() + scheduler.get_quantumTime()
#         )
#         if scheduler.isLive():
#             time.sleep(scheduler.get_quantumTime())

#         return None


#===============================================================================================================
#another IMP
#===============================================================================================================
from .SchedulingStrategy import *
from ..process.Status import *
import time



class PP(SchedulingStrategy):
    def run(self, scheduler):

        for process in processes:
            if process.getStatus() == Status.NOT_ARRIVED and process.getArrivalTime() <= scheduler.get_elapsedTprocess.getArrivalTime():
                process.setStatus(Status.READY)

       
        for process in scheduler.get_processes():
            if process.getStatus() == Status.RUNNING:
                process.setStatus(Status.READY)

        processes = sorted(scheduler.get_processes(), key=lambda x: x.priority)


      # check if no process is running
        if not any(process.getStatus() == Status.RUNNING for process in processes):
            for process in processes:
                if (
                    process.getStatus() == Status.READY
                    and process.getArrivalTime() <= scheduler.get_elapsedTime()
                ):
                    process.setStatus(Status.RUNNING)
                    processr=process
                    break

        #check if process have the same priority with other and take which come first
        for next_process in scheduler.get_processes()[1:]:
            if (
                next_process.getStatus() == Status.READY
                and next_process.arrivalTime <= scheduler.get_elapsedTime()
                and next_process.priority == processr.priority
                and next_process.arrivalTime < processr.arrivalTime
                
                ):
                processr.setStatus(Status.READY)
                next_process.setStatus(Status.RUNNING)
                processr=next_process
                





        # execute the running process
        for process in processes:
            if (
                process.getStatus() == Status.RUNNING
                and process.getArrivalTime() <= scheduler.get_elapsedTime()
            ):
                if process.getBurstTime() >= scheduler.get_quantumTime():
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

                return process










        

 
