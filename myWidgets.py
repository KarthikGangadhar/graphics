# Gangadhara, Karthik.
# kxg7851
# 2018-09-06

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been significantly modified and updated by Brian A. Dalio for
# use in CSE 4303 / CSE 5365 in the 2018 Fall semester.

#----------------------------------------------------------------------
import tkinter as tk
import ModelData as modeldata
from tkinter import simpledialog
from tkinter import filedialog
from ModelData import constructTransform
#----------------------------------------------------------------------
class cl_widgets :
  def __init__( self, ob_root_window, ob_world = [] ) :
    self.ob_root_window = ob_root_window
    self.ob_world = ob_world

    self.Clipping = tk.BooleanVar()
    self.Perspective = tk.BooleanVar()
    self.EullerRotate = tk.BooleanVar()
    
    self.menu = cl_menu( self )

    self.toolbar = cl_toolbar( self )

    self.statusBar_frame = cl_statusBar_frame( self.ob_root_window )
    self.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.statusBar_frame.set( 'This is the status bar' )

    self.ob_canvas_frame = cl_canvas_frame( self )
    self.ob_world.add_canvas( self.ob_canvas_frame.canvas )
    
#----------------------------------------------------------------------
class cl_canvas_frame :
  def __init__( self, master ) :
    self.master = master
    self.canvas = tk.Canvas(
      master.ob_root_window, width=1, height=1, bg='skyblue' )

    self.canvas.pack( expand=tk.YES, fill=tk.BOTH )
    self.canvas.bind( '<Configure>',       self.canvas_resized_callback )
    self.canvas.bind( '<ButtonPress-1>',   self.left_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-1>', self.left_mouse_release_callback )
    self.canvas.bind( '<B1-Motion>',       self.left_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-2>',   self.middle_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-2>', self.middle_mouse_release_callback )
    self.canvas.bind( '<B2-Motion>',       self.middle_mouse_down_motion_callback )
    self.canvas.bind( '<ButtonPress-3>',   self.right_mouse_click_callback )
    self.canvas.bind( '<ButtonRelease-3>', self.right_mouse_release_callback )
    self.canvas.bind( '<B3-Motion>',       self.right_mouse_down_motion_callback )
    self.canvas.bind( '<Key>',             self.key_pressed_callback )
    self.canvas.bind( '<Up>',              self.up_arrow_pressed_callback )
    self.canvas.bind( '<Down>',            self.down_arrow_pressed_callback )
    self.canvas.bind( '<Right>',           self.right_arrow_pressed_callback )
    self.canvas.bind( '<Left>',            self.left_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Up>',        self.shift_up_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Down>',      self.shift_down_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Right>',     self.shift_right_arrow_pressed_callback )
    self.canvas.bind( '<Shift-Left>',      self.shift_left_arrow_pressed_callback )

  def key_pressed_callback( self, event ) :
    msg = f'{event.char!r} ({ord( event.char )})' \
      if len( event.char ) > 0 else '<non-printing char>'

    self.master.statusBar_frame.set(
      f'{msg} pressed at ({event.x},{event.y})' )

  def up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Up arrow pressed' )

  def down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Down arrow pressed' )

  def right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Right arrow pressed' )

  def left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Left arrow pressed' )

  def shift_up_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift up arrow pressed' )

  def shift_down_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift down arrow pressed' )

  def shift_right_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift right arrow pressed' )

  def shift_left_arrow_pressed_callback( self, event ) :
    self.master.statusBar_frame.set( 'Shift left arrow pressed' )

  def left_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def left_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def left_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'LMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def middle_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y
    self.canvas.focus_set()

  def middle_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def middle_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'MMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_click_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB down. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def right_mouse_release_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB released. ({event.x}, {event.y})' )
    self.x = None
    self.y = None

  def right_mouse_down_motion_callback( self, event ) :
    self.master.statusBar_frame.set( f'RMB dragged. ({event.x}, {event.y})' )
    self.x = event.x
    self.y = event.y

  def canvas_resized_callback( self, event ) :
    self.canvas.config( width = event.width-4, height = event.height-4 )

    self.master.statusBar_frame.pack( side = tk.BOTTOM, fill = tk.X )
    self.master.statusBar_frame.set(
      f'Canvas width, height ({self.canvas.cget( "width" )}, ' +
      f'{self.canvas.cget( "height" )})' )

    self.canvas.pack()

    self.master.ob_world.redisplay( self.master.ob_canvas_frame.canvas, event )

#----------------------------------------------------------------------
class cl_statusBar_frame( tk.Frame ) :
  def __init__( self, master ) :
    tk.Frame.__init__( self, master )
    self.label = tk.Label( self, bd = 1, relief = tk.SUNKEN, anchor = tk.W )
    self.label.pack( fill = tk.X )

  def set( self, formatStr, *args ) :
    self.label.config( text = 'kxg7851: ' + formatStr % args )
    self.label.update_idletasks()

  def clear( self ) :
    self.label.config( text='' )
    self.label.update_idletasks()

#----------------------------------------------------------------------
class cl_menu :
  def __init__( self, master ) :
    self.master = master
    self.menu = tk.Menu( master.ob_root_window )
    master.ob_root_window.config( menu = self.menu )

    self.filemenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'File', menu = self.filemenu )
    self.filemenu.add_command( label = 'New', command = lambda : self.menu_callback( 'file>new' ) )
    self.filemenu.add_command( label = 'Open...', command = lambda : self.menu_callback( 'file>open' ) )
    self.filemenu.add_separator()
    self.filemenu.add_command( label = 'Exit', command = lambda : self.menu_callback( 'file>exit' ) )

    self.settingsmenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Settings', menu = self.settingsmenu )
    self.settingsmenu.add_checkbutton( label = 'Clipping', onvalue=True, offvalue=False,  variable = self.master.Clipping, command = lambda : self.menu_callback( 'settings>clipping'))
    self.settingsmenu.add_checkbutton( label = 'Perspective', onvalue=True, offvalue=False, variable = self.master.Perspective, command = lambda : self.menu_callback( 'settings>perspective'))
    self.settingsmenu.add_checkbutton( label = 'Euler Rotate', onvalue=True, offvalue=False, variable = self.master.EullerRotate, command = lambda : self.menu_callback( 'settings>Euler Rotate'))
    # self.settingsmenu.add_checkbutton( label = 'Resolution', onvalue=True, offvalue=False, variable = self.master.Resolution, command = lambda : self.menu_callback( 'settings>Resolution'))

    self.helpmenu = tk.Menu( self.menu )
    self.menu.add_cascade( label = 'Help', menu = self.helpmenu )
    self.helpmenu.add_command( label = 'About...', command = lambda : self.menu_callback( 'help>about' ) )

  def menu_callback( self, which = None ) :
    item = 'menu' if which is None else which
    self.master.statusBar_frame.set( f'{item!r} callback' )

