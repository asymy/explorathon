from stopThreadclass import StoppableThread
# from presentation import MyPresentation
import config
from generalfunc import general
import time

gen = general()


class MyHeatPainProgramme(StoppableThread):

    def __init__(self):
        config.buttonState = {
            'HPTRun': False,
            'CDTRun': False,
            'WDTRun': False,
            'initial': True
        }
        StoppableThread.__init__(self)

    def run(self):
        while not self.stopped():
            if config.buttonState['HPTRun']:
                self.HPT()
            elif config.buttonState['WDTRun']:
                self.WDT()
            elif config.buttonState['initial']:
                print('initialising')
                self.inital()
            else:
                time.sleep(0.1)

    def HPT(self):
        print('Hpt')
        config.temperatureCollected = False
        config.defaultVals['stopTemp'] = 50.0
        # for n in range(config.repititions):
        config.startThreshold = True
        while (config.cancelProg is False and config.temperatureCollected is False):
            gen.wait(.1)
        print(config.collectedTemp)
        self.setandcheck(config.defaultVals['startingTemp'])
        config.temperatureCollected = False
        gen.wait(10)
        config.buttonState['HPTRun'] = False

    def CDT(self):
        pass

    def WDT(self):
        pass

    def inital(self):
        print('setting temp')
        self.setandcheck(32.0)
        print('tempset')
        config.buttonState['initial'] = False

    def setandcheck(self, temp):
        if not config.cancelProg:
            config.targetTemp = temp
            config.changeProg = True
            while (config.currentTemp >=
                   (config.targetTemp + config.defaultVals['tolerance']) or
                   config.currentTemp <=
                   (config.targetTemp - config.defaultVals['tolerance'])):
                gen.wait(0.1)
