
import numpy as np
import time

# Personal
from generalfunc import general
from CalibrationPlot import CalibratedPlot_Participant
from stopThreadclass import StoppableThread
import config

class MyHeatPainProgramme(StoppableThread):

    def __init__(self):

        StoppableThread.__init__(self)

        startingVals = gen.json_read(
            config.folders['calibration'], 'startingdata')
        config.defaultVals = startingVals
        config.targetTemp = config.defaultVals['baselineTemperature']
        config.changeProg = True

        self.allRatings = []
        self.EEG = False


    def setandcheck(self, temp):
        if not config.cancelProg:
            config.targetTemp = temp
            config.changeProg = True
            while (config.currentTemp >=
                    (config.targetTemp + config.defaultVals['tolerance']) or
                    config.currentTemp <=
                    (config.targetTemp - config.defaultVals['tolerance'])):
                gen.wait(0.1)