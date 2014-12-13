#The state of the wheelchair's motor according to the system state calculated thanks to the Navigaotr unit

# The emergency stop case still have to be added
from navigator import update_state

class wheelchair:
#the possible speed for the wheelchair motors.
#This file is only here for a test, as we cannot afford having a wheelchair and the motor capacities would change according to the model
    STOP = 0
    BACKWARD = 1
    NORMAL_SPEED = 2
    HIGH_SPEED = 3
    LEFT = 4
    RIGHT = 5

    def __init__(motor_speed, state):
	state_stop(motor_speed, state)
#Stop
    def state_stop(motor_speed, state):
	motor_speed = STOP
	while(state==STOP):
	if state = LEFT:
	     state_left(motor_speed,state)
	if state = RIGHT:
	     state_right(motor_speed,state)
	if state = NORMAL_SPEED:
	     state_normalspe(motor_speed,state)
	if state = BACKWARD:
	     state_backward(motor_speed,state)
	
#Left
    def state_left(motor_speed, state)
	motor_speed = LEFT
	while(state==LEFT):
	if state==STOP:
	     state_stop(motor_speed, state)
	else :
	     state_normalspe(motor_speed,state)

#Right
    def state_right(motor_speed, state)
	motor_speed = RIGHT
	while(state==RIGHT):
	if state==STOP:
	     state_stop(motor_speed, state)
	else :
	     state_normalspe(motor_speed,state)

#Normal speed
    def state_normalspe(motor_speed, state)
	motor_speed = NORMAL_SPEED
	while(state==NORMAL_SPEED):
	if state = LEFT:
	     state_left(motor_speed,state)
	if state = RIGHT:
	     state_right(motor_speed,state)
	if state = HIGH_SPEED:
	     state_highspe(motor_speed,state)
	if state = STOP:
	     state_stop(motor_speed,state)

#High speed
    def state_highspe(motor_speed, state)
	motor_speed = HIGH_SPEED
	while(state==HIGH_SPEED):
	if state = LEFT:
	     state_left(motor_speed,state)
	if state = RIGHT:
	     state_right(motor_speed,state)
	if state = NORMAL_SPEED:
	     state_normalspe(motor_speed,state)

#Backward
    def state_backward(motor_speed, state)
	motor_speed = BACKWARD
	while(state==BACKWARD):
	state_stop(motor_speed, state)



