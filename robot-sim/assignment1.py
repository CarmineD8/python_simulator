from __future__ import print_function
import time
from sr.robot import *

R = Robot()
""" instance of the class Robot"""
a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4

def drive_rot(speed, seconds):
    """
    Function for setting a linear velocity and an angular velocity
    """
    R.motors[0].m0.power = speed*2
    R.motors[0].m1.power = 0
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def find_silver_token():
    """
    Function to find the closest silver token

    Returns:
	dist (float): distance of the closest silver token (-1 if no silver token is detected)
	rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.rot_y<30.0 and token.rot_y>-30.0:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return 100, -1
    else:
   	return dist, rot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
	dist (float): distance of the closest golden token (-1 if no golden token is detected)
	rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist=100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_GOLD and ((token.dist < dist and token.rot_y<25 and token.rot_y>-25) or (token.dist < 0.5 and token.rot_y<90.0 and token.rot_y>-90.0)):
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return 100, -1
    else:
   	return dist, rot_y
   	
def check_right_side():
    dist = 100
    #print (R.see())
    for token in R.see():
         if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.rot_y<90.0 and token.rot_y>60.0:
             dist=token.dist
             #print(token.rot_y)
    if dist==100:
	return 100
    else:
   	return dist
   	
def check_left_side():
    dist = 100
    #print (R.see())
    for token in R.see():
         if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.rot_y>-90.0 and token.rot_y<-60.0:
             dist=token.dist
             #print(token.rot_y)
    if dist==100:
	return 100
    else:
   	return dist
  	
while 1:
    dist, rot_y = find_silver_token()
    go = True
    if dist < 2.0:
        go=False
        dist2, rot2_y = find_golden_token()
        if dist2 > 0.0 and dist2 <0.8:
            go=True
        if dist==-1: # if no token is detected, we make the robot turn 
	    pass
        elif dist <d_th: # if we are close to the token, we try grab it.
            print("Found it!")
            if R.grab(): # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
	        turn(30, 2)
	        #drive(20,2)
	        R.release()
	        #drive(-20,2)
	        turn(-30,2)
	    else:
                print("Aww, I'm not close enough.")
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
	    print("Ah, that'll do.")
            drive(50, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)
    if (go):    
        drive(50,.05) #we move the robot forward
        dist, rot_y = find_golden_token()
        init=True
        left=True
        if dist > 0.0 and dist <0.8:
    	    while True:
                if(init):
                    dist_r=check_right_side()
                    dist_l=check_left_side() 
                    print(dist_r)
                    print(dist_l)
                    if(dist_r>dist_l):
                        left=True
                    else:
                        left=False
                    init=False
                
                if(left):
                    turn(10,0.1)
                else:
                    turn(-10,0.1)
                dist, rot_y = find_golden_token()
                if dist>2.0:
                    break
         
        

	
