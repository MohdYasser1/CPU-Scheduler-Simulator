import customtkinter as ctk
from model.process.Process import Process
import matplotlib.pyplot as plt
import matplotlib.cm as cm 
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LiveFrame(ctk.CTkFrame):
    def __init__(self, master, scheduler, schedulerType, noOfProcess):
        super().__init__(master)

        self.scheduler = scheduler
        self.schedulerType = schedulerType
        self.noOfProcess = noOfProcess
        self.currentTime = 0
        self.run = True

        self.grid_rowconfigure((0, 1), weight=3)
        self.grid_columnconfigure((0), weight=1)
        self.grid_columnconfigure((1), weight=5)

        self.inputProcessFrame = ctk.CTkFrame(self)
        self.inputProcessFrame.grid(row=0, column=0, rowspan=1, sticky = 'snew', padx=(10, 10), pady=(10, 10)) 
        self.inputProcessFrame.grid_columnconfigure((0), weight=1)

        self.summaryFrame = ctk.CTkFrame(self)
        self.summaryFrame.grid(row=1, column=0, rowspan=3, sticky = 'snew', padx=(10, 10), pady=(10, 10))

        self.progressFrame = ctk.CTkFrame(self)
        self.progressFrame.grid(row=0, column=1, rowspan=3, sticky = 'snew', padx=(10, 10), pady=(10, 10))

        self.gnattFrame = ctk.CTkFrame(self)
        self.gnattFrame.grid(row=3, column=1, sticky = 'snew', padx=(10, 10), pady=(10, 10))
        
        # Add new process
        self.inputProcessFrame.grid_rowconfigure((0,3), weight=1)
        self.inputProcessLabel = ctk.CTkLabel(self.inputProcessFrame, text="Add new process", font=ctk.CTkFont(size=30, weight="bold"))
        self.addProcessButton = ctk.CTkButton(self.inputProcessFrame, text="Add", command=self.addProcess)
        if (
            schedulerType == 'Priority (Preemptive)'
            or schedulerType == 'Priority (Non-Preemptive)'
            ):
            self.inputProcessFrame.grid_columnconfigure((0,1), weight=1)
            self.inputProcessLabel.grid(row = 0, column = 0, columnspan=2, sticky = 'ew', pady=10)
            self.priorityLayout = ctk.CTkLabel(self.inputProcessFrame, text="Priority", font=ctk.CTkFont(size=20))
            self.priorityLayout.grid(row = 1, column = 1, pady=10)
            self.priority = ctk.CTkEntry(self.inputProcessFrame, placeholder_text="Enter Priority")
            self.priority.grid(row=2, column=1, pady=10)
            self.addProcessButton.grid(row=3, column=0, columnspan=2, pady=10)
        else:
            self.inputProcessLabel.grid(row = 0, column = 0, sticky = 'ew', pady=10)
            self.addProcessButton.grid(row = 3, column = 0, pady=10)

        self.burstTimeLayout = ctk.CTkLabel(self.inputProcessFrame, text="Burst Time", font=ctk.CTkFont(size=20))
        self.burstTimeLayout.grid(row=1, column=0, pady=10)
        self.burstTime = ctk.CTkEntry(self.inputProcessFrame, placeholder_text="Enter Burst Time")
        self.burstTime.grid(row=2, column=0, pady=10)

        # Create Summary Section
        self.summaryFrame.grid_rowconfigure((0, 1), weight=1)
        self.summaryFrame.grid_columnconfigure((0), weight=1)
        self.AvgWaitingTime = ctk.CTkLabel(self.summaryFrame, text="Average Waiting Time: -", font=ctk.CTkFont(size=20, weight="bold"))
        self.AvgWaitingTime.grid(row=0, column=0)
        self.AvgTurnaroundTime = ctk.CTkLabel(self.summaryFrame, text="Average Turnaround Time: -", font=ctk.CTkFont(size=20, weight="bold"))
        self.AvgTurnaroundTime.grid(row=1, column=0)

        # Create Process Progress Section
        self.progressFrame.grid_rowconfigure((0, self.noOfProcess + 1), weight=1)
        self.progressFrame.grid_columnconfigure((0), weight=1)
        self.progressFrame.grid_columnconfigure((1), weight=5)
        self.progressFrame.grid_columnconfigure((2,3), weight=1)
        remainingTimeLabel = ctk.CTkLabel(self.progressFrame, text="Remaining Burst", font=ctk.CTkFont(size=20))
        remainingTimeLabel.grid(row=0, column=2, pady=10, padx=3)
        waitingTimeLabel = ctk.CTkLabel(self.progressFrame, text="Status", font=ctk.CTkFont(size=20))
        waitingTimeLabel.grid(row=0, column=3, pady=10, padx=3)
        self.elapsedTime = ctk.CTkLabel(self.progressFrame, text= f"Elapsed time: {self.currentTime} sec", font=ctk.CTkFont(size=20))
        self.elapsedTime.grid(row=0, column=0, pady=10, padx=3)
        self.processProgress = []
        self.remainingTime = []
        self.status = []
        for process in self.scheduler.get_processes():
            processLabel = ctk.CTkLabel(self.progressFrame, text=f"P{process.getProcessId()}:", font=ctk.CTkFont(size=20))
            processLabel.grid(row=process.getProcessId() + 1, column=0, pady=10, padx=2)
            processProgressBar = ctk.CTkProgressBar(self.progressFrame)
            processProgressBar.grid(row=process.getProcessId() + 1, column=1, pady=10, padx = 2)
            processProgressBar.set(0)
            self.processProgress.append(processProgressBar)
            remainingTime = ctk.CTkLabel(self.progressFrame, text=f"{process.getBurstTime()} sec", font=ctk.CTkFont(size=20))
            remainingTime.grid(row=process.getProcessId() + 1, column=2, pady=10, padx=3)
            self.remainingTime.append(remainingTime)
            status = ctk.CTkLabel(self.progressFrame, text=f"{process.getStatus()}", font=ctk.CTkFont(size=20))
            status.grid(row=process.getProcessId() + 1, column=3, pady=10, padx=3)
            self.status.append(status)

        # Create gnatt chart section
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(8,2)
        self.ax.xaxis.grid(True)
        plt.yticks([])
        self.ax.set_ylim(-0.25, 0.5)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.gnattFrame)
        self.canvas.get_tk_widget().grid(row = 0, column = 0)

        # Start Simulation
        self.runningP = self.scheduler.progress()
        self.time = [(self.runningP, [(self.currentTime, self.currentTime+1)])]
        self.startSimulation()
        

    def addProcess(self):
        self.noOfProcess += 1
        if (
            self.schedulerType == 'Priority (Preemptive)'
            or self.schedulerType == 'Priority (Non-Preemptive)'
            ):
            process = Process(self.noOfProcess - 1, int(self.burstTime.get()), int(self.priority.get()))
            self.priority.delete(0, 'end')
        else:
            process = Process(self.noOfProcess - 1, int(self.burstTime.get()))
        self.scheduler.add_process(process)
        self.burstTime.delete(0, 'end')
        self.progressFrame.grid_rowconfigure((0, self.noOfProcess + 1), weight=1)
        processLabel = ctk.CTkLabel(self.progressFrame, text=f"P{process.getProcessId()}:", font=ctk.CTkFont(size=20))
        processLabel.grid(row=process.getProcessId() + 1, column=0, pady=10, padx=2)
        processProgressBar = ctk.CTkProgressBar(self.progressFrame)
        processProgressBar.grid(row=process.getProcessId() + 1, column=1, pady=10, padx = 2)
        processProgressBar.set(0)
        self.processProgress.append(processProgressBar)
        remainingTime = ctk.CTkLabel(self.progressFrame, text=f"{process.getBurstTime()} sec", font=ctk.CTkFont(size=20))
        remainingTime.grid(row=process.getProcessId() + 1, column=2, pady=10, padx=3)
        self.remainingTime.append(remainingTime)
        status = ctk.CTkLabel(self.progressFrame, text=f"{process.getStatus()}", font=ctk.CTkFont(size=20))
        status.grid(row=process.getProcessId() + 1, column=3, pady=10, padx=3)
        self.status.append(status)
        if self.run==False:
            self.startSimulation()
        

    def startSimulation(self):
        for j, (process, slices) in enumerate(self.time):
            if self.runningP is not None:
                if process.getProcessId() == self.runningP.getProcessId():
                    slices.append((self.currentTime, self.currentTime+1))
                    self.time[j] = (process, slices)
                    break
        else:
            self.time.append((self.runningP, [(self.currentTime, self.currentTime+1)]))
        if not self.scheduler.has_processes():
            self.stopSimulation()
        self.runningP = self.scheduler.progress()
        self.currentTime += 1
    
        self.updateGUI(self.time)
        self.after(1000, self.startSimulation)

    def updateGUI(self, processTime):
        self.ax.clear()
        self.color_cycle = iter(cm.tab10.colors)
        self.legend_patches = []
        self.xrange = [0]
        for i, (process, slices) in enumerate(processTime):
            start = 0
            colour = next(self.color_cycle)
            self.legend_patches.append(mpatches.Patch(color=colour, label=f"Process{process.getProcessId()}"))
            if process is not None:
                for (sliceStart, sliceEnd) in slices:
                    self.ax.barh(0, sliceEnd - sliceStart, left=sliceStart, height=0.25, color=colour)
                    # ax.text((sliceStart + sliceEnd)/2, 0, "Process"+str(process.getProcessId()), ha='center', va='center', color='black')
                    start = sliceEnd
            self.xrange.append(start)
        self.ax.set_xticks(self.xrange)
        self.ax.legend(handles=self.legend_patches, loc='upper right', bbox_to_anchor=(1, 1))
        
        self.canvas.draw()

        for process in self.scheduler.get_processes():
            self.processProgress[process.getProcessId()].set(1- (process.getBurstTime()/process.getWorkingTime()))
            self.remainingTime[process.getProcessId()].configure(text=f"{process.getBurstTime()} sec")
            self.status[process.getProcessId()].configure(text=f"{process.getStatus()}")
        self.elapsedTime.configure(text= f"Elapsed time: {self.currentTime} sec")

    def stopSimulation(self):
        self.run = False
        self.AvgWaitingTime.configure(text=f"Average Waiting Time: {self.scheduler.getAverageWaitingTime()}")
        self.AvgTurnaroundTime.configure(text=f"Average Turnaround Time: {self.scheduler.getAverageTurnaroundTime()}")

        




# class MainWindow(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("1200x700")
#         self.title("CPU Scheduler Simulator")
#         self.mainFrame = LiveFrame(self, None, "Priority (Preemptive")
#         self.mainFrame.pack(fill=ctk.BOTH, expand=True)

# if __name__ ==  '__main__':
#     main = MainWindow()
#     main.mainloop()
