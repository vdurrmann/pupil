#This file must update a variable "state" which will see its value change according to the eye position and the previous state

#The STOP state has to be completed by detecting the EYE_CLOSED case
#The case switches should only be possible when the smartglasses are in CONTROL_MODE, which should be detecting by the DOUBLE_BLINK case


from glfw import *
from ctypes import c_float
import atb

# window calbacks
#def on_resize(window,w, h):
 #   active_window = glfwGetCurrentContext()
 #   glfwMakeContextCurrent(window)
 #   adjust_gl_view(w,h,window)
 #   glfwMakeContextCurrent(active_window)


class navigator:
#the possible states
    STOP = 0
    BACKWARD = 1
    NORMAL_SPEED = 2
    HIGH_SPEED = 3
    LEFT = 4
    RIGHT = 5
#the border of the different area within the frame
    LEFT_BORDER = 0.35
    RIGHT_BORDER = 0.75
    UP_BORDER = 0.75
    DOWN_BORDER = 0.35

    def __init__(state):
	state = STOP

    def update_state(state, previous_state, frame, recent_pupil_positions):
	for pt in recent_pupil_positions:
	    if pt['norm_gaze'] is not None:
		
#LEFT
		if (pt['norm_gaze'][0] < LEFT_BORDER) and (state!=BACKWARD):
		    previous_state = state
		    state = LEFT
		    while pt['norm_gaze'][0] < LEFT_BORDER:
		    if previous_state == STOP:
			state = STOP
		    else :
			state = NORMAL_SPEED
		
#RIGHT
		if (pt['norm_gaze'][0] > RIGHT_BORDER) and (state!=BACKWARD):
		    previous_state = state
		    state = RIGHT
		    while pt['norm_gaze'][0] > RIGHT_BORDER:
		    if previous_state == STOP:
			state = STOP
		    else :
			state = NORMAL_SPEED
		
#NORMAL SPEED
		if (pt['norm_gaze'][1]>UP_BORDER) and (state==STOP):
		    state = NORMAL_SPEED
		if (pt['norm_gaze'][1]<DOWN_BORDER) and (state==HIGH_SPEED):
		    state = NORMAL_SPEED
		
#HIGH SPEED

		if (pt['norm_gaze'][1]>UP_BORDER) and (state==NORMAL_SPEED):
		    state = HIGH_SPEED
#BACKWARD
		if (pt['norm_gaze'][1]<DOWN_BORDER) and (state==STOP):
		    state = BACKWARD
		
#STOP
		if (pt['norm_gaze'][1]>UP_BORDER) and (state==BACKWARD):
		    state = STOP
		if (pt['norm_gaze'][1]<DOWN_BORDER) and (state==NORMAL_SPEED):
		    state = STOP
#TO be completed by detecting the EYE_CLOSED case
