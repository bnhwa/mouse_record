from __future__ import print_function
"""
===============================================================================
Overview
===============================================================================

The mouse-picture program takes a photo of the background, and saves it into
the user-specified directory. The generated photos are time-stamped and in
.jpg format.
"""


__author__ = "Bailey Nozomu Hwa <hwab@janelia.hhmi.org>"
__date__ = "$Aug 05, 2015, 3:36 PM$"

import argparse
import picamera
import datetime
import os


def main(*argv):
    """
       The program takes a photo of the background when run and saves it into a user-specified directory.

        Args:
            argv(str):                      Arguments are stored as a list

        Notes:
            these are the parameters of the arguments.

            folder(str):                    File directory


    """

    # Directory is stored here
    parser = argparse.ArgumentParser(
        description=" Takes photo of background saves to a directory."
    )
    parser.add_argument(
        "folder",
        nargs='?',
        type=str,
        default=os.getcwd(),
        help="Directory to picture to (default is current working directory)."
    )
    args = parser.parse_args(argv[1:])
    folder = args.folder
    if not os.path.exists(folder):
        os.makedirs(folder)

    with picamera.PiCamera(framerate=90) as camera:
        j = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")
        camera.capture(os.path.join(
            folder, "background-" + str(j) + os.extsep + "jpg"
        ))

    return 0
