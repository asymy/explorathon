from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import config


def init():

    def selectThermode(selected):
        config.selectedThermode = selected

    selectThermode('thermode_v5')

    def selectMonitor(selected):
        config.monitor = selected

    selectMonitor('Lonovo')

    def selectGender(selected):
        genderMenuDisplay.set(selected)
        config.gender = selected

    def accept():
        config.participantID = e.get()
        config.participantAge = int(a.get())
        question = 'Would you like to run the programme with these settings?'
        ok = tk.messagebox.askokcancel('Confirm Set Up', question)
        if ok:
            root.destroy()
            import startcollection
            startcollection.run()

    def displayResults():
        from results import ResultsShower
        ResultsShower()

    config.init()
    root = tk.Tk()

    root.geometry('500x400')
    defaultBGColour = 'LightSkyBlue1'
    strongButtonColour = 'RoyalBlue4'
    textColor = 'midnight blue'
    defaultWidth = 13
    root.configure(background=defaultBGColour)
    root.option_add("*Font", "Helvetica, 12")
    # root.wm_iconbitmap('PainScaleicon.ico')
    root.title('Set Up')

    # top label
    topContainer = tk.Frame(root, borderwidth=1, bg=defaultBGColour)
    topContainer.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    instruc = 'Please Enter the Following Details:'
    labelInstruc = tk.Label(topContainer,
                            fg=textColor,
                            text=instruc,
                            bg=defaultBGColour,
                            font='Helvetica, 16')
    labelInstruc.pack(side=tk.BOTTOM, pady=20)

    title = 'Explorathon 2019 Thermal Tester'
    labelTitle = tk.Label(topContainer,
                          fg=textColor,
                          text=title,
                          bg=defaultBGColour,
                          font='Helvetica 18 bold')
    labelTitle.pack(side=tk.BOTTOM)

    # Patrticipant ID Info

    participantContainer = tk.Frame(root, bg=defaultBGColour)
    participantContainer.pack(side=tk.TOP, expand=True)

    labelParticipantID = tk.Label(participantContainer,
                                  justify=tk.RIGHT,
                                  fg=textColor,
                                  text='Participant ID:',
                                  bg=defaultBGColour,
                                  width=defaultWidth)
    labelParticipantID.pack(side=tk.LEFT)
    e = tk.Entry(participantContainer, width=defaultWidth)
    e.pack(side=tk.RIGHT)
    e.focus_set()

    # Participant Age

    ageContainer = tk.Frame(root, bg=defaultBGColour)
    ageContainer.pack(side=tk.TOP, expand=True)

    labelAge = tk.Label(ageContainer,
                        justify=tk.RIGHT,
                        fg=textColor,
                        text='Age:',
                        bg=defaultBGColour,
                        width=defaultWidth)
    labelAge.pack(side=tk.LEFT)
    a = tk.Entry(ageContainer, width=defaultWidth)
    a.pack(side=tk.RIGHT)

    # Participant Gender

    genderContainer = tk.Frame(root, bg=defaultBGColour)
    genderContainer.pack(side=tk.TOP, expand=True)

    genderLabel = tk.Label(genderContainer,
                           fg=textColor,
                           justify=tk.RIGHT,
                           text='Gender:',
                           bg=defaultBGColour,
                           width=defaultWidth)
    genderLabel.pack(side=tk.LEFT)

    genderMenuDisplay = tk.StringVar()
    genderMenuDisplay.set('select')
    genderMenu = tk.Menubutton(genderContainer,
                               textvariable=genderMenuDisplay,
                               width=defaultWidth)

    picks = tk.Menu(genderMenu)
    genderMenu.config(menu=picks)

    picks.add_command(
        label='Female', command=lambda name='Female': selectGender('Female'))
    picks.add_command(
        label='Male', command=lambda name='Male': selectGender('Male'))

    genderMenu.config(bg=strongButtonColour,
                      fg='white',
                      font='helvetica 12 bold',
                      bd=4,
                      relief=tk.RAISED)
    genderMenu.pack(side=tk.RIGHT, expand=True)

    # Bottom buttons

    bottomContainer = tk.Frame(root, bg=defaultBGColour)
    bottomContainer.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    # Accept Button

    acceptButton = tk.Button(bottomContainer,
                             text="Accept",
                             bg=strongButtonColour,
                             fg='white',
                             font='helvetica 12 bold',
                             width=defaultWidth,
                             command=accept)
    acceptButton.pack(side=tk.RIGHT, padx=20, pady=5)

    # Results Button

    acceptButton = tk.Button(bottomContainer,
                             text="Results",
                             bg=strongButtonColour,
                             fg='white',
                             font='helvetica 12 bold',
                             width=defaultWidth,
                             command=displayResults)
    acceptButton.pack(side=tk.LEFT, padx=20, pady=5)

    tk.mainloop()
