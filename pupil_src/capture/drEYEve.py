# example of a plugin with atb bar and its own private window + gl-context:

from glfw import *
from plugin import Plugin
from gl_utils import draw_gl_points_norm

from ctypes import c_int,c_bool
import atb
from gl_utils import adjust_gl_view,clear_gl_screen,basic_gl_setup


# window calbacks
def on_resize(window,w, h):
    active_window = glfwGetCurrentContext()
    glfwMakeContextCurrent(window)
    adjust_gl_view(w,h,window)
    glfwMakeContextCurrent(active_window)
    

class drEYEve(Plugin):

    
    def __init__(self,g_pool,atb_pos=(10,320)):
        Plugin.__init__(self)

        self.g_pool = g_pool

        self.window_should_open = False
        self.window_should_close = False
        self._window = None
        
        self.pupil_display_list = []
       
            
        #primary_monitor = glfwGetPrimaryMonitor()

        
        #To get the state Value
        def get_state(data):
            return data.value
        #To set the state Value
        def set_state(newSate):
            self.state=newState
        

        atb_label = "drEYEve"
        # Creating an ATB Bar.
        self._bar = atb.Bar(name =self.__class__.__name__, label=atb_label,
            help="state of drEYEve project", color=(50, 50, 50), alpha=100,
            text='light', position=atb_pos,refresh=.3, size=(300, 100))
        
        self.state_enum = atb.enum("State",{"Stop":0, "Backward":1,"Normal Speed":2,"High Speed":3})
        self.state = c_int(0)
        
        self._bar.add_var("Current state", vtype=self.state_enum,setter=set_state,getter=get_state, readonly=True)
        self._bar.add_var("State", self.state, readonly=True)

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
                if pt['norm_gaze'][0] < 0.40:
                    self.state.value = 1
                    print "Inferieur"
                if pt['norm_gaze'][0] > 0.40:
                    self.state.value = 0  
                    print "superieur"  
                
                self.pupil_display_list.append(pt['norm_gaze'])
        self.pupil_display_list[:-3] = []

        
        
        if self.window_should_close:
            self.close_window()

        if self.window_should_open:
            self.open_window()
            

    def gl_display(self):
        """
        use gl calls to render on world window
        """
        if self.state == 0:
            draw_gl_points_norm(self.pupil_display_list,size=35,color=(1.,.5,.5,.6))
        if self.state == 1:
            draw_gl_points_norm(self.pupil_display_list,size=35,color=(.5,1.,.5,.6))

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