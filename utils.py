import models.Hardy_Weinberg.simulation as HW

def simulation_switch(model, params):
  res = 'fail'
  match model:
    case 'Hardy-Weinberg':
      print('yes')
      pop = params['pop']
      p_step = params['p_step']
      gens = params['gens']
      res = HW.simulation([p_step, pop, gens])
      print([p_step, pop, gens])
    case 'Other one':
      print('fail')
  return res

def center_window(win):
  win.update()
  current_window_height = win.winfo_height()
  current_window_width = win.winfo_width()
  winwidth = win.winfo_screenwidth()
  winheight = win.winfo_screenheight()
  geometry = "+" + str(int(winwidth / 2 - current_window_width/2)) + "+" +  str(int(winheight / 2 - current_window_height/2))
  win.geometry(geometry)
  win.update()
