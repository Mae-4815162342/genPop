import customtkinter as ctk
import numpy as np

MODELS = ['Hardy-Weinberg', 'Other one']
#(param name, description, min value, max value)
PARAMS = {'Hardy-Weinberg': 
          {
            'pop':('Population size', 10, 10000),
            'p_step':( 'Value of step between two values of p', 1, 100),
            'gens':( 'Number of generations', 1, 100)
          }
          ,
          'Other one':
          {'TUP':( 'Terribly useless param', 5, 4)}
          }

#  new_window = ctk.CTkToplevel(app) 
ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("dark-blue")
APP = ctk.CTk()
PARAMS_FRAME = ctk.CTkFrame(APP)
ERROR_FRAME = ctk.CTkFrame(APP)
MAIN_BUTTON = ctk.CTkButton(APP)
PARAMS_VALUES = {}
CURRENT_MODEL = ''

def combobox_callback(choice):
  instructions.destroy()
  combobox.grid(row = 1, column=0, pady=(20, 10))
  show_params(choice)

def kill_error():
  global ERROR_FRAME
  ERROR_FRAME.destroy()

def center_window():
  global APP
  APP.update()
  current_window_height = APP.winfo_height()
  current_window_width = APP.winfo_width()
  winwidth = APP.winfo_screenwidth()
  winheight = APP.winfo_screenheight()
  geometry = "+" + str(int(winwidth / 2 - current_window_width/2)) + "+" +  str(int(winheight / 2 - current_window_height/2))
  APP.geometry(geometry)
  APP.update()

def display_error_message(errors):
  global PARAMS_FRAME
  global PARAMS_VALUES
  global ERROR_FRAME
  kill_error()
  ERROR_FRAME = ctk.CTkFrame(PARAMS_FRAME, bg_color= 'ivory2')
  ERROR_FRAME.grid(column=0, row=(len(PARAMS_VALUES)*2))
  i = 0

  # for each error message, display in label
  for err in errors:
    error_label = ctk.CTkLabel(ERROR_FRAME, text=err, text_color='lightcoral')
    error_label.grid(column=0, row=i, padx=10, pady=10)
    i += 1

  center_window()

def show_params(model):
  global APP
  global PARAMS_FRAME
  global MAIN_BUTTON
  global PARAMS_VALUES
  global CURRENT_MODEL

  # reinitialisation
  params = PARAMS[model]
  PARAMS_FRAME.destroy()
  MAIN_BUTTON.destroy()
  PARAMS_VALUES = {}
  CURRENT_MODEL = model

  # defining frame
  PARAMS_FRAME = ctk.CTkFrame(APP, fg_color='ivory2')
  PARAMS_FRAME.grid(row=2, column=0)
  PARAMS_FRAME.grid_columnconfigure(0, weight=1)
  i = 0

  # adding params widgets
  for name in params.keys():
    desc, min, max = params[name]
    frame = ctk.CTkFrame(PARAMS_FRAME, fg_color='ivory2')
    frame.grid(row=2*i, column=0, pady=(10, 0), padx=10)

    label = ctk.CTkLabel(frame, text=name)
    label.grid(column=0, row=0, pady=(10, 10), padx=(10, 10))
    value = ctk.CTkEntry(frame, placeholder_text=min)
    value.grid(column=1, row=0, pady=(10, 10), padx=(10, 10))

    desc_text = desc + ' (min: '+ str(min) + ', max: ' + str(max) + ')'
    label = ctk.CTkLabel(PARAMS_FRAME, text=desc_text, text_color='cadetblue', font=('Arial', 10, 'italic'))
    label.grid(row=(2*i + 1), pady=(0, 10), padx=(10, 10))
    PARAMS_VALUES[name] = value
    i += 1
  
  # adding launch button
  MAIN_BUTTON = ctk.CTkButton(APP, command=launch_simulation, corner_radius= 12, text= 'Start simulation', fg_color='cadetblue', hover_color='lightblue4')
  MAIN_BUTTON.grid(row= 2*i + 1, column=0, padx=10, pady=10)
  print(MAIN_BUTTON._hover_color)

  # updating window position
  center_window()



def launch_simulation():
    global PARAMS_VALUES
    global PARAMS
    global CURRENT_MODEL
    params = {}
    can_proceed = True
    errors = []
    kill_error()
    for value in PARAMS_VALUES:
      val = PARAMS_VALUES[value].get()
      int_val = -1

      # if the value is not given
      if len(val) < 1:
        PARAMS_VALUES[value].configure(border_color = 'lightcoral')
        can_proceed = False
        errors.append(str(value) + ' is required')
        continue
      else:
        try:
          int_val = int(val)

        # if the value is not an integer
        except:
          PARAMS_VALUES[value].configure(border_color = 'lightcoral')
          can_proceed = False
          errors.append(str(value) + ' must be an integer')
          continue

        # if the value is outside of defined min and max values
        _, min_val, max_val = PARAMS[CURRENT_MODEL][value]
        if int_val < min_val or int_val > max_val:
          PARAMS_VALUES[value].configure(border_color = 'lightcoral')
          can_proceed = False
          errors.append(str(value) + ' must be selected between ' + str(min_val) + ' and ' + str(max_val))
          continue

        # any other case: the value is conserved
        else:
          params[value] = int_val
          PARAMS_VALUES[value].configure(border_color = 'lightgreen')

    if can_proceed:
      print('can_proceed', params)
    else:
      display_error_message(errors)
      print('cannot_proceed', params)
  




# main APP
ctk.set_appearance_mode("System")     
APP.title('GenPop simulations')


instructions = ctk.CTkLabel(APP, text='Please select a model ')
instructions.grid(row=0, column=0, pady=(30, 10))

combobox = ctk.CTkComboBox(master = APP, values=MODELS, command=combobox_callback, border_color='cadetblue', button_color='cadetblue', button_hover_color='lightblue4')
combobox.grid(row = 1, column=0, pady=(20, 10))
combobox.set('Model selection')

APP.grid_columnconfigure(0, weight=1)
APP.minsize(300, 150)
center_window()
APP.mainloop()