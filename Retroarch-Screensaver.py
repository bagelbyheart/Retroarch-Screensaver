#!/usr/bin/env python3
"""
Use Retroarch as a screensaver to show off your ROM collection.
"""

__author__ = "Stephen Ancona"
__version__ = "0.3.0"
__license__ = "The Unlicense"


from sys import exit
import argparse
import os
import random
import subprocess
import pygame
from time import time


"""
TODO:
- [PEP 257: Docstring Conventions](https://peps.python.org/pep-0257/)
- Library Import as a more generic launch random y thing for x time
- Reduce messages printed to screen/add proper debugging
"""


def path_listing(directory):
    listing = []
    for p, d, f in os.walk(directory):
        for file in f:
            full_path = os.path.join(p, file)
            listing.append(full_path)
    return (listing)


def pick_random(listing):
    random.shuffle(listing)
    selection = listing.pop()
    return (selection)


def start_pygame():
    os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    joysticks = [
        pygame.joystick.Joystick(x)
        for x in range(pygame.joystick.get_count())
    ]


def rom_loop(retroarch_bin, core_file, rom_dir, timeout):
    # this doesn't currently end the RA process when the parent python process
    # ends, and I'm not sure on the best way to handle that. Maybe also run the
    # subprocess in a multiprocess container?
    global retroarch
    start_time = int(round(time()))
    end_time = start_time + timeout
    roms = path_listing(rom_dir)
    while len(roms) > 0:
        rom = pick_random(roms)
        print(f'{len(roms)}: {rom}')
        print(f'next refresh at {end_time}')
        try:
            retroarch = subprocess.Popen([retroarch_bin, '-L', core_file, rom])
        except None:
            print('Exception!')
        while True:
            if retroarch.poll() is not None:
                retroarch.terminate()
                end_time = int(round(time())) + timeout
                break
            for event in pygame.event.get():
                if event.type == pygame.JOYDEVICEADDED:
                    joysticks = [
                        pygame.joystick.Joystick(x)
                        for x in range(pygame.joystick.get_count())
                    ]
                if (
                        event.type == pygame.JOYBUTTONUP or
                        event.type == pygame.JOYHATMOTION or
                        event.type == pygame.JOYAXISMOTION
                        ):
                    end_time = int(round(time())) + 600
                    print(f'input seen; next refresh at {end_time}')
            if int(round(time())) >= end_time:
                retroarch.terminate()
                end_time = int(round(time())) + timeout
                break
    rom_loop(retroarch_bin, core_file, rom_dir, timeout)


def main(args):
    """ Main entry point of the app """
    if os.path.isfile(args.retroarch_bin):
        retroarch_bin = args.retroarch_bin
    else:
        print(f'{args.retroarch_bin} is not a directory.')
        exit(1)
    if os.path.isdir(args.rom_dir):
        rom_dir = args.rom_dir
    else:
        print(f'{args.rom_dir} is not a directory.')
        exit(1)
    # replace this with an optional cmdline argument
    timeout = args.timeout
    if os.path.isfile(args.core_file):
        core_file = args.core_file
    else:
        print(f'{args.core_file} is not a file.')
        exit(1)
    print(args)
    start_pygame()
    rom_loop(retroarch_bin, core_file, rom_dir, timeout)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("retroarch_bin", help="Retroarch binary")
    parser.add_argument("rom_dir", help="ROM file directory")
    parser.add_argument("core_file", help="Libretro core file")
    parser.add_argument(
        "-t", "--timeout", action="store", dest="timeout", type=int,
        help="Time between game changes", default=300
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        retroarch.kill()
        print("Ending!")
