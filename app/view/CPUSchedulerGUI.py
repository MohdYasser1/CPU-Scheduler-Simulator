import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
import threading

from app.view.NotLiveGUI import NotLiveFrame
from app.view.LiveGUI import LiveFrame
from app.model.process.Process import Process
from app.model.schedulingAlgorithms import *
from app.model.schedulingAlgorithms.RR import RR
from app.model.schedulingAlgorithms.PSJF import PSJF
from app.model.schedulingAlgorithms.NPSJF import NPSJF
from app.model.schedulingAlgorithms.PP import PP
from app.model.schedulingAlgorithms.NPP import NPP
from app.controller.Scheduler import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("CPU Scheduler Simulator")
        self.mainFrame = MainFrame(self)
        self.mainFrame.pack(fill=ctk.BOTH, expand=True)
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def notLiveMode(self, scheduler):
        self.mainFrame.destroy()
        self.notLiveGUI = NotLiveFrame(self, scheduler)
        self.notLiveGUI.pack(fill=ctk.BOTH, expand=True)
    
    def liveMode(self, scheduler, schedulerType, noOfProcess):
        self.mainFrame.destroy()
        self.liveGUI = LiveFrame(self, scheduler, schedulerType, noOfProcess)
        self.liveGUI.pack(fill=ctk.BOTH, expand=True)
    

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure((0, 2), weight=1)

        self.schedulerType = None

        self.titleLabel = ctk.CTkLabel(
            self, text="CPU Scheduler", font=ctk.CTkFont(size=70, weight="bold")
        )
        self.titleLabel.grid(row=0, column=0, pady=50, columnspan=3)

        # Scheduler Selector
        self.schedulerSelectLayout = ctk.CTkLabel(
            self, text="Select Scheduler", font=ctk.CTkFont(size=25)
        )
        self.schedulerSelectLayout.grid(row=1, column=0, padx=75, sticky="w")
        schedules = [
            "FCFS",
            "SJF (Preemptive)",
            "SJF (Non-Preemptive)",
            "Priority (Preemptive)",
            "Priority (Non-Preemptive)",
            "Round Robin",
        ]
        self.dropdown = ctk.CTkOptionMenu(
            self, values=schedules, command=self.chooseScheduler
        )
        self.dropdown.set("Choose Scheduler")
        self.dropdown.grid(row=1, column=1, columnspan=2)

        # Ready Process Input
        self.noOfProcessLayout = ctk.CTkLabel(
            self,
            text="Number of Processes ready:",
            font=ctk.CTkFont(size=25),
            anchor="e",
        )
        self.noOfProcessLayout.grid(row=2, column=0, padx=75, pady=20, sticky="w")
        self.noOfProcessEntry = ctk.CTkEntry(
            self, placeholder_text="Enter no. of processes"
        )
        self.noOfProcessEntry.grid(row=2, column=1, columnspan=2)

        # Mode Selection
        self.modeLayout = ctk.CTkLabel(
            self, text="Select Mode", font=ctk.CTkFont(size=35)
        )
        self.modeLayout.grid(row=3, column=0, padx=75, pady=(0, 50), sticky="s")
        self.liveButton = ctk.CTkButton(
            self, text="Live", command=self.liveMode, font=ctk.CTkFont(size=35)
        )
        self.processInput = None
        self.liveButton.grid(row=3, column=1, pady=(0, 50), sticky="s")
        self.notLiveButton = ctk.CTkButton(
            self, text="Not Live", command=self.notLiveMode, font=ctk.CTkFont(size=35)
        )
        self.notLiveButton.grid(row=3, column=2, pady=(0, 50), sticky="s")

    def chooseScheduler(self, choise):
        self.schedulerType = choise

    def inputProcesses(self):
        if self.processInput is None or not self.processInput.winfo_exists():
            if (
                self.schedulerType == "Priority (Preemptive)"
                or self.schedulerType == "Priority (Non-Preemptive)"
            ):
                self.processInput = ProcessPriorityInputFrame(
                    self, int(self.noOfProcessEntry.get())
                )
            elif self.schedulerType == "Round Robin":
                self.processInput = ProcessRRInputFrame(
                    self, int(self.noOfProcessEntry.get())
                )
            else:
                self.processInput = ProcessInputFrame(
                    self, int(self.noOfProcessEntry.get())
                )
            self.processInput.attributes("-topmost", "true")
        else:
            self.processInput.focus()

    def liveMode(self):
        self.mode = "live"
        if self.schedulerType is None:
            CTkMessagebox(title="Error", message="Please select a scheduler")
        else:
            self.inputProcesses()

    def notLiveMode(self):
        self.mode = "not live"
        self.inputProcesses()

    def schedule(self):
        if (
            self.schedulerType == "Priority (Preemptive)"
            or self.schedulerType == "Priority (Non-Preemptive)"
        ):
            arrivalTime = [int(i[0].get()) for i in self.processInput.processesObject]
            burstTime = [int(i[1].get()) for i in self.processInput.processesObject]
            priority = [int(i[2].get()) for i in self.processInput.processesObject]
            self.processes = [
                Process(i, j, k, l)
                for i, j, k, l in zip(range(len(burstTime)), burstTime, priority, arrivalTime)
            ]
        else:
            #burstTime = [int(i.get()) for i in self.processInput.processesObject]
            arrivalTime = [int(process[0].get()) for process in self.processInput.processesObject]
            burstTime = [int(process[1].get()) for process in self.processInput.processesObject]

            self.processes = [
                Process(i, j, arrivalTime=k) for i, j, k in zip(range(len(burstTime)), burstTime, arrivalTime)
            ]
        if self.schedulerType == "Round Robin":
            self.timeQuantum = int(self.processInput.timeQuantum.get())
            print(self.timeQuantum)
        self.processInput.destroy()
        self.processInput.update()

        if self.schedulerType == "FCFS":
            self.SchedulingStrategy = FCFS()
        if self.schedulerType == "SJF (Preemptive)":
            self.SchedulingStrategy = PSJF()
        if self.schedulerType == "SJF (Non-Preemptive)":
            self.SchedulingStrategy = NPSJF()
        if self.schedulerType == "Priority (Preemptive)":
            self.SchedulingStrategy = PP()
        if self.schedulerType == "Priority (Non-Preemptive)":
            self.SchedulingStrategy = NPP()
        if self.schedulerType == "Round Robin":
            self.SchedulingStrategy = RR()

        if self.mode == "live":
            self.scheduler = Scheduler(
                self.SchedulingStrategy, self.processes, live=True
            )
            if self.schedulerType == "Round Robin":
                self.scheduler.set_quantumTime(self.timeQuantum)
            self.master.liveMode(self.scheduler, self.schedulerType, len(self.processes))
        elif self.mode == "not live":
            self.scheduler = Scheduler(
                self.SchedulingStrategy, self.processes, live=False
            )
            if self.schedulerType == "Round Robin":
                self.scheduler.set_quantumTime(self.timeQuantum)
            self.master.notLiveMode(self.scheduler)

