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
        self.bLine, = self.ax1.plot(0, 0, 'b*', markersize=22)

        objects = ('Female', 'Male', 'Female', 'Male', 'Female', 'Male')
        y_pos = (0, 1, 2, 3, 4, 5)
        femaleHPT, femaleCDT, femaleWDT = [], [], []
        maleHPT, maleCDT, maleWDT = [], [], []
        for n in range(len(self.data['gender'])):
            if self.data['gender'][n] == 'Female':
                if self.data['HPT'][n]:
                    femaleHPT.append(self.data['HPT'][n])
                if self.data['CDT'][n]:
                    femaleCDT.append(self.data['CDT'][n])
                if self.data['WDT'][n]:
                    femaleWDT.append(self.data['WDT'][n])
            elif self.data['gender'][n] == 'Male':
                if self.data['HPT'][n]:
                    maleHPT.append(self.data['HPT'][n])
                if self.data['CDT'][n]:
                    maleCDT.append(self.data['CDT'][n])
                if self.data['WDT'][n]:
                    maleWDT.append(self.data['WDT'][n])
        x_data = [np.nanmean(femaleHPT), np.nanmean(maleHPT), np.nanmean(
            femaleWDT), np.nanmean(maleWDT), np.nanmean(femaleCDT), np.nanmean(maleCDT)]
        error = [np.nanstd(femaleHPT), np.nanstd(maleHPT), np.nanstd(
            femaleWDT), np.nanstd(maleWDT), np.nanstd(femaleCDT), np.nanstd(maleCDT)]
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
        xdata, ydata = [], []
        if self.graphconfig['threshold'] == 'HPT':
            for n in range(len(self.data['HPT'])):
                if self.data['HPT'][n]:
                    xdata.append(self.data['HPT'][n])
                    ydata.append(self.data['age'][n])
            xmax = round(np.max(xdata))+2
            xmin = 32
            self.ax2.set_xlim(-0.5, 1.5)
            self.aLine.set_color('darkred')
            self.bLine.set_color('magenta')

        elif self.graphconfig['threshold'] == 'WDT':
            for n in range(len(self.data['WDT'])):
                if self.data['WDT'][n]:
                    xdata.append(self.data['WDT'][n])
                    ydata.append(self.data['age'][n])
            xmax = round(np.max(xdata))+2
            xmin = 0
            self.ax2.set_xlim(1.5, 3.5)
            self.aLine.set_color('crimson')
            self.bLine.set_color('magenta')

        elif self.graphconfig['threshold'] == 'CDT':
            for n in range(len(self.data['CDT'])):
                if self.data['HPT'][n]:
                    xdata.append(self.data['CDT'][n])
                    ydata.append(self.data['age'][n])
            xmax = 0
            xmin = round(np.min(xdata))-2
            self.ax2.set_xlim(3.5, 5.5)
            self.aLine.set_color('navy')
            self.bLine.set_color('magenta')

        self.aLine.set_data(ydata, xdata)
        self.bLine.set_data(ydata[-1], xdata[-1])
        self.ax1.axes.set_ylim(xmin, xmax)
        self.ax2.axes.set_ylim(xmin, xmax)

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
