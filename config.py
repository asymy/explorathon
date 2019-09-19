from pathlib import Path
import json
import sys


def init():
    global thermodeInfo, monitorInfo, selectedMonitor
    global thermode, monitor
    global gender, program
    global participantID
    thermodeInfo = {
        "name": "thermode_v5",
        "OffSetTemp_DA": 366,
        "ScaleFactorTemp_DA": 45.8,
        "OffSetSlope_DA": -48,
        "ScaleFactorSlope_DA": 437,
        "OffSetTemp_AD": 27,
        "ScaleFactorTemp_AD": 69.1
    }
    monitorInfo = json_read(Path('CalibrationFiles'), 'monitorinfo')
    thermode = ''
    monitor = ''
    gender = ''
    program = ''
    selectedMonitor = ''
    participantID = ''

    global defaultVals
    defaultVals = {
        'slope': 1,
        'returnSlope': 3,
        'startingTemp': 32,
        'tolerance': 2
    }

    global cancelProg
    cancelProg = False

    global currentTemp, targetTemp, changeProg, slope
    currentTemp = 0.0
    changeProg = True
    targetTemp = 32.0
    slope = 1


def json_read(data_folder, fileName):
    DataFile = Path(data_folder / (fileName + '.json'))
    with open(DataFile, 'r') as filehandle:
        data = json.load(filehandle)
    return data
