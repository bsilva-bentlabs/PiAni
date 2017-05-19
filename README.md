The PiAni project is currently in Beta state
**************

At this point, PiAni should probably only be used by people with some Linux and Python experience.

I'm working on making an installer for PiAni and adding some detailed install instructions, but it'll take a week or two.

If you'd like to write some instructions or help in any other way, send me an email!  I'd love help.

Meanwhile, if you saw the project at Maker Faire and are interested in building your own robot, please send me an email and I'll put you on the mailing list.   We should have it easier to install quickly, my grandsons are looking forward to bulding stuff too.
bsilva@bentlabs.org

That being said, the code here works.  The P2.py is purely experimental and will be moved to a branch soon.

To use you simply need a Raspberry Pi, any version will work, and an Adafruit 16 channel servo controller.  You can use either the PiHat version or the smaller version, but the smaller one requires more electronics experience to setup.
https://www.adafruit.com/product/2327
https://www.adafruit.com/product/815

To run, follow the Adafruit instructions to install the Python drivers for the 16 channel servo controller.
https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/overview

Download the Piani code (use the 'git' commmand, Brad needs to put better instructions here)

Hook up a couple of servos and you can use the "keyboard-servo-test.py" application to test your servos.  The left and right arrows select which servo is moving and the up and down arrows move the servo.  

Most of the time, when you've built a robot, you won't use the full range of motion of the servo, just a slice of it.  Also, in most robots when you move the left and right arms, one servo will increase to move the arm up and the other servo will decrease to move the arm up.   You can use the "keyboard-servo-test.py" app to determine the position numbers for the fully-down and fully up positions.   One of the nice features of PiAni is that you put these numbers into a servo definitions file for your robot and then in your program, you can simply move both arms down and PiAni will figure out which way the servo should turn.

The other advantage of the servo definition file is that after you've written a performance for your robot, if you ever change a servo or make other changes to your robot, you can simply change the servo definitions, rather than having to re-write your performance.

To see how to write your own code, look at the "testbed_servo_def.py" and "MyNameIsTetbed-1.py" files.

And check back, this will get better documented, I promise.

Cheers,
Brad 
