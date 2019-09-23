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
    monitor = 'Lonovo'
    gender = ''
    program = ''
    selectedMonitor = ''
    participantID = ''

    global defaultVals
    defaultVals = {
        'slope': 1,
        'returnSlope': 3,
        'startingTemp': 32,
        'tolerance': 1
    }

    global cancelProg, startThreshold
    cancelProg = False
    startThreshold = False

    global currentTemp, targetTemp, changeProg, slope, collectedTemp, temperatureCollected
    currentTemp = 0.0
    changeProg = True
    targetTemp = 32.0
    slope = 1
    collectedTemp = 0
    temperatureCollected = False

    global buttonState
    buttonState = {
        'HPTRun': False,
        'CDTRun': False,
        'WDTRun': False,
    }

    global repititions
    repititions = 3

    global buttonColour, buttonArray
    buttonColour = {
        'preClick': ['mediumorchid', 'plum'],
        'postClick': ['darkgray', 'darkgray'],
        'postRun': ['thistle', 'thistle'],
    }
    buttonArray = {}

    global progStatus
    progStatus = {
        'name': '',
        'prevTemp': 0.0,
        'nextTemp': 0.0,
        'timeLeft': 0.0,
    }


def json_read(data_folder, fileName):
    DataFile = Path(data_folder / (fileName + '.json'))
    with open(DataFile, 'r') as filehandle:
        data = json.load(filehandle)
    return data
