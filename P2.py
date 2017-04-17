#because every Python2 program needs this:
from __future__ import division
from Adafruit_PWM_Servo_Driver import PWM
import time, os
import wave
import numpy
#import cpickle as pickle

class PiAni :
    instance_counter=0
    time_slice = .01 #time in seconds between steps

    def __init__(self, servo_def):
        PiAni.instance_counter += 1
        if PiAni.instance_counter == 1:
            PiAni.pwm = PWM(0x40)     # Initialise the PWM device using the default address
            PiAni.pwm.setPWMFreq(60)  # Set frequency to 60 Hz

        self.servo_def = servo_def      # Robot motor assignment definitions.
        self.max_servos = 16    # number of servos that can be controlled.
        self.last_time = 1      # current size of movement array
        # Main exec array
        # first index is time / time_slice, i.e in this case 1 entry for every 1/100th of a second.
        self.servo_pos = [[0 for y in xrange(self.max_servos)] for x in xrange(2)]
        #self.servo_pos = [0 for y in xrange(self.max_servos)]           #This will be a two dimensional array as it grows.
        self.servo_pos_extension = [0 for a in xrange(self.max_servos)] #blank set, used to grow self.servo_pos
        self.servo_cur_pos = [0 for y in range(self.max_servos)]                    # current position of each servo
        self.servo_last_time = [0 for y in range(self.max_servos)]                   # Per servo last time in array.  Time is in time_slice steps.
        #event_pos is used for events that occur at a particular time, not sequentially.
        #The event_next and event_next_time variables track the time of the next event.
        #event_pos[time][0=timestamp,1=event-type,=2=event-data]
        #event-type = 1: Sound.  event-data=file path to pass to aplay.
        self.event_pos=[0, 0, ""]
        self.event_pos.append([0, 0, ""])
        self.event_next_time = 0
        self.event_next_entry = 0
        # set starting, at rest, positions.  Currently sets all to minimum.
        # Going to try just having the user set this as the initial position in script.
        #for index in self.servo_def.keys():
        #    self.servo_cur_pos[self.servo_def[index][1]] = self.servo_def[index][2]

    # populate exec array with movements for each time_slice for this servo
    # servo=index on board, min,max=absolute positions from robot-servo-def.py
    # pos=logical position for movement, 1-100 value, secs=time to complete movement
    def set(self, servo_name, pos, secs):
        "Creates a series of entries in the movement array to move the servo to a target position in 'secs' time."
        servo = self.servo_def[servo_name][1]
        smin = self.servo_def[servo_name][2]
        smax = self.servo_def[servo_name][3]
        logical_inc = abs(smax - smin) / 100              # compute 1-100 step size between smin and smax, as pos is expressed as 1-100 value
        if smin > smax:
            mult = -1
        else:
            mult = 1
        target_pos = smin + ((pos * logical_inc) * mult)  # need to determine target position as servo value, instead of 1-100 value
        actual_inc = ((target_pos - self.servo_cur_pos[servo]) / (secs / PiAni.time_slice))  # actual_inc is increment from curr pos to target pos per time slice over seconds to complete move.
        target_time = self.servo_last_time[servo] + int(secs / PiAni.time_slice)
