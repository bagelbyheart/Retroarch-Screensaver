# Retroarch-Screensaver

Use Retroarch as a screensaver to show off your ROM collection.

## How does it work?

This tool loads Retroarch via it's command line interface, specifying a
libretro core and a random ROM file from a provided directory, runs for five
minutes, then resets with another random ROM file.

The tool accepts three arguments:

- **Retroarch Path:** The location you installed Retroarch to
- **Core Path:** The path of the libretro core you want to use for the
  screensaver (at this time the screensaver only supports one system at a time)
- **ROM Directory:** The location of the ROM files you want the screensaver to
  cycle through
