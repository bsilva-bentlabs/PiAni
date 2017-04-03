#!/usr/bin/python
import PiAni as PiAni
import testbed_servo_def

s=PiAni.PiAni(testbed_servo_def.servo_def)

#bring everything home and rest for .5 seconds.
s.set("mouth",1,0.1)
s.set("head-tilt",50,0.1)
s.set("arm-l",1,0.1)
s.set("arm-r",1,0.1)
s.pause(.3)

#3-1 1.2s
s.set("head-tilt",70,.2)
s.set("arm-r",100,0.3)
s.set("arm-r", 60,.15)
s.sync()
s.mplay("sounds/TB-HiImTestbed-3-1.wav","mouth")
s.set("arm-r",100,.15)
s.set("arm-r", 60,.15)
s.set("arm-r",100,.15)
s.set("arm-r", 60,.15)
s.set("arm-l", 60,.15)
s.sync()
s.set("arm-r",100,.85)
s.set("arm-l",100,.85)
s.sync()

#3-2, 1.6s
s.pause(.1)
s.mplay("sounds/TB-HiImTestbed-3-2.wav","mouth")
s.set("arm-r",10,1.2)
s.set("arm-l",10,1.2)
s.set("head-tilt",80,.6)
s.set("head-tilt",50,1)
s.sync()

#3-3 1.9s
s.pause(.35)
s.mplay("sounds/TB-HiImTestbed-3-3.wav","mouth")
s.set("arm-r",30,1.2)
s.set("arm-l",30,1.2)
s.set("head-tilt",80,.32)
s.set("head-tilt",65,.32)
s.set("head-tilt",80,.32)
s.set("head-tilt",65,.32)
s.set("head-tilt",80,.32)
s.set("head-tilt",65,.32)
s.sync()

#3-4, 2.9s
s.pause(.2)
s.mplay("sounds/TB-HiImTestbed-3-4.wav","mouth")
s.set("arm-r",30,.2)
s.set("arm-l",30,.2)
s.set("arm-r",50,.2)
s.set("arm-l",50,.2)
s.set("arm-r",30,.2)
s.set("arm-l",30,.2)
s.set("arm-r",31,.4)
s.set("arm-r",99,1.)
s.set("head-tilt",80,.2)
s.set("head-tilt",60,.2)
s.set("head-tilt",80,.2)
s.set("head-tilt",60,.2)
s.set("head-tilt",90,1.5)
s.set("arm-r",50,.4)
s.sync()

#3-5 5.7s
s.pause(.25) 
s.mplay("sounds/TB-HiImTestbed-3-5.wav","mouth")
s.set("arm-r",20,1.2)
s.set("arm-l",20,1.2)
s.set("head-tilt",45,1.2)
s.set("head-tilt",60,.25)
s.set("head-tilt",45,1.45)
#s.sync()
s.set("head-tilt",80,.2)
s.set("head-tilt",85,.32)
s.set("arm-r",20,1.2)
s.set("arm-l",20,1.2)
s.sync()


while True:
  s.run_exec_array()
  nb = raw_input('Press Enter to loop: ')
