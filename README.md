# pynia

- - -
#### This is a fork of David Ng's (discontinued?) pynia project on Google Code: http://code.google.com/p/pynia/
The original documentation of the project follows:

>#### This is a simple GUI to play with the NIA on Mac and Linux until OCZ release a set of drivers for these platforms.
>
>It requires the following dependencies:
>* http://code.google.com/p/pyglet/
>* http://libusb.wiki.sourceforge.net/
>* http://sourceforge.net/projects/pyusb/
>* http://sourceforge.net/projects/numpy/

- - -

# Troubleshooting
#### Versions
I ran into quite a few problems getting **pynia** working. David Ng's project
had 2 fairly different versions of the code. I'm going to be developing
primarily off the version **0.0.1** codebase because it required less
modifications to make it functional, and it also has much better documentation.
#### "Access Denied" warning on GNU/Linux
By default, libusb doesn't provide read/write access to USB devices. In order to
get **pynia** working on Linux without root privileges, you need to add an
exception for the NIA to your udev rules in `/etc/udev/rules.d` (a sample file
has been included in the `udev` folder of this repo), and then you need to run
the command `udevadm control --reload-rules` to reload the rules. After that,
unplug the NIA and plug it back in.

# License #
#### [MIT License](http://opensource.org/licenses/mit-license.php)
