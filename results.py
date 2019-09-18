import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from psychopy import visual, core, monitors, event
import time


def createButton(pos, text, function):
    axB = plt.axes(pos)
    button = Button(axB, text)
    button.label.set_fontsize(14)
    button.on_clicked(function)
    # button.color = config.buttonColour['preClick'][0]
    # button.hovercolor = config.buttonColour['preClick'][1]
    return button


class ResultsShower():
    def __init__(self):

        self.graphconfig = {
            'type': 'gender',
            'threshold': 'HPT'
        }
        # self._dataClass = dataClass
        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(right=0.85)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        self.titleupdate()
        self.fig.patch.set_facecolor('snow')
        self.fig.set_size_inches(20, 10)
        self.fig.canvas.set_window_title('Thermode Heat Pain EEG')
        self.ani = FuncAnimation(self.fig, self.run, interval=10, repeat=True)
        self.ax.axes.set_ylim(19, 51)
        self.ax.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax.axes.set_xlabel('Time (s)', fontsize=16)
        self.ax.axes.grid()

        a, b, c, d = 0.88, 0.1, 0.1, 0.06
        self.buttonClose = createButton(
            [a, b, c, d], 'Close', self.MyCloseResults)

        a, b, c, d = 0.93, 0.8, 0.05, 0.06
        self.buttonPlus = createButton([a, b, c, d], '>', self.MyNavPlus)
        a, b, c, d = 0.88, 0.8, 0.05, 0.06
        self.buttonMinus = createButton([a, b, c, d], '<', self.MyNavMinus)

        a, b, c, d = 0.88, 0.5, 0.1, 0.06
        self.buttonPlotToggle = createButton(
            [a, b, c, d], 'Plot Toggle', self.MyPlotToggle)

        plt.show()

    def titleupdate(self):
        titlestr = self.graphconfig['type'] + ' ' + self.graphconfig['threshold']
        self.ax.set_title(titlestr, fontsize=20)

    def MyCloseResults(self, event):
        plt.close()

    def MyNavPlus(self, event):
        if self.graphconfig['threshold'] == 'HPT':
            self.graphconfig['threshold'] = 'WDT'
        elif self.graphconfig['threshold'] == 'WDT':
            self.graphconfig['threshold'] = 'CDT'
        else:
            self.graphconfig['threshold'] = 'HPT'
        self.titleupdate()

    def MyNavMinus(self, event):
        if self.graphconfig['threshold'] == 'HPT':
            self.graphconfig['threshold'] = 'CDT'
        elif self.graphconfig['threshold'] == 'WDT':
            self.graphconfig['threshold'] = 'HPT'
        else:
            self.graphconfig['threshold'] = 'HPT'
        self.titleupdate()

    def MyPlotToggle(self, event):
        if self.graphconfig['type'] == 'gender':
            self.graphconfig['type'] = 'age'
        else:
            self.graphconfig['type'] = 'gender'
        self.titleupdate()

    def run(self, i):
        pass

