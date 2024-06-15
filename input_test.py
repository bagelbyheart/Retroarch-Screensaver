#!/usr/bin/env python3
"""
Background input tester
"""

__author__ = "Stephen Ancona"
__version__ = "0.1.0"
__license__ = "The Unlicense"


import os
import pygame


def start_pygame():
    os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    joysticks = [
        pygame.joystick.Joystick(x)
        for x in range(pygame.joystick.get_count())
    ]


def input_loop():
    while True:
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
                print('input seen')


def main():
    start_pygame()
    input_loop()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    try:
        main()
    except KeyboardInterrupt:
        print("Ending!")