#        print servo, pos, logical_inc, mult, self.servo_cur_pos[servo], target_pos, actual_inc, target_time
        while self.last_time < target_time:     # grow ths servo_pos array until it has enough space to contain this set of movements.
            self.servo_pos.append(self.servo_pos_extension)
            self.last_time += 1
        while self.servo_last_time[servo] < target_time:
            self.servo_last_time[servo] += 1
            self.servo_cur_pos[servo] += actual_inc
            self.servo_pos[self.servo_last_time[servo]][servo] = self.servo_cur_pos[servo]

    # sets the current time for all channels to the highest time in any channel.
    # used to let movements catch up to a commmon point.
    def sync(self):
        "updates time counters so that all current servo movements complete before the next movement starts."
        tmax = max(self.servo_last_time)
        self.servo_last_time = [tmax] * len(self.servo_last_time)

    # Syncs and Pauses insertion of new movements.
    def pause(self, delay):
        "updates time counters so that all current servo movements complete, then moves time counters forward by 'delay' seconds"
        tmax = max(self.servo_last_time)
        self.servo_last_time = int(tmax + (delay / self.time_slice) * len(self.servo_last_time))

    # plays audio file at current time
    def play(self, file):
        "queues an audio file to play at current point in time.  Reccomend using at beginning of file or after a sync()."
        tmax = max(self.servo_last_time)
        self.event_pos.append([0, 0, ""])
        self.event_pos[self.event_next_entry][0] = tmax
        self.event_pos[self.event_next_entry][1] = 1        # Entry type 1 is audio file
        self.event_pos[self.event_next_entry][2] = file
        self.event_next_entry += 1

    # Plays audio file while attempts primitive lip sync of mouth servo.
    # Currently assumes voice will be first (left) channel on multi-channel tracks.
    # This currently uses a very primitive algorythem of opening the mouth based on the signal average
    # looking forward from this time_slice until the next.
    def mplay(self, file, mouth):
        "Same as play, but attempts to move the mouth servo in time to the volume of the audio."
        tmax = max(self.servo_last_time)
        servo = self.servo_def[mouth][1]
        smin = self.servo_def[mouth][2]
        smax = self.servo_def[mouth][3]
        logical_inc = abs(smax - smin)              # compute step size between smin and smax
        if smin > smax:
            mult = -1
        else:
            mult = 1
        #put audio file in event queue.
        self.event_pos.append([0, 0, ""])
        self.event_pos[self.event_next_entry][0] = tmax
        self.event_pos[self.event_next_entry][1] = 1        # entry type 1 is audio file
        self.event_pos[self.event_next_entry][2] = file
        self.event_next_entry += 1
        af = wave.open(file)
        framerate = af.getframerate()
        frames = af.getnframes()
        channels = af.getnchannels()
        width = af.getsampwidth()
        print("sampling rate:", framerate, "Hz, length:", frames, "samples,",
            "channels:", channels, "sample width:", width, "bytes")
        if channels > 1 or width != 2:
            print "At this time, the mplay() method only supports single channel 16 bit .wav files."
            exit(1)
        data = af.readframes(frames)                        # Read audio into buffer.
        af.close()
        sig = numpy.frombuffer(data, dtype='<i2').reshape(-1, channels) # Traslate buffer into usable data.
        frameslice = framerate * self.time_slice
        self.servo_last_time[servo] = tmax
        a = 0
        #while a < frames - frameslice:           # find the peak audio level in each time_slice
        while a < frames - (frameslice * 5):           # find the peak audio level in each time_slice
            b = a - 1
            savg = 0
            #while b <= a + frameslice:
            while b <= a + (frameslice * 5):
                b += 1
                savg += abs(sig[b,0])
            savg = savg / (frameslice * 5)        #try using avg instead
            self.servo_last_time[servo] += 1
            self.servo_cur_pos[servo] = smin + ((savg / 16384) * (logical_inc * mult)) + 1   #convert to usable value, cannot be 0
            self.servo_pos[self.servo_last_time[servo]][servo] = self.servo_cur_pos[servo]
            a += frameslice         # advance counter to next time_slice (I don't need to examime the entire array)

    def print_exec_array(self):
        "prints the servo event array to the console.  Used for debugging."
        tmax = max(self.servo_last_time)
        for a in range(tmax + 1):
            print a, ":",
            for b in self.servo_def.keys():  # Unforuntately, this does not print the values in the expected order.
                print self.servo_pos[a][self.servo_def[b][1]],
            print ""

    #output the values in the array to the servos in time_slice steps.
    def run_exec_array(self):
        "Takes the built servo movement array and sends each movement to the robot."
        self.event_next_entry = 0
        self.event_next_time = self.event_pos[self.event_next_entry][0]
        tmax = max(self.servo_last_time)
        start = time.time()
        cur = 0
        last = 0
        while cur < tmax:
            cur = int((time.time() - start) / PiAni.time_slice)
            if cur == last:
                time.sleep(.003)  # this probably isn't the right way to do this.  sleep until?
            else:
                last = cur
                # For each motor, find the servo port and send the next position to that port
                for a in self.servo_def.keys():
                    if self.servo_pos[cur][self.servo_def[a][1]] > 0:
                        PiAni.pwm.setPWM(self.servo_def[a][1], 0, int(self.servo_pos[cur][self.servo_def[a][1]]))
                if cur >= self.event_next_time:
                    if self.event_pos[self.event_next_entry][1] == 1: # 1=Audio play event
                        cmd = '/usr/bin/aplay ' + self.event_pos[self.event_next_entry][2] + '&'
                        os.system(cmd)
                        self.event_next_entry += 1
                        self.event_next_time = self.event_pos[self.event_next_entry][0]
