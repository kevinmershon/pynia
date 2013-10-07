# pynia

- - -
#### This is a fork of David Ng's (discontinued?) pynia project on Google Code: http://code.google.com/p/pynia/
- - -

# Getting started
## Dependencies
* http://code.google.com/p/pyglet/
* http://libusb.wiki.sourceforge.net/
* http://sourceforge.net/projects/pyusb/
* http://sourceforge.net/projects/numpy/
* http://webpy.org/

On Mac it's simply enough to run `pip install pyglet pyusb numpy web.py`. On GNU/Linux I had to compile and install the libusb code. Also, see the [Troubleshooting - Access Denied section](#access-denied-warning-on-gnulinux).

## Usage
There are two user interfaces for pyNIA: pyglet and HTML5.
### pyglet
![pyglet](/screenshots/pynia-pyglet.png)

The pyglet interface has a histogram of the 6 BrainFingers at top, a spectograph that I don't understand in the bottom left, and a general compiled waveform of the raw output from the device in the bottom right.

#### running it
I never got pyglet working on Mac, but it works fine on GNU/Linux. Simply run `python pynia.py`.
### HTML5
![html5](/screenshots/pynia-http.png)

[Click here for the annotated version](/screenshots/pynia-http-annotated.png). The HTML5 interface has the same histogram as the pyglet version at top, but the other two images are different. The bottom left has a distorted hexagon I have nicknamed the Brain Shape, where the distortion to each vertex is determined by a specific BrainFinger. The hexagon is bluer when all frequencies are low, redder when beta frequencies are high, and greener when alpha frequencies are high. The bottom right is a historical graph of all six BrainFinger values, instead of a single compiled waveform.

#### running it
1. You will need to install CoffeeScript, have `coffee` on your path, and run `batch/coffee-compile.sh`. Alternatively, you can use [Coffee2JS](http://js2coffee.org/#coffee2js) to convert `/src/coffee/index.coffee` and save the output to `static/js/index.js`.
2. Once you have compiled the CoffeeScript code, run `python http.py` and visit `http://localhost:8080`.

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

# Credits
The original documentation of the project follows:

>#### This is a simple GUI to play with the NIA on Mac and Linux until OCZ release a set of drivers for these platforms.
>
>It requires the following dependencies:
>* http://code.google.com/p/pyglet/
>* http://libusb.wiki.sourceforge.net/
>* http://sourceforge.net/projects/pyusb/
>* http://sourceforge.net/projects/numpy/
