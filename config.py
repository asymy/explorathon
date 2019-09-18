from pathlib import Path
import json
import sys


def init():
    global thermodeInfo, monitorInfo, selectedThermode, selectedMonitor
    global thermode, monitor
    global gender, program
    global participantID
    thermodeInfo = json_read(Path('CalibrationFiles'), 'thermodeinfo')
    monitorInfo = json_read(Path('CalibrationFiles'), 'monitorinfo')
    thermode = ''
    monitor = ''
    gender = ''
    program = ''
    selectedMonitor = ''
    selectedThermode = ''
    participantID = ''

    global defaultVals
    defaultVals = {
        'slope': 1,
        'returnSlope': 3,
        'startingTemp': 32
    }

    global cancelProg
    cancelProg = False

    global currentTemp, targetTemp, changeProg
    currentTemp = 0.0
    changeProg = True
    targetTemp = 32.0


def json_read(data_folder, fileName):
    DataFile = Path(data_folder / (fileName + '.json'))
    with open(DataFile, 'r') as filehandle:
        data = json.load(filehandle)
    return data
