from stopThreadclass import StoppableThread
# from presentation import MyPresentation
import config
from generalfunc import general
import time
import random

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
            elif config.buttonState['CDTRun']:
                self.CDT()
            elif config.buttonState['initial']:
                print('initialising')
                self.inital()
            else:
                time.sleep(0.1)

    def HPT(self):
        print('HPT')
        config.progStatus['name'] = 'HPT'
        config.defaultVals['stopTemp'] = 50.0
        result = self.commonThreshold()
        config.results['HPT'] = result
        config.buttonState['HPTRun'] = False
        config.progStatus['name'] = ''
        config.cancelProg = False

    def CDT(self):
        print('CDT')
        config.progStatus['name'] = 'CDT'
        config.defaultVals['stopTemp'] = 15.0
        result = self.commonThreshold()
        config.results['CDT'] = result
        config.progStatus['name'] = ''
        config.buttonState['CDTRun'] = False
        config.cancelProg = False

    def WDT(self):
        print('WDT')
        config.progStatus['name'] = 'WDT'
        config.defaultVals['stopTemp'] = 40.0
        result = self.commonThreshold()
        config.results['WDT'] = result
        config.buttonState['WDTRun'] = False
        config.progStatus['name'] = ''
        config.cancelProg = False

    def commonThreshold(self):
        gen.wait(random.randint(1, 2))
        results = [0, 0, 0]
        for n in range(config.repititions):
            self.setandcheck(config.defaultVals['startingTemp'])
            gen.wait(random.randint(5, 7))
            if config.cancelProg is False:
                config.temperatureCollected = False
                config.startThreshold = True
                while (config.cancelProg is False and config.temperatureCollected is False):
                    gen.wait(1)
                results[n] = config.collectedTemp
                config.targetTemp = config.defaultVals['startingTemp']
                self.andcheck()
        result = round(sum(results)*10/config.repititions)/10
        return result

    def inital(self):
        print('setting temp')
        self.setandcheck(32.0)
        print('tempset')
        config.buttonState['initial'] = False

    def setandcheck(self, temp):
        if not config.cancelProg:
            config.targetTemp = temp
            config.changeProg = True
            self.andcheck()

    def andcheck(self):
        while (config.currentTemp >=
               (config.targetTemp + config.defaultVals['tolerance']) or
               config.currentTemp <=
               (config.targetTemp - config.defaultVals['tolerance'])):
            gen.wait(0.1)
