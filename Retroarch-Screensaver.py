#!/usr/bin/env python3
"""
Use Retroarch as a screensaver to show off your ROM collection.
"""

__author__ = "Stephen Ancona"
__version__ = "0.1.0"
__license__ = "The Unlicense"

import argparse
import os
import random
import subprocess
import pygame
from multiprocessing import Process


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
    return(selection)


def rom_loop(ra_path, core_file, rom_dir, timeout):
    # this doesn't currently end the RA process when the parent python process
    # ends, and I'm not sure on the best way to handle that. Maybe also run the
    # subprocess in a multiprocess container?
    roms = path_listing(rom_dir)
    while len(roms) > 0:
        rom = pick_random(roms)
        print(f'{len(roms)}: {rom}')
        try:
            subprocess.run([ra_path, '-L', core_file, rom], timeout=timeout)
        except subprocess.TimeoutExpired:
            pass
        except:
            print("Exception!")
    rom_loop(ra_path, core_file, rom_dir, timeout)


def input_loop(ra_path, core_file, rom_dir, timeout):
    os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    game_loop = Process(target=rom_loop, args=(ra_path, core_file, rom_dir, timeout))
    game_loop.start()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYDEVICEADDED:
                joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            if event.type == pygame.JOYBUTTONUP:
                print("input seen!")
                # this is successfully killing python, but not the retroarch
                # child process and I don't know how to fix that
                game_loop.terminate()
                exit()


def main(args):
    """ Main entry point of the app """
    if os.path.isdir(args.retroarch_dir):
        retroarch_dir = args.retroarch_dir
    else:
        print(f'{args.retroarch_dir} is not a directory.')
        exit(1)
    if os.path.isdir(args.rom_dir):
        rom_dir = args.rom_dir
    else:
        print(f'{args.rom_dir} is not a directory.')
        exit(1)
    # replace this with an optional cmdline argument
    timeout = 30
    if os.path.isfile(os.path.join(retroarch_dir, 'cores', args.core_file)):
        core_file = os.path.join(retroarch_dir, 'cores', args.core_file)
    else:
        print(f'{args.core_file} is not a file.')
        exit(1)
    print(args)
    ra_path = os.path.join(retroarch_dir, 'retroarch.exe')
    input_checker = Process(target=input_loop, args=(ra_path, core_file, rom_dir, timeout))
    input_checker.start()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()
    parser.add_argument("retroarch_dir", help="Retroarch install directory")
    parser.add_argument("rom_dir", help="ROM file directory")
    parser.add_argument("core_file", help="Libretro core file")
    # Optional argument which requires a parameter (eg. -d test)
    # parser.add_argument("-n", "--name", action="store", dest="name")
    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))
    args = parser.parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print("Ending!")
