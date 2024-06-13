# Retroarch-Screensaver

Use Retroarch as a faux-screensaver to show off your ROM collection.

## How does it work?

This tool loads Retroarch via it's command line interface, specifying a
libretro core and a random ROM file from a provided directory, runs for five
minutes, then resets with another random ROM file. When controller input is
detected, the reset time is moved to 10 minutes from last input to allow
gameplay.

The tool requires three arguments:

- **Retroarch Path:** The location you installed Retroarch to
- **Core Path:** The path of the libretro core you want to use for the
  screensaver (at this time the screensaver only supports one system at a time)
- **ROM Directory:** The location of the ROM files you want the screensaver to
  cycle through

And takes one optional argument:

- **Timeout:** How long each game should run before loading the next

## Help Output

```output
usage: Retroarch-Screensaver.py [-h] [-t TIMEOUT] [--version] retroarch_dir rom_dir core_file

positional arguments:
  retroarch_dir         Retroarch install directory
  rom_dir               ROM file directory
  core_file             Libretro core file

options:
  -h, --help            show this help message and exit
  -t TIMEOUT, --timeout TIMEOUT
                        Time between game changes
  --version             show program's version number and exit
```

## Requirements

The only python library outside of the standard library used is `pygame2`. This
is required "pick up and play" functionality.

## Build Process

This can be built for executable distribution using `PyInstaller`, I use the
following command to build it in my environment:

```shell
python -m PyInstaller Retroarch-Screensaver.py
```
