from numpy import fft, zeros, uint32,int8, array, append,hanning,argmax,vstack,ravel,ones,dstack
import sys
import math
import usb
import threading


class DeviceDescriptor:
    def __init__(self, vendor_id, product_id, interface_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.interface_id = interface_id

    def get_device(self):
        buses = usb.busses()
        for bus in buses:
            for device in bus.devices:
                if device.idVendor == self.vendor_id:
                    if device.idProduct == self.product_id:
                        return device
        return None


class NIA():
    """ Attaches the NIA device, and provides low level data collection"""
    VENDOR_ID    = 0x1234   #: Vendor Id
    PRODUCT_ID   = 0x0000   #: Product Id for the bridged usb cable
    INTERFACE_ID = 0        #: The interface we use to talk to the device
    BULK_IN_EP   = 0x83     #: Endpoint for Bulk reads
    BULK_OUT_EP  = 0x02     #: Endpoint for Bulk writes
    PACKET_LENGTH = 0x40    #: 64 bytes

    device_descriptor = DeviceDescriptor(VENDOR_ID, PRODUCT_ID, INTERFACE_ID)

    def __init__(self):
        # The actual device (PyUSB object)
        self.device = self.device_descriptor.get_device()
        # Handle that is used to communicate with device
        self.handle = None

    def open(self):
        """ Attaches the NIA interface"""
        self.device = self.device_descriptor.get_device()
        if not self.device:
            print >> sys.stderr, "Failed to open NIA device. Cable isn't plugged in"
            return False
        try:
            self.handle = self.device.open()
            # try to detach the interfaces from the kernel, silently ignoring
            # failures if they are already detached
            try:
                self.handle.detachKernelDriver(0)
            except Exception, e:
                pass
            try:
                self.handle.detachKernelDriver(1)
            except Exception, e:
                pass
            self.handle.claimInterface(self.device_descriptor.interface_id)
        except usb.USBError, err:
            print >> sys.stderr, err

        return True

    def close(self):
        """ Release device interface """
        try:
            self.handle.reset()
            self.handle.releaseInterface()
        except Exception, err:
            print >> sys.stderr, err
        self.handle, self.device = None, None

    def bulk_read(self):
        """ Read data off the NIA from its internal buffer of up to 16 samples"""
        read_bytes = self.handle.interruptRead(0x81, 64, 25);
        return read_bytes

class NiaData():
    """ Looks after the collection and processing of NIA data"""
    def __init__(self, nia, milliseconds):
        self.Points = milliseconds/2
        self.Processed_Data = ones(4096, dtype=uint32)
        self.Raw_Data = zeros(10, dtype=uint32)
        self.Fourier_Data = zeros((140, 160), dtype=int8)
        self.AccessDeniedError = False
        self.nia = nia

    def get_data(self):
        """
            This function is called via threading, so that we can plot the
            previous set of data whilst this function collects the new data. It
            sorts out the data into a list of the last second's worth of data
            (~4096 samples)
        """
        Raw_Data = array([])
        try:
            for a in range(self.Points):
                data = self.nia.bulk_read()
                p = int(data[54])
                temp = zeros(p, dtype=uint32)
                for col in range(p):
                    temp[col] = data[col*3+2]*65536 + data[col*3+1]*256 + data[col*3]
                Raw_Data = append(Raw_Data, temp)
        except usb.USBError, err:
            print >> sys.stderr, "Failed to access NIA device: Access Denied"
            print >> sys.stderr, "If you're on GNU/Linux, see README Troubleshooting section for details"
            self.AccessDeniedError = True
        self.Processed_Data = append(self.Processed_Data, Raw_Data)[-4096:-1]

    def waveform(self):
        """
            This function takes a subset of the last second-worth of data,
            filters out frequecies over 30 Hertz, and returns a matrix of pixel
            colors as a string for us to render.
        """
        filter_over = 30
        data = fft.fftn(self.Processed_Data[::8]) #less data points = faster!
        data[filter_over:-filter_over] = 0 # Filter out higher frequencies
        data = fft.ifft(data)
        x_max = max(data)*1.1
        x_min = min(data)*0.9
        data = (140*(data-x_min)/(x_max-x_min)) #normalise with a bit of a window
        wave = ones((140, 410), dtype=int8)
        wave = dstack((wave*0, wave*0, wave*51))
        for i in range(410):
            wave_data_index = data[i+102]
            # throw away NaN values that may occur due to adjusting the NIA
            if not math.isnan(wave_data_index):
                wave[int(wave_data_index), i, :] = [0, 204, 255]
        return wave.tostring()

    def fourier(self, data):
        """
            This function performs a fourier trasform on the last 140 samples
            taken with a Hanning window, and adds the normalised results to an
            array. The highest values are found and used to generate a marker to
            visualize the brain's dominant frequency. The FT is also partitioned
            to represent 6 groups of frequencies, 3 alpha and 3 beta, as defined
            by the waves tuple. These, along with array of fourier data are
            returned to be plotted
        """
        self.Fourier_Data[1:140, :] = self.Fourier_Data[0:139, :]
        x = abs(fft.fftn(data.Processed_Data*hanning(len(data.Processed_Data))))[4:44]
        x_max = max(x)
        x_min = min(x)
        x = (255*(x-x_min)/(x_max-x_min))
        pointer = zeros((160), dtype=int8)
        pointer[(argmax(x))*4:(argmax(x))*4+4]= 255
        y = vstack((x, x, x, x))
        y = ravel(y, 'F')
        self.Fourier_Data[5, :] = y
        self.Fourier_Data[0:4, :] = vstack((pointer, pointer, pointer, pointer))
        fingers = []
        waves = (6, 9, 12, 15, 20, 25, 30)
        for i in range(6):
            finger_sum = sum(x[waves[i]:waves[i+1]])/100
            # throw away NaN values that may occur due to adjusting the NIA
            if not math.isnan(finger_sum):
                fingers.append(finger_sum)
            else:
                fingers.append(0)
        return self.Fourier_Data.tostring(), fingers
