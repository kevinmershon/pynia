import pyglet
import sys
import threading
import nia as NIA

# global scope stuff
backgound = pyglet.image.load('static/images/pynia.png')
step = pyglet.image.load('static/images/step.png')
nia = None
nia_data = None

def update(x):
    """
        The main pyglet loop. This function starts a data collection thread,
        whilst processing and displying the previously collected data. At the
        end of the loop the threads are joined
    """
    window.clear()

    # kick-off processing data from the NIA
    data_thread = threading.Thread(target=nia_data.get_data)
    data_thread.start()

    # fill in the background image
    backgound.blit(0, 0)

    # get the fourier data from the NIA
    data, steps = nia_data.fourier(nia_data)

    # render an Intensity-based graph of the data
    image = pyglet.image.ImageData(160, 140, 'I', data)
    image.blit(20, 20)

    # render step scales of the 'brain-fingers'
    for i in range(6):  # this blits the brain-fingers blocks
        for j in range(int(steps[i])):
            step.blit(i*50+100, j*15+200)

    # get a waveform of the last 1 second of data
    data = nia_data.waveform()

    # render an RGB graph of the waveform data
    image = pyglet.image.ImageData(410, 140, 'RGB', data)
    image.blit(210, 20)

    # wait for the next batch of data to come in
    data_thread.join()

    # exit if we cannot read data from the device
    if nia_data.AccessDeniedError:
        sys.exit(1)

if __name__ == "__main__":
    """
        The main function opens the NIA, creates a pyglet window, and then
        enters the main pyglet loop (update). When the main pyglet loop exits,
        the NIA is closed out and the programs exits successfully.
    """
    # open the NIA, or exit with a failure code
    nia = NIA.NIA()
    if not nia.open():
        sys.exit(1)

    # start collecting data
    milliseconds = 50
    nia_data = NIA.NiaData(nia, milliseconds)

    # open a window and schedule continuous updates
    window = pyglet.window.Window(caption="pyNIA")
    pyglet.clock.schedule(update)
    pyglet.app.run()

    # when pyglet exits, close out the NIA and exit gracefully
    nia.close()
    sys.exit(0)
