from __future__ import print_function

__author__ = "Bailey Nozomu Hwa <hwab@janelia.hhmi.org"
__date__ = "$July 30, 2015 20:20:18 EDT$"

import argparse
import io
import time
import picamera
import datetime
import os


def main(*argv):
    """
        Simple main function. Defines arguments: time before and after the initiation of a trigger event,
        and directory of the file to be saved into.

        Args:
            args = parser.parse_args(argv[1:]):     All arguments stored as list

            folder = args.folder:                   File directory
            x = args.before:                        Time to record before (in seconds)
            y = args.after:                         Time to record after (in seconds)
            z = x + y                               Total buffer size (in seconds)


    """

    # Time to record before and after as well as directory are stored here
    parser = argparse.ArgumentParser(description="seconds before and after lever is pressed.")
    parser.add_argument("before", type=int, help="seconds to record before.")
    parser.add_argument("after", type=int, help="seconds to record after.")
    parser.add_argument("folder", type=str, default='.', help="mouse to be tested")
    args = parser.parse_args(argv[1:])

    folder = args.folder
    x = args.before
    y = args.after
    z = x + y

    # sets up trigger event for the recordings, i.e., GPIO 27
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.IN, GPIO.PUD_UP)

    with picamera.PiCamera(framerate=90) as camera:
        try:
            # Creates directory/folder if the desired directory is nonexistent
            if not os.path.exists(folder):
                os.makedirs(folder)
            stream = picamera.PiCameraCircularIO(camera, seconds=z)
            while True:
                # Up until now, the program defines the arguments and settings for the Raspberry Pi camera and trigger event(GPIO 27)
                # The code below provides the recording protocol for the stream, based on the initiation of the trigger event
                stream.seek(0)
                camera.start_recording(stream, format="h264", splitter_port=1)
                GPIO.wait_for_edge(27, GPIO.FALLING)
                camera.wait_recording(y, splitter_port=1)
                camera.stop_recording()

                for frame in stream.frames:
                    if frame.frame_type == picamera.PiVideoFrameType.sps_header:
                        stream.seek(frame.position)
                        break
                # Gives the time specifications that you want, in
                # year-month-day_hour:minute:second:microsecond
                j = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
                # Responsible for saving and writing the stream to a h264 video file
                with io.open(os.path.join(folder, "mouse_press" + str(j).replace(
                        ' ', '_') + ".h264"), "wb") as output:
                    data = stream.read()
                    if not data:
                        break
                    output.write(data)
        except KeyboardInterrupt:
            print("Program is now ending session.")

    return 0