#----------------------------------------------------------------------
class cl_toolbar :
  def __init__( self, master ) :
    self.master = master
    self.clmenu = cl_menu(master)
    self.toolbar = tk.Frame( master.ob_root_window )
    self.button = tk.Button( self.toolbar, text = 'Resolution', width = 8, command = self.toolbar_resolution_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Distance', width = 6, command = self.toolbar_perspective_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'ϕ', width = 2, command = self.toolbar_roll_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'θ', width = 2, command = self.toolbar_pitch_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'ψ', width = 2, command = self.toolbar_yaw_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Reset', width = 4, command = self.toolbar_reset_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Load', width = 3, command = self.toolbar_load_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.button = tk.Button( self.toolbar, text = 'Draw', width = 3, command = self.toolbar_draw_callback )
    self.button.pack( side = tk.LEFT, padx = 2, pady = 2 )
    self.toolbar.pack( side = tk.TOP, fill = tk.X )
    self.model = {}
    self.height = 0
    self.width = 0
    self.distance = 1.0
    self.roll = 0.0
    self.pitch = 0.0
    self.yaw = 0.0
    self.resolution = 4

  def toolbar_perspective_callback( self ) :
    distance = simpledialog.askfloat("Distance", "Enter Distance", initialvalue=1.0, minvalue=1.0)
    if distance != None:
      self.distance = distance
      self.master.statusBar_frame.set( 'Perspective callback, distance set to {0}'.format(self.distance))
    else:
      self.master.statusBar_frame.set( 'Perspective callback distance Cancelled, distance {0} is retained'.format(self.distance))
  
  def toolbar_yaw_callback(self):
    yaw = simpledialog.askfloat("yaw(ψ)", "Enter Angle", initialvalue=0.0)
    if yaw != None:
      self.yaw = yaw
      self.master.statusBar_frame.set( 'Euler Rotate callback, ψ set to {0}'.format(self.yaw))
    else:
      self.master.statusBar_frame.set( 'Euler Rotate callback Cancelled, ψ {0} is retained'.format(self.yaw))
  
  def toolbar_roll_callback(self):
    roll = simpledialog.askfloat("roll(ϕ)", "Enter Angle", initialvalue=0.0)
    if roll != None:
      self.roll = roll
      self.master.statusBar_frame.set( 'Euler Rotate callback, ϕ set to {0}'.format(self.roll))
    else:
      self.master.statusBar_frame.set( 'Euler Rotate callback Cancelled, ϕ {0} is retained'.format(self.roll))

  def toolbar_resolution_callback(self):
    resolution = simpledialog.askinteger("Resolution", "Enter Resolution", initialvalue=4, minvalue=4)
    if resolution != None:
      self.resolution = resolution
      self.master.statusBar_frame.set( 'Resolution callback, Resolution set to {0}'.format(self.resolution))
    else:
      self.master.statusBar_frame.set( 'Resolution callback Cancelled, Resolution {0} is retained'.format(self.resolution))

  def toolbar_pitch_callback(self):
    pitch = simpledialog.askfloat("pitch(θ)", "Enter Angle", initialvalue=0.0)
    if pitch != None:
      self.pitch = pitch
      self.master.statusBar_frame.set( 'Euler Rotate callback, θ set to {0}'.format(self.pitch))
    else:
      self.master.statusBar_frame.set( 'Euler Rotate callback Cancelled, θ {0} is retained'.format(self.pitch))

  def toolbar_reset_callback( self ) :
    self.master.ob_world.reset()
    self.master.statusBar_frame.set( 'Reset callback' )

  def toolbar_load_callback( self ) :
    self.master.statusBar_frame.set( 'Load callback' )
    fName = tk.filedialog.askopenfilename( filetypes = [ ("text files","*.txt"),("python files","*.py") ] )
    if len(fName) > 0:
      self.model = modeldata.ModelData(fName)

  def toolbar_draw_callback( self ) :
    if not self.model:
      return
      
    self.master.ob_world.reset()
    self.master.statusBar_frame.set( 'Draw callback' )
    self.height = int(self.master.ob_canvas_frame.canvas.cget( 'height' ))
    self.width = int(self.master.ob_canvas_frame.canvas.cget( 'width' ))
    window = self.model.m_Window
    viewport = self.model.m_Viewport
    transform = constructTransform( window, viewport, self.width, self.height )
    self.model.specifyTransform(*transform, self.distance)
    self.model.specifyEulerAngles(self.roll, self.pitch, self.yaw)
    self.master.ob_world.create_graphic_objects( self.model, self.master.ob_canvas_frame.canvas, self.master.Clipping.get() ,self.master.Perspective.get(), self.master.EullerRotate.get(), self.resolution)
#----------------------------------------------------------------------
