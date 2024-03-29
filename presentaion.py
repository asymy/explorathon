
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from psychopy import visual, core, monitors, event
import numpy as np
import webbrowser
import datetime
import threading

import config
from generalfunc import general

gen = general()


def write_to_axes(ax, txt, pos):
    return ax.text(pos[0], pos[1], txt,
                   horizontalalignment='left',
                   verticalalignment='center',
                   transform=ax.transAxes,
                   fontsize=18)


def create_info_box(ax, pos):
    boxInfo = dict(
        facecolor='snow',
        edgecolor='black',
        boxstyle='round,pad=0.3')
    return ax.text(pos[0], pos[1], '',
                   horizontalalignment='center',
                   verticalalignment='bottom',
                   transform=ax.transAxes,
                   fontsize=18,
                   bbox=boxInfo)


class MyPresentation():

    def __init__(self, dataClass):
        # GRAPH
        self._dataClass = dataClass
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(left=0.2, bottom=0.23)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.title('Temperature of Thermode', fontsize=20)
        self.fig.patch.set_facecolor('snow')
        self.fig.set_size_inches(20, 10)
        self.fig.canvas.set_window_title('Thermode Heat Pain EEG')
        self.hLine, = plt.plot(0, 0, 'g')
        self.hLine.set_color('b')
        self.ani = FuncAnimation(self.fig, self.run, interval=10, repeat=True)
        self.ax.axes.set_ylim(14, 51)
        self.ax.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax.axes.set_xlabel('Time (s)', fontsize=16)
        self.ax.axes.grid()

        # Buttons
        def createButton(pos, text, function):
            axB = plt.axes(pos)
            button = Button(axB, text)
            button.label.set_fontsize(14)
            button.on_clicked(function)
            button.color = config.buttonColour['preClick'][0]
            button.hovercolor = config.buttonColour['preClick'][1]
            return button

        delta = 0.08
        a, b, c, d = 0.02, 0.1, 0.1, 0.06
        config.buttonArray['Cancel'] = createButton(
            [a, b, c, d], 'Cancel', self.MyCancel)
        config.buttonArray['Cancel'].color = 'orangered'
        config.buttonArray['Cancel'].hovercolor = 'lightsalmon'
        b = b+delta+0.07
        config.buttonArray['HPT'] = createButton(
            [a, b, c, d], 'HPT', self.MyHPT)
        b = b+delta
        config.buttonArray['WDT'] = createButton(
            [a, b, c, d], 'WDT', self.MyWDT)
        b = b+delta
        config.buttonArray['CDT'] = createButton(
            [a, b, c, d], 'CDT', self.MyCDT)
        b = b+delta
        config.buttonArray['test'] = createButton(
            [a, b, c, d], 'test', self.MyTest)
        a, b, c = 0.93, 0.91, 0.05
        config.buttonArray['Quit'] = createButton(
            [a, b, c, d], 'Quit', self.MyQuit)
        config.buttonArray['Quit'].color = 'orangered'
        config.buttonArray['Quit'].hovercolor = 'lightsalmon'
        a = a-0.06
        config.buttonArray['About'] = createButton(
            [a, b, c, d], 'About', self.AboutMe)
        config.buttonArray['About'].color = 'mediumturquoise'
        config.buttonArray['About'].hovercolor = 'paleturquoise'

        tax = plt.axes([0.2, 0.02, 0.7, 0.13], facecolor='floralwhite')
        tax.get_xaxis().set_visible(False)
        tax.get_yaxis().set_visible(False)

        x1, x2, x3 = 0.02, 0.43, 0.73
        y1, y2 = 0.73, 0.35
        txt = 'Programme Running:'
        write_to_axes(tax, txt, [x1, y1])

        txt = 'Current Temperature:'
        write_to_axes(tax, txt, [x1, y2])

        txt = 'Cold Detection:'
        write_to_axes(tax, txt, [x2, y1])

        txt = 'Cold Pain:'
        write_to_axes(tax, txt, [x2, y2])

        txt = 'Warm Detection:'
        write_to_axes(tax, txt, [x3, y1])

        txt = 'Heat Pain:'
        write_to_axes(tax, txt, [x3, y2])

        x1, x2, x3 = 0.31, 0.63, 0.93
        y1, y2 = 0.65, 0.25
        self.infoCurrentProgramme = create_info_box(tax, [x1, y1])
        self.infoCurrentProgramme.set_text('None')
        self.infoCurrentTemp = create_info_box(tax, [x1, y2])
        self.infoCDT = create_info_box(tax, [x2, y1])
        self.infoCPT = create_info_box(tax, [x2, y2])
        self.infoWDT = create_info_box(tax, [x3, y1])
        self.infoHPT = create_info_box(tax, [x3, y2])

        # PSYCHOPY
        # self.mon = monitors.Monitor(name=config.monitor)
        # self.win = visual.Window(fullscr=True,
        #                          size=self.mon.getSizePix(),
        #                          screen=1,
        #                          monitor=self.mon)
        # self.mes = visual.TextStim(self.win, text='')
        # # self.mes.setSize(12)
        # self.mes.height = .05
        # self.mes.setAutoDraw(True)  # automatically draw every frame
        # self.win.flip()
        # config.text = ''
        # self.fixation = visual.ShapeStim(self.win,
        #                                  units='cm',
        #                                  vertices=((0, -.75),
        #                                            (0,  .75),
        #                                            (0,    0),
        #                                            (-.75,    0),
        #                                            (.75,    0)),
        #                                  lineWidth=4,
        #                                  closeShape=False,
        #                                  lineColor="white")
        # self.myRatingScale = visual.RatingScale(
        #     self.win, low=0, high=20,
        #     marker='triangle', stretch=1.5,
        #     tickHeight=1.2, precision=1,
        #     tickMarks=(0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20),
        #     labels=['0', '1', '2', '3', '4',
        #             '5', '6', '7', '8', '9', '10'],
        #     scale=('0 = No Pain, 10 = Worst Pain Imaginable'),
        #     acceptText='Accept',
        #     maxTime=20, showValue=False)
        # self.Question = visual.TextStim(
        #     self.win,
        #     units='norm',
        #     pos=[0, 0.4],
        #     text=('What was the maximum pain '
        #           'intensity during the last period?'))
        # PRpicture = 'PainScale2.png'
        # self.ScalePic = visual.ImageStim(self.win, image=PRpicture,
        #                                  units='cm', pos=[0, 0])

    def run(self, i):
        # print(config.text)
        # GRAPH
        self.hLine.set_data(self._dataClass.XData, self._dataClass.YData)
        self.hLine.axes.set_xlim(
            np.max(self._dataClass.XData)-60, np.max(self._dataClass.XData))
        self.infoCurrentTemp.set_text(
            str(config.currentTemp) + '°C')
        changeDisp = False
        for x in config.buttonState:
            if config.buttonState[x]:
                changeDisp = True
        if changeDisp:
            self.infoCurrentProgramme.set_text(config.progStatus['name'])
        else:
            self.infoCurrentProgramme.set_text('None')
        self.infoCDT.set_text(
            (str(config.results['CDT']) + '°C'))
        self.infoWDT.set_text(
            (str(config.results['WDT']) + '°C'))
        self.infoHPT.set_text(
            (str(config.results['HPT']) + '°C'))
        self.infoCPT.set_text(
            (str(config.results['CPT']) + '°C'))

        # PSYCHOPY
        # if config.text == '+':
        #     self.mes.setText('')
        #     self.fixation.draw()

    def MyWDT(self, event):
        config.buttonArray['WDT'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['WDT'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['WDTRun'] = True

    def MyHPT(self, event):
        config.buttonArray['HPT'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['HPT'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['HPTRun'] = True

    def MyCDT(self, event):
        config.buttonArray['CDT'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['CDT'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['CDTRun'] = True

    def MyTest(self, event):
        config.buttonArray['test'].color = (
            config.buttonColour['postClick'][0])
        config.buttonArray['test'].hovercolor = (
            config.buttonColour['postClick'][1])
        config.buttonState['testRun'] = True

    def AboutMe(self, event):
        webbrowser.open("aboutme.txt")

    def MyCancel(self, event):
        config.cancelProg = True

    def MyQuit(self, event):
        print('Quit Button Pressed')
        config.cancelProg = True
        for thread in threading.enumerate():
            if thread.name is not 'MainThread':
                thread.stop()
                print(thread.name)
        plt.close()
        tempdic = config.results
        tempdic['age'] = config.participantAge
        tempdic['gender'] = config.participantGender
        tempdic['ID'] = config.participantID
        newdata = tempdic
        self.savedata(newdata)
        import main
        main.run()

    def savedata(self, newdata):
        import json
        with open('data.json') as f:
            data = json.load(f)
        data['age'].append(newdata['age'])
        data['gender'].append(newdata['gender'])
        data['HPT'].append(newdata['HPT'])
        data['CDT'].append(newdata['CDT'])
        data['WDT'].append(newdata['WDT'])
        data['ID'].append(newdata['ID'])
        with open('data.json', 'w') as f:
            json.dump(data, f)
