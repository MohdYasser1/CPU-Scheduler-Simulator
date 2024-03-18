import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("750x450")
        self.title("CPU Scheduler Simulator")

        self.grid_rowconfigure((0,6), weight=1)
        self.grid_columnconfigure((0,1), weight=1)

        self.titleLabel = ctk.CTkLabel(self, text="CPU Scheduler", font=ctk.CTkFont(size=70, weight="bold"))
        self.titleLabel.grid(row = 0, column = 0, columnspan=2)
        self.schedulerSelectLayout = ctk.CTkLabel(self, text="Select Scheduler", font=ctk.CTkFont(size=25))
        self.schedulerSelectLayout.grid(row = 1, column = 0)

        schedules = ["FCFS", "SJF (Preemptive)", "SJF (Non-Preemptive)", "Priority (Preemptive)", "Priority (Non-Preemptive)", "Round Robin"]
        self.dropdown = ctk.CTkOptionMenu(self, values = schedules)
        self.dropdown.grid(row = 1, column = 1)


if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()