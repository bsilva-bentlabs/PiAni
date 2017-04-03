#!/usr/bin/python

import curses
from Adafruit_PWM_Servo_Driver import PWM
import time

def main(stdscr):
    # Initialise the PWM device using the default address
    pwm = PWM(0x40)
    pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
    pos = 300
    servo = 0

    # do not wait for input when calling getch
    stdscr.nodelay(1)
    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:

            if c == 259:
                pos += 1
            if c == 258:
                pos -= 1
            if c == 260:
                if servo > 0:
                    servo -= 1
            if c == 261:
                if servo < 15:
                    servo += 1
            # return curser to start position
            stdscr.move(0, 0)
            # print numeric value
            stdscr.addstr(str(c) + ' ' )
            stdscr.move(1, 0)
            stdscr.addstr('Servo: ' + str(servo) + '  Pos: ' + str(pos) + '   ')
            stdscr.refresh()

            pwm.setPWM(servo, 0, pos)


if __name__ == '__main__':
    curses.wrapper(main)
