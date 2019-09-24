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
        # plt.xticks(fontsize=14)
        # plt.yticks(fontsize=14)
        plt.setp(self.ax1.get_xticklabels(), fontsize=14)
        plt.setp(self.ax1.get_yticklabels(), fontsize=14)
        plt.setp(self.ax2.get_xticklabels(), fontsize=14)
        plt.setp(self.ax2.get_yticklabels(), fontsize=14)

        self.fig.patch.set_facecolor('snow')
        self.fig.set_size_inches(20, 10)
        self.fig.canvas.set_window_title('Thermode Heat Pain EEG')
        self.ani = FuncAnimation(self.fig, self.run, interval=10, repeat=True)
        self.ax1.axes.set_ylim(19, 51)
        self.ax2.axes.set_ylim(19, 51)
        self.ax1.set_title('Age Differences', fontsize=18)
        self.ax2.set_title('Gender Differences', fontsize=18)
        self.ax1.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax2.axes.set_ylabel('Temperature (°C)', fontsize=16)
        self.ax1.axes.set_xlabel('Age', fontsize=16)
        self.ax2.axes.set_xlabel('Gender', fontsize=16)
        self.ax1.axes.grid()
        self.ax2.axes.grid(axis='y')
        xmin = np.min(self.data['age'])-3
        xmax = np.max(self.data['age'])+3
        self.ax1.axes.set_xlim(xmin, xmax)

        self.aLine, = self.ax1.plot(0, 0, 'go')

        objects = ('Female', 'Male', 'Female', 'Male', 'Female', 'Male')
        y_pos = (0, 1, 2, 3, 4, 5)
        femaleHPT, femaleCDT, femaleWDT = [], [], []
        maleHPT, maleCDT, maleWDT = [], [], []
        for n in range(len(self.data['gender'])):
            if self.data['gender'][n] == 'Female':
                femaleHPT.append(self.data['HPT'][n])
                femaleCDT.append(self.data['CDT'][n])
                femaleWDT.append(self.data['WDT'][n])
            elif self.data['gender'][n] == 'Male':
                maleHPT.append(self.data['HPT'][n])
                maleCDT.append(self.data['CDT'][n])
                maleWDT.append(self.data['WDT'][n])
        x_data = [np.mean(femaleHPT), np.mean(maleHPT), np.mean(
            femaleWDT), np.mean(maleWDT), np.mean(femaleCDT), np.mean(maleCDT)]
        error = [np.std(femaleHPT), np.std(maleHPT), np.std(
            femaleWDT), np.std(maleWDT), np.std(femaleCDT), np.std(maleCDT)]
        barlist = plt.bar(y_pos, x_data, yerr=error,
                          align='center',  ecolor='black', capsize=10)
        plt.xticks(y_pos, objects)
        barlist[0].set_color('mediumpurple')
        barlist[1].set_color('mediumturquoise')
        barlist[2].set_color('mediumpurple')
        barlist[3].set_color('mediumturquoise')
        barlist[4].set_color('mediumpurple')
        barlist[5].set_color('mediumturquoise')

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
            xmax = round(np.max(self.data['HPT']))+2
            self.ax1.axes.set_ylim(32, xmax)
            self.ax2.axes.set_ylim(32, xmax)
            self.ax2.set_xlim(-0.5, 1.5)
            self.aLine.set_color('darkred')
        elif self.graphconfig['threshold'] == 'WDT':
            self.aLine.set_data(self.data['age'], self.data['WDT'])
            xmax = round(np.max(self.data['WDT']))+2
            self.ax1.axes.set_ylim(0, xmax)
            self.ax2.axes.set_ylim(0, xmax)
            self.ax2.set_xlim(1.5, 3.5)
            self.aLine.set_color('crimson')
        elif self.graphconfig['threshold'] == 'CDT':
            self.aLine.set_data(self.data['age'], self.data['CDT'])
            xmin = round(np.max(self.data['CDT']))-2
            self.ax1.axes.set_ylim(xmin, 0)
            self.ax2.axes.set_ylim(xmin, 0)
            self.ax2.set_xlim(3.5, 5.5)
            self.aLine.set_color('navy')

    def titleupdate(self):
        if self.graphconfig['threshold'] == 'HPT':
            self.fig.suptitle('Heat Pain', fontsize=20)
        elif self.graphconfig['threshold'] == 'WDT':
            self.fig.suptitle('Warm Detection', fontsize=20)
        elif self.graphconfig['threshold'] == 'CDT':
            self.fig.suptitle('Cold Detection', fontsize=20)

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
