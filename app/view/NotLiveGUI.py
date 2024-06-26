
import customtkinter as ctk
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.model.process.Status import Status

class NotLiveFrame(ctk.CTkFrame):
    def __init__(self, master, scheduler):
        super().__init__(master)

        self.scheduler = scheduler

        self.grid_rowconfigure((0,5), weight=1)
        self.grid_columnconfigure((0,0), weight=1)

        self.gnattLabel = ctk.CTkLabel(self, text="Gnatt Chart", font=ctk.CTkFont(size=50))
        self.gnattLabel.grid(row = 0, column = 0,
                             pady=10,
                             columnspan=2)
        
        processTime = self.calculateProcessTime()

        #building the gnatt chart
        fig, ax = plt.subplots()
        fig.set_size_inches(8,4)

        color_cycle = iter(cm.tab10.colors)

        legend_patches = []
        xrange = [0]
        for i, (process, slices) in enumerate(processTime):
            start = 0
            colour = next(color_cycle)

            if process is not None:
                legend_patches.append(mpatches.Patch(color=colour, label=f"Process{process.getProcessId()}"))
                for (sliceStart, sliceEnd) in slices:
                    ax.barh(0, sliceEnd - sliceStart, left=sliceStart, height=0.25, color=colour)
                    # ax.text((sliceStart + sliceEnd)/2, 0, "Process"+str(process.getProcessId()), ha='center', va='center', color='black')
                    start = sliceEnd
            xrange.append(start)
        ax.set_xticks(xrange)
        ax.xaxis.grid(True)
        plt.yticks([])
        ax.legend(handles=legend_patches, loc='upper right', bbox_to_anchor=(1, 1))
        ax.set_ylim(-0.25, 0.5)
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 1, column = 0, columnspan=2, pady=10)

        self.avgWaitingTimeLabel = ctk.CTkLabel(self, text=f"Average Waiting Time: {scheduler.getAverageWaitingTime()}", font=ctk.CTkFont(size=20, weight="bold"))
        self.avgWaitingTimeLabel.grid(row = 2, column = 0, pady=10)
        # self.avgWaitingTimeAnsLabel = ctk.CTkLabel(self, text = str(scheduler.getAverageWaitingTime()), font=ctk.CTkFont(size=20))
        # self.avgWaitingTimeAnsLabel.grid(row=2, column=1, sticky='w')
        self.avgTurnaroundTimeLabel = ctk.CTkLabel(self, text=f"Average Turnaround Time: {scheduler.getAverageTurnaroundTime()}", font=ctk.CTkFont(size=20, weight="bold"))
        self.avgTurnaroundTimeLabel.grid(row = 3, column = 0)
        # self.avgTurnaroundTimeAnsLabel = ctk.CTkLabel(self, text = str(scheduler.getAverageTurnaroundTime()), font=ctk.CTkFont(size=20))
        # self.avgTurnaroundTimeAnsLabel.grid(row=3, column=1, sticky='w')

    def calculateProcessTime(self):
        i = 0
        runningP = self.scheduler.progress()
        
        time = [(runningP, [(i, i+1)])]

        while(True):            
            for j, (process, slices) in enumerate(time):
                if runningP is not None:
                    if process is None:
                        continue
                    if process.getProcessId() == runningP.getProcessId():
                        slices.append((i, i+1))
                        time[j] = (process, slices)
                        break
            else:
                time.append((runningP, [(i, i+1)]))
            if not self.scheduler.has_processes():
                break
            runningP = self.scheduler.progress()                
            i+=1
            
        return time

