from __future__ import print_function

import time
from sr.robot import *

"""
Exercise 2 python script

Put the main code after the definition of the functions. The code should make the robot grab the closest marker (token)
Steps to be performed:
1 - call the function find_token() to retrieve the distance and the angle between the robot and the closest marker
2 - drive the robot towards the marker. If the distance between the robot and the marker is less than d_th
     meters, the robot can grab the marker, by using the method grab() of the class Robot. Otherwise, the 
     robot should be driven toward the token. The robot is a non-holonomic robot, so you should control the 
     angle, by calling the method turn, if rot_y is greater then a_th or lower then -a_th (check the sign!).
     On the contrary, if -a_th < rot_y < a_th, you can use the method drive to move the robot forward.
3 - after you grab the marker, you can exit the program (function exit()).

   When done, run with:
	$ python run.py solutions/exercise2_solution.py
"""


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

R = Robot()
""" instance of the class Robot"""


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

def find_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
	return -1, -1
    else:
   	return dist, rot_y


while 1:
    dist, rot_y = find_token()  # we look for markers
    if dist==-1:
       	print("I don't see any token!!")
	exit()  # if no markers are detected, the program ends
    elif dist <d_th: 
        print("Found it!")
        R.grab() # if we are close to the token, we grab it.
        print("Gotcha!") 
        exit()
    elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
       print("Ah, here we are!.")
       drive(10, 0.5)
    elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
       print("Left a bit...")
       turn(-2, 0.5)
    elif rot_y > a_th:
       print("Right a bit...")
       turn(+2, 0.5)
	