# class ProcessInputFrame(ctk.CTkToplevel):
#     def __init__(self, master, noOfProcess):
#         super().__init__(master)
#         self.geometry("400x300")
#         self.title("Process Input")
#         self.noOfProcess = noOfProcess
#         self.processesObject = []
#         self.grid_rowconfigure((0, self.noOfProcess + 2), weight=1)
#         self.grid_columnconfigure((0, 1), weight=1)
#         self.burstTimeLayout = ctk.CTkLabel(
#             self, text="Burst Time", font=ctk.CTkFont(size=25)
#         )
#         self.burstTimeLayout.grid(row=0, column=1)
#         self.addProcess()
#         self.scheduleButton = ctk.CTkButton(
#             self, text="Schedule", command=master.schedule
#         )
#         self.scheduleButton.grid(
#             row=self.noOfProcess + 3, column=0, columnspan=2, pady=(0, 10), sticky="s"
#         )

#     def addProcess(self):
#         for i in range(1, self.noOfProcess + 1):
#             processId = ctk.CTkLabel(
#                 self, text="P" + str(i - 1) + ":", font=ctk.CTkFont(size=20)
#             )
#             processId.grid(row=i, column=0, padx=(0, 10), sticky="e")
#             burstTime = ctk.CTkEntry(self, placeholder_text="Enter Burst Time")
#             burstTime.grid(row=i, column=1, pady=(0, 2))
#             self.processesObject.append(burstTime)

