# example of a plugin with atb bar and its own private window + gl-context:

from glfw import *
from plugin import Plugin
from gl_utils import draw_gl_points_norm

from ctypes import c_float
import atb
from gl_utils import adjust_gl_view,clear_gl_screen,basic_gl_setup

# window calbacks
def on_resize(window,w, h):
    active_window = glfwGetCurrentContext()
    glfwMakeContextCurrent(window)
    adjust_gl_view(w,h,window)
    glfwMakeContextCurrent(active_window)
    

class drEYEve(Plugin):
    
    STOP = 0
    BACKWARD = 1
    NORMAL_SPEED = 2
    HIGH_SPEED = 3
    LEFT = 4
    RIGHT = 5
    #the border of the different area within the frame
    LEFT_BORDER = 0.35
    RIGHT_BORDER = 0.65
    UP_BORDER = 0.65
    DOWN_BORDER = 0.05
    #Threshold frames
    FRAME_WAIT = 12

    def __init__(self,g_pool,atb_pos=(10,320)):
        Plugin.__init__(self)

        self.g_pool = g_pool

        self.window_should_open = False
        self.window_should_close = False
        self._window = None
        
        self.pupil_display_list = []
        self.nb_frame = 0
        
        #To get the state Value
        def get_state(data):
            return data.value


        #ATB variables
        self.state_enum = atb.enum("State",{"Stop":self.STOP, "Backward":self.BACKWARD,"Normal Speed":self.NORMAL_SPEED,"High Speed":self.HIGH_SPEED,"Left":self.LEFT,"Right":self.RIGHT})
        self.gaze_x = c_float(0.0)
        self.gaze_y = c_float(0.0)

        # Creating an ATB Bar.
        atb_label = "drEYEve"
        self._bar = atb.Bar(name =self.__class__.__name__, label=atb_label,
            help="state of drEYEve project", color=(50, 50, 50), alpha=100,
            text='light', position=atb_pos,refresh=.3, size=(300, 100))
        
        self.state_data = c_int(0)
        
        self._bar.add_var("Current state", vtype=self.state_enum, getter=get_state, data=self.state_data, readonly=True)
        self._bar.add_var("Gaze X", self.gaze_x, readonly=True)
        self._bar.add_var("Gaze Y", self.gaze_y, readonly=True)

    def do_open(self):
        if not self._window:
            self.window_should_open = True

    def open_window(self):
        if not self._window:
            if self.fullscreen.value:
                monitor = glfwGetMonitors()[self.monitor_idx.value]
                mode = glfwGetVideoMode(monitor)
                height,width= mode[0],mode[1]
            else:
                monitor = None
                height,width= 640,360

            self._window = glfwCreateWindow(height, width, "Plugin Window", monitor=monitor, share=None)
            if not self.fullscreen.value:
                glfwSetWindowPos(self._window,200,0)

            on_resize(self._window,height,width)

            #Register callbacks
            glfwSetWindowSizeCallback(self._window,on_resize)
            glfwSetKeyCallback(self._window,self.on_key)
            glfwSetWindowCloseCallback(self._window,self.on_close)

            # gl_state settings
            active_window = glfwGetCurrentContext()
            glfwMakeContextCurrent(self._window)
            basic_gl_setup()

            # refresh speed settings
            glfwSwapInterval(0)

            glfwMakeContextCurrent(active_window)
            self.window_should_open = False


    def on_close(self,window=None):
        self.window_should_close = True

    def close_window(self):
        if self._window:
            glfwDestroyWindow(self._window)
            self._window = None
            self.window_should_close = False


    def update(self,frame,recent_pupil_positions,events):
        
        for pt in recent_pupil_positions:
            if pt['norm_gaze'] is not None:
                self.nb_frame = self.nb_frame + 1
                if self.nb_frame > self.FRAME_WAIT: 
                    
                    #self.LEFT
                    if (pt['norm_gaze'][0] < self.LEFT_BORDER) and (self.state_data.value!=self.BACKWARD):
                        self.previous_state = self.state_data.value
                        self.state_data.value = self.LEFT
                        self.nb_frame = 0
                    elif (self.state_data.value == self.LEFT) and (pt['norm_gaze'][0] > self.LEFT_BORDER):
                        if self.previous_state == self.STOP:
                            self.state_data.value = self.STOP
                            self.nb_frame = 0
                        else:
                            self.state_data.value = self.NORMAL_SPEED
                            self.nb_frame = 0
                    #self.RIGHT
                    elif (pt['norm_gaze'][0] > self.RIGHT_BORDER) and (self.state_data.value!=self.BACKWARD):
                        self.previous_state = self.state_data.value
                        self.state_data.value = self.RIGHT
                        self.nb_frame = 0
                    elif (self.state_data.value == self.RIGHT) and (pt['norm_gaze'][0] < self.RIGHT_BORDER):
                        if self.previous_state == self.STOP:
                            self.state_data.value = self.STOP
                            self.nb_frame = 0
                        else:
                            self.state_data.value = self.NORMAL_SPEED
                            self.nb_frame = 0
                    #NORMAL SPEED
                    elif (pt['norm_gaze'][1]>self.UP_BORDER) and (self.state_data.value==self.STOP):
                        self.state_data.value = self.NORMAL_SPEED
                        self.nb_frame = 0
                    elif (pt['norm_gaze'][1]<self.DOWN_BORDER) and (self.state_data.value==self.HIGH_SPEED):
                        self.state_data.value = self.NORMAL_SPEED
                        self.nb_frame = 0
                    
                    #HIGH SPEED
                    elif (pt['norm_gaze'][1]>self.UP_BORDER) and (self.state_data.value==self.NORMAL_SPEED):
                        self.state_data.value = self.HIGH_SPEED
                        self.nb_frame = 0
                    #self.BACKWARD
                    elif (pt['norm_gaze'][1]<self.DOWN_BORDER) and (self.state_data.value==self.STOP):
                        self.state_data.value = self.BACKWARD
                        self.nb_frame = 0
                    
                    #self.STOP
                    elif (pt['norm_gaze'][1]>self.UP_BORDER) and (self.state_data.value==self.BACKWARD):
                        self.state_data.value = self.STOP
                        self.nb_frame = 0
                    elif (pt['norm_gaze'][1]<self.DOWN_BORDER) and (self.state_data.value==self.NORMAL_SPEED):
                        self.state_data.value = self.STOP
                        self.nb_frame = 0
                    
                #END if nb_frame > FRAME_WAIT    
                
                self.gaze_x.value = pt['norm_gaze'][0]
                self.gaze_y.value = pt['norm_gaze'][1]
                   
                
                self.pupil_display_list.append(pt['norm_gaze'])
            #END if pt
                
        self.pupil_display_list[:-3] = []


        if self.window_should_close:
            self.close_window()

        if self.window_should_open:
            self.open_window()
            

    def gl_display(self):
        """
        use gl calls to render on world window
        """
        if self.gaze_x == 0:
            draw_gl_points_norm(self.pupil_display_list,size=60,color=(1.,.5,.5,.6))
        if self.gaze_x == 1:
            draw_gl_points_norm(self.pupil_display_list,size=60,color=(.5,1.,.5,.6))

        # gl stuff that will show on the world window goes here:

        if self._window:
            self.gl_display_in_window()

    def gl_display_in_window(self):
        active_window = glfwGetCurrentContext()
        glfwMakeContextCurrent(self._window)

        clear_gl_screen()

        # gl stuff that will show on your plugin window goes here

        glfwSwapBuffers(self._window)
        glfwMakeContextCurrent(active_window)



    def cleanup(self):
        """gets called when the plugin get terminated.
        This happends either volunatily or forced.
        if you have an atb bar or glfw window destroy it here.
        """
        if self._window:
            self.close_window()
        self._bar.destroy()