import customtkinter as ctk
import threading
import time
from utils import center_window, simulation_switch

global stop_gif 
stop_gif = False

class Simulation(threading.Thread):
  def __init__(self, win, model, params):
    threading.Thread.__init__ (self)
    self.window = win   

    global stop_gif
    stop_gif = False 

    self.waiting_frame = ctk.CTkFrame(self.window)
    self.waiting_frame.grid(row=0, column=0)

    self.gif = Gif(self.waiting_frame)
    self.gif.start()
    
    self.params = params
    self.model = model
    
  def run(self):
    res = str(simulation_switch(self.model, self.params))
    global stop_gif
    stop_gif = True
    self.waiting_frame.grid_remove()
    tabview = ctk.CTkTabview(self.window)
    tabview.pack(padx=20, pady=20)

    tabview.add("tab 1")  # add tab at the end
    tabview.add("tab 2")  # add tab at the end
    tabview.set("tab 2")  # set currently visible tab

    button_1 = ctk.CTkButton(tabview.tab("tab 1"), text=res)
    button_1.pack(padx=20, pady=20)

class Gif(threading.Thread):
  def __init__(self, frame):
    threading.Thread.__init__ (self)
    self.frame = frame

  def run(self):
    label = ctk.CTkLabel(self.frame, text='Running', anchor='center', width=150, text_color='cadetblue', font=('Arial', 25, 'bold'))
    label.grid(row=0, column=0, padx=20, pady=10)
    label2 = ctk.CTkLabel(self.frame, text='...', anchor='center', width=150, text_color='cadetblue', font=('Arial', 25, 'bold'))
    label2.grid(row=2, column=0, padx=20, pady=(0,10))
    while self.frame :
      label2.configure(text='')
      time.sleep(1)
      label2.configure(text='.')
      time.sleep(1)
      label2.configure(text='..')
      time.sleep(1)
      label2.configure(text='...')
      time.sleep(1)
      global stop_gif
      if stop_gif:
        break
    
def call_simulation(current_win, model, params_values):
  window = ctk.CTkToplevel(current_win)
  window.title('Running...')
  window.grid_columnconfigure(0, weight=1)
  center_window(window)

  sim = Simulation(window, model, params_values)
  sim.start()

  window.mainloop()
   

