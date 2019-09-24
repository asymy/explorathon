import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.animation import FuncAnimation
from psychopy import visual, core, monitors, event
import time
import json


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

        with open('data.json') as f:
            self.data = json.load(f)

        self.graphconfig = {
            'threshold': 'HPT'
        }

        self.fig, (self.ax1, self.ax2) = plt.subplots(nrows=1, ncols=2)
        plt.subplots_adjust(right=0.85)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)

        self.fig.patch.set_facecolor('snow')
        self.fig.set_size_inches(20, 10)
        self.fig.canvas.set_window_title('Thermode Heat Pain EEG')
        self.ani = FuncAnimation(self.fig, self.run, interval=10, repeat=True)
        self.ax1.axes.set_ylim(19, 51)
        self.ax2.axes.set_ylim(19, 51)
        self.ax1.set_title('Age Differences')
        self.ax1.set_title('Gender Differences')
        self.ax1.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax2.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax1.axes.set_xlabel('Age', fontsize=16)
        self.ax2.axes.set_xlabel('Gender', fontsize=16)
        self.ax1.axes.grid()
        self.ax2.axes.grid(axis='y')
        self.ax1.axes.set_xlim(0, 50)

        self.aLine, = self.ax1.plot(0, 0, 'go')

        objects = ('Female', 'Male', 'Female', 'Male', 'Female', 'Male')
        y_pos = (0, 1, 2, 3, 4, 5)
        femaleHPT, femaleCDT, femaleWDT = [], [], []
        maleHPT, maleCDT, maleWDT = [], [], []
        for n in range(len(self.data['gender'])):
            if self.data['gender'][n] == 'female':
                femaleHPT.append(self.data['HPT'][n])
                femaleCDT.append(self.data['CDT'][n])
                femaleWDT.append(self.data['WDT'][n])
            else:
                maleHPT.append(self.data['HPT'][n])
                maleCDT.append(self.data['CDT'][n])
                maleWDT.append(self.data['WDT'][n])
        x_data = [np.mean(femaleHPT), np.mean(maleHPT), np.mean(
            femaleWDT), np.mean(maleWDT), np.mean(femaleCDT), np.mean(maleCDT)]
        error = [np.std(femaleHPT), np.std(maleHPT), np.std(
            femaleWDT), np.std(maleWDT), np.std(femaleCDT), np.std(maleCDT)]
        plt.bar(y_pos, x_data, yerr=error,
                align='center', alpha=0.5,  ecolor='black', capsize=10)
        plt.xticks(y_pos, objects)
        self.ax2.set_xlim(-0.5, 1.5)

        self.graphupdate()

        a, b, c, d = 0.88, 0.1, 0.1, 0.06
        self.buttonClose = createButton(
            [a, b, c, d], 'Close', self.MyCloseResults)

        a, b, c, d = 0.93, 0.8, 0.05, 0.06
        self.buttonPlus = createButton([a, b, c, d], '>', self.MyNavPlus)
        a, b, c, d = 0.88, 0.8, 0.05, 0.06
        self.buttonMinus = createButton([a, b, c, d], '<', self.MyNavMinus)

        plt.show()

    def graphupdate(self):
        self.titleupdate()
        if self.graphconfig['threshold'] == 'HPT':
            self.aLine.set_data(self.data['age'], self.data['HPT'])
            self.ax1.axes.set_ylim(30, 51)
            self.ax2.axes.set_ylim(30, 51)
            self.ax2.set_xlim(-0.5, 1.5)
        elif self.graphconfig['threshold'] == 'WDT':
            self.aLine.set_data(self.data['age'], self.data['WDT'])
            self.ax1.axes.set_ylim(30, 40)
            self.ax2.axes.set_ylim(30, 40)
            self.ax2.set_xlim(1.5, 3.5)
        elif self.graphconfig['threshold'] == 'CDT':
            self.aLine.set_data(self.data['age'], self.data['CDT'])
            self.ax1.axes.set_ylim(20, 34)
            self.ax2.axes.set_ylim(20, 34)
            self.ax2.set_xlim(3.5, 5.5)

    def titleupdate(self):
        titlestr = self.graphconfig['threshold']
        self.fig.suptitle(titlestr, fontsize=20)

    def MyCloseResults(self, event):
        plt.close()

    def MyNavPlus(self, event):
        if self.graphconfig['threshold'] == 'HPT':
            self.graphconfig['threshold'] = 'WDT'
        elif self.graphconfig['threshold'] == 'WDT':
            self.graphconfig['threshold'] = 'CDT'
        else:
            self.graphconfig['threshold'] = 'HPT'
        self.graphupdate()

    def MyNavMinus(self, event):
        if self.graphconfig['threshold'] == 'HPT':
            self.graphconfig['threshold'] = 'CDT'
        elif self.graphconfig['threshold'] == 'WDT':
            self.graphconfig['threshold'] = 'HPT'
        else:
            self.graphconfig['threshold'] = 'HPT'
        self.graphupdate()

    def run(self, i):
        pass


if __name__ == "__main__":
    ResultsShower()
