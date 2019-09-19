import time
import json
import numpy as np
from pathlib import Path
from sklearn.linear_model import LinearRegression
import config
from threading import Thread


class general(Thread):
    def __init__(self):
        Thread.__init__(self)

    def json_read(self, data_folder, fileName):
        DataFile = Path(data_folder / (fileName + '.json'))
        with open(DataFile, 'r') as filehandle:
            data = json.load(filehandle)
        return data

    def json_write(self, data_folder, data, namelist):
        file_to_open = Path(data_folder / (namelist + '.json'))
        with open(file_to_open, 'w') as filehandle:
            json.dump(data, filehandle)

    def wait(self, time_in_s):
        start = time.time()
        endTime = start + time_in_s
        currentTime = time.time()
        while currentTime < endTime and config.cancelProg is False:
            time.sleep(0.1)
            currentTime = time.time()

    def timer(self, startTime, time_in_s):
        endTime = startTime + time_in_s
        currentTime = time.time()
        while currentTime < endTime and config.cancelProg is False:
            time.sleep(0.1)
            currentTime = time.time()

    def num2hex(self, num):
        num = int(num)
        if num < 0:
            num = sum([4095, num])
        return f'{num:03x}'

    def writeandcheck(self, ser, towrite):
        ser.write(str.encode(towrite))
        red = ser.read(4).decode("utf-8")
        if red == towrite:
            pass
        else:
            exit('Error: Value to write = ' + str(towrite) +
                 ', Value read = ' + str(red))

    def set_temp(self, ser, floattemp, floatslope):
        st = self.num2hex(int(floattemp*10))
        slope = self.num2hex(int(floatslope*10))
        self.writeandcheck(ser, 'B' + st)
        self.writeandcheck(ser, 'R' + slope)
        self.writeandcheck(ser, 'C000')

    def set_threshold(self, ser, floatstart, floatstop, floatslope, floatresetslope):
        start = self.num2hex(int(floatstart*10))
        stop = self.num2hex(int(floatstop*10))
        slope = self.num2hex(int(floatslope*10))
        resetslope = self.num2hex(int(floatresetslope*10))
        self.writeandcheck(ser, 'B' + start)
        self.writeandcheck(ser, 'R' + resetslope)
        self.writeandcheck(ser, 'S' + slope)
        self.writeandcheck(ser, 'T' + stop)
        self.writeandcheck(ser, 'C003')
        config.startThreshold = False
