#definitions of servo start. stop and inc direction for skel robot
#Will need to be edited when servos or strings are replaced

#because every Python2 program needs this:
from __future__ import division

servo_def={}

# definitions for each servo
# servo_def['short-name']=['Long descriptive name', servo number, minimum position, maximum position]
# 'short-name' is the name that will be used when writing programs to move the servo.
# 'Long descriptive name' is just used to help you remember what this servo does, but may
#  be used in other ways in the future.
# 'servo number' refers to the plug on the Adafruit PWM board.
# 'minimum position' is one extreme position of the servo.  To make thing easy to remember,
#  this should be the lowest position, most inward position or the leftmost position.
# 'maximum position' is the other extreme.  Please note that these are not the furthest
#  the servo can move, but the furthest you want them to move in your design.
# ***** add more description about min/max reverse
# **** make this a class with a method for each item.
servo_def['arm-l']=['Arm left raise',3,234,569]
servo_def['arm-r']=['Arm right raise',2,587,159]
servo_def['mouth']=['mouth open',0,400,290]
servo_def['head-tilt']=['Head tilt',1,495,169]

# class Servo(object):
#
#     def __init__(self, channel, min_val, max_val):
#         self.channel = channel
#         self.min_val = min_val
#         self.max_val = max_val
#
# servo_def['arm-l-r'] = Servo(channel=3,
#            min_val=234,
#            max_val=569)
