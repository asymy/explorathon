
import numpy as np
import time
import serial
import sys

# Personal
from generalfunc import general
from stopThreadclass import StoppableThread
from generalfunc import general
import config

gen = general()


class MyDataFetcher(StoppableThread):

    def __init__(self, dataClass):

        StoppableThread.__init__(self)

        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = 'COM4'
        self.ser.parity = 'N'
        self.ser.bytesize = 8
        self.ser.stopbits = 1
        self.ser.xonxoff = True
        self.ser.timeout = 5
        self.ser.open()

        Thermode = config.thermodeInfo

        offset0 = 'G' + gen.num2hex(float(Thermode['OffSetTemp_DA']))
        gain0 = 'H' + gen.num2hex(float(Thermode['ScaleFactorTemp_DA'])*10)
        offset1 = 'O' + gen.num2hex(float(Thermode['OffSetSlope_DA']))
        gain1 = 'N' + gen.num2hex(float(Thermode['ScaleFactorSlope_DA']))
        offsetC = 'K' + gen.num2hex(float(Thermode['OffSetTemp_AD']))
        gainC = 'L' + gen.num2hex(float(Thermode['ScaleFactorTemp_AD'])*10)
        s = self.ser.read(8).decode("utf-8")

        if s == 'INF01.03':
            gen.writeandcheck(self.ser, offset0)
            gen.writeandcheck(self.ser, offset1)
            gen.writeandcheck(self.ser, offsetC)
            gen.writeandcheck(self.ser, gain0)
            gen.writeandcheck(self.ser, gain1)
            gen.writeandcheck(self.ser, gainC)
            self._dataClass = dataClass
            self._period = 1/10
            self._nextCall = time.time()
        else:
            print('Thermode Not Sending Data')
            self.ser.close()
            sys.exit()

        config.startTime = time.time()
        self.poll_temp()
        self._dataClass.YData[0] = config.currentTemp

    def poll_temp(self):
        self.ser.write(str.encode('M000'))
        red = self.ser.read(4).decode("utf-8")
        if red[0] == 'P':
            config.collectedTemp = int(red[1:], 16)/10
            config.temperatureCollected = True
        elif red[0] == 'F':
            config.collectedTemp = int(red[1:], 16)/10
            config.temperatureCollected = True
        else:
            config.currentTemp = int(red[1:], 16)/10

    def run(self):
        while not self.stopped():
            callTime = time.time()
            self.poll_temp()
            # add data to data class
            if config.changeProg:
                gen.set_temp(self.ser, config.targetTemp, config.slope)
                config.changeProg = False
            if config.startThreshold:
                config.startThreshold = False
                gen.set_threshold(
                    self.ser,
                    config.defaultVals['startingTemp'],
                    config.defaultVals['stopTemp'],
                    config.defaultVals['slope'],
                    config.defaultVals['returnSlope']
                )
            self._dataClass.XData.append(time.time()-config.startTime)
            self._dataClass.YData.append(config.currentTemp)
            # sleep until next execution
            sleepTime = self._period-(callTime - time.time())
            time.sleep(sleepTime)