class ProcessInputFrame(ctk.CTkToplevel):
    def __init__(self, master, noOfProcess):
        super().__init__(master)
        self.geometry("400x300")
        self.title("Process Input")
        self.noOfProcess = noOfProcess
        self.processesObject = []
        self.grid_rowconfigure((0, self.noOfProcess + 2), weight=1)
        self.grid_columnconfigure((0, 2), weight=1)
        self.processIdLayout = ctk.CTkLabel(
            self, text="Process ID", font=ctk.CTkFont(size=20)
        )
        self.processIdLayout.grid(row=0, column=0, padx=(0, 10), sticky="e")
        self.arrivalTimeLayout = ctk.CTkLabel(
            self, text="Arrival Time", font=ctk.CTkFont(size=20)
        )
        self.arrivalTimeLayout.grid(row=0, column=1, padx=(0, 10), sticky="e")
        self.burstTimeLayout = ctk.CTkLabel(
            self, text="Burst Time", font=ctk.CTkFont(size=20)
        )
        self.burstTimeLayout.grid(row=0, column=2)
        self.addProcess()
        self.scheduleButton = ctk.CTkButton(
            self, text="Schedule", command=master.schedule
        )
        self.scheduleButton.grid(
            row=self.noOfProcess + 3, column=0, columnspan=3, pady=(0, 10), sticky="s"
        )

    def addProcess(self):
        for i in range(1, self.noOfProcess + 1):
            processId = ctk.CTkLabel(
                self, text="P" + str(i - 1) + ":", font=ctk.CTkFont(size=15)
            )
            processId.grid(row=i, column=0, padx=(0, 10), sticky="e")
            arrivalTime = ctk.CTkEntry(self, placeholder_text="Enter Arrival Time")
            arrivalTime.grid(row=i, column=1, pady=(0, 2))
            burstTime = ctk.CTkEntry(self, placeholder_text="Enter Burst Time")
            burstTime.grid(row=i, column=2, pady=(0, 2))
            self.processesObject.append((arrivalTime, burstTime))


# class ProcessPriorityInputFrame(ProcessInputFrame):
#     def __init__(self, master, noOfProcess):
#         super().__init__(master, noOfProcess)
#         self.priorityLayout = ctk.CTkLabel(
#             self, text="Priority", font=ctk.CTkFont(size=25)
#         )
#         self.priorityLayout.grid(row=0, column=2)
#         self.scheduleButton.grid(columnspan=3)

#     def addProcess(self):
#         for i in range(1, self.noOfProcess + 1):
#             processId = ctk.CTkLabel(
#                 self, text="P" + str(i - 1) + ":", font=ctk.CTkFont(size=20)
#             )
#             processId.grid(row=i, column=0, padx=(0, 10), sticky="e")
#             burstTime = ctk.CTkEntry(self, placeholder_text="Enter Burst Time")
#             burstTime.grid(row=i, column=1, pady=(0, 2))
#             priority = ctk.CTkEntry(self, placeholder_text="Enter Priority")
#             priority.grid(row=i, column=2, pady=(0, 2))
#             self.processesObject.append((burstTime, priority))

class ProcessPriorityInputFrame(ProcessInputFrame):
    def __init__(self, master, noOfProcess):
        super().__init__(master, noOfProcess)
        self.geometry(f"600x{100 + 35 * (noOfProcess + 2)}")
        self.priorityLayout = ctk.CTkLabel(
            self, text="Priority", font=ctk.CTkFont(size=25)
        )
        self.priorityLayout.grid(row=0, column=3)
        self.scheduleButton.grid(row=noOfProcess + 3, column=0, columnspan=4, pady=(0, 10), sticky="s")

    def addProcess(self):
        for i in range(1, self.noOfProcess + 1):
            processId = ctk.CTkLabel(
                self, text="P" + str(i - 1) + ":", font=ctk.CTkFont(size=15)
            )
            processId.grid(row=i, column=0, padx=(0, 10), sticky="e")
            arrivalTime = ctk.CTkEntry(self, placeholder_text="Enter Arrival Time")
            arrivalTime.grid(row=i, column=1, pady=(0, 2))
            burstTime = ctk.CTkEntry(self, placeholder_text="Enter Burst Time")
            burstTime.grid(row=i, column=2, pady=(0, 2))
            priority = ctk.CTkEntry(self, placeholder_text="Enter Priority")
            priority.grid(row=i, column=3, pady=(0, 2), padx=(0, 10))
            self.processesObject.append((arrivalTime, burstTime, priority))





class ProcessRRInputFrame(ProcessInputFrame):
    def __init__(self, master, noOfProcess):
        super().__init__(master, noOfProcess)
        self.timeQuantum = ctk.CTkEntry(self, placeholder_text="Enter Time Quantum")
        self.timeQuantum.grid(row=noOfProcess + 2, column=0, columnspan=2)
