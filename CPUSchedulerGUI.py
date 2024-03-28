import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title("CPU Scheduler Simulator")
        self.mainFrame = MainFrame(self)
        self.mainFrame.pack(fill=ctk.BOTH, expand=True)


class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
    
        self.grid_rowconfigure((0,3), weight=1)
        self.grid_columnconfigure((0,2), weight=1)

        self.titleLabel = ctk.CTkLabel(self, text="CPU Scheduler", font=ctk.CTkFont(size=70, weight="bold"))
        self.titleLabel.grid(row = 0, column = 0,
                             pady=50,
                             columnspan=3)

        # Scheduler Selector
        self.schedulerSelectLayout = ctk.CTkLabel(self, text="Select Scheduler", font=ctk.CTkFont(size=25))
        self.schedulerSelectLayout.grid(row = 1, column = 0,
                                         padx=75,
                                         sticky="w")
        schedules = ["FCFS", "SJF (Preemptive)", "SJF (Non-Preemptive)", "Priority (Preemptive)", "Priority (Non-Preemptive)", "Round Robin"]
        self.dropdown = ctk.CTkOptionMenu(self,
                                           values = schedules,
                                           command = self.chooseScheduler)
        self.dropdown.set("Choose Scheduler")
        self.dropdown.grid(row = 1, column = 1,
                           columnspan=2)
        
        # Ready Process Input
        self.noOfProcessLayout = ctk.CTkLabel(self, text="Number of Processes ready:", font=ctk.CTkFont(size=25), anchor="e")
        self.noOfProcessLayout.grid(row = 2, column = 0, padx=75, pady=20, sticky='w')
        self.noOfProcessEntry = ctk.CTkEntry(self, placeholder_text="Enter no. of processes")
        self.noOfProcessEntry.grid(row = 2, column = 1,
                                   columnspan=2)

        # Mode Selection
        self.modeLayout = ctk.CTkLabel(self, text="Select Mode",
                                        font=ctk.CTkFont(size=35))
        self.modeLayout.grid(row = 3, column = 0, padx=75, pady=(0,50), sticky="s")
        self.liveButton = ctk.CTkButton(self, text="Live",
                                         command=self.liveMode,
                                         font=ctk.CTkFont(size=35))
        self.processInput = None
        self.liveButton.grid(row = 3, column = 1,
                              pady=(0,50), 
                              sticky="s")
        self.notLiveButton = ctk.CTkButton(self, text="Not Live",
                                            command=self.notLiveMode,
                                            font=ctk.CTkFont(size=35))
        self.notLiveButton.grid(row = 3, column = 2,
                                pady=(0,50), 
                                sticky="s")
       
    def chooseScheduler(self, choise):            
        self.schedulerType = choise
    
    def inputProcesses(self):
        if self.processInput is None or not self.processInput.winfo_exists():
            if self.schedulerType == "Priority (Preemptive)" or self.schedulerType == "Priority (Non-Preemptive)":
                self.processInput = ProcessPriorityInputFrame(self, int(self.noOfProcessEntry.get()))
            elif self.schedulerType == "Round Robin":
                self.processInput = ProcessRRInputFrame(self, int(self.noOfProcessEntry.get()))
            else:
                self.processInput = ProcessInputFrame(self, int(self.noOfProcessEntry.get()))
            self.processInput.attributes("-topmost", 'true')
        else:
            self.processInput.focus()  

    def liveMode(self):
        self.mode = "live"
        self.inputProcesses()

    def notLiveMode(self):
        self.mode = "not live"
        self.inputProcesses()

    def schedule(self):
        self.processes = [i.get() for i in self.processInput.processesObject]
        if self.schedulerType == "Round Robin":
            self.timeQuantum = self.processInput.timeQuantum.get()
            print(self.timeQuantum)
        self.processInput.destroy()
        self.processInput.update()
        print(self.processes)
        pass

class ProcessInputFrame(ctk.CTkToplevel):
    def __init__(self, master, noOfProcess):
        super().__init__(master)
        self.geometry("400x300")
        self.title("Process Input")
        self.noOfProcess = noOfProcess
        self.processesObject = []
        self.grid_rowconfigure((0, self.noOfProcess+2), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.burstTimeLayout = ctk.CTkLabel(self, text="Burst Time", font=ctk.CTkFont(size=25))
        self.burstTimeLayout.grid(row = 0, column = 1)
        self.addProcess()
        self.scheduleButton = ctk.CTkButton(self, text="Schedule", command=master.schedule)
        self.scheduleButton.grid(row = self.noOfProcess+3, column = 0, columnspan=2, pady=(0,10), sticky='s')

    def addProcess(self):
        for i in range(1, self.noOfProcess+1):
            processId = ctk.CTkLabel(self, text='P'+str(i-1) + ':', font=ctk.CTkFont(size=20))
            processId.grid(row = i, column = 0, padx=(0,10), sticky='e')
            burstTime = ctk.CTkEntry(self, placeholder_text="Enter Burst Time")
            burstTime.grid(row = i, column = 1, pady=(0,2))
            self.processesObject.append(burstTime)


class ProcessPriorityInputFrame(ProcessInputFrame):
    def __init__(self, master, noOfProcess):
        super().__init__(master, noOfProcess)
        self.priorityLayout = ctk.CTkLabel(self, text="Priority", font=ctk.CTkFont(size=25))
        self.priorityLayout.grid(row = 0, column = 2)
        self.scheduleButton.grid(columnspan=3)
    def addProcess(self):
            for i in range(1, self.noOfProcess+1):
                processId = ctk.CTkLabel(self, text='P'+str(i-1) + ':', font=ctk.CTkFont(size=20))
                processId.grid(row = i, column = 0, padx=(0,10), sticky='e')
                burstTime = ctk.CTkEntry(self, placeholder_text="Enter Burst Time")
                burstTime.grid(row = i, column = 1, pady=(0,2))
                priority = ctk.CTkEntry(self, placeholder_text="Enter Priority")
                priority.grid(row = i, column = 2, pady=(0,2))
                self.processesObject.append((burstTime, priority))

class ProcessRRInputFrame(ProcessInputFrame):
    def __init__(self, master, noOfProcess):
        super().__init__(master, noOfProcess)
        self.timeQuantum = ctk.CTkEntry(self, placeholder_text="Enter Time Quantum")
        self.timeQuantum.grid(row = noOfProcess+2, column = 0, columnspan=2)


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()