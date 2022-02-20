import sys
import googletrans

if __name__ != "__main__":
    sys.exit()

# Only gets executes when program is main
from winMain import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import SpeechToText as STT
import JsonParser

# Variables for the UI Elements and the App Itself
app = QtWidgets.QApplication(sys.argv)
ui = Ui_Form()
parser = JsonParser.Parser()


# Sets all ui Element states and starts Run in STT
def Run():
    # Main Window
    ui.btnRun.setEnabled(False)
    ui.btnStop.setEnabled(True)

    # Settings
    ui.btnSave.setEnabled(False)
    ui.btnLoad.setEnabled(False)
    ui.comBoxLanguage.setEnabled(False)
    ui.comBoxTranslation.setEnabled(False)
    ui.chBoxTranslation.setEnabled(False)
    ui.spBoxRecording.setEnabled(False)
    ui.spBoxSleepTime.setEnabled(False)
    ui.keySequenceRecord.setEnabled(False)
    ui.keySequenceOpenChat.setEnabled(False)
    ui.keySqeuenceCloseChat.setEnabled(False)

    # Setup of the Recognition
    STT.Setup(ui.spBoxRecording.property("value"), ui.spBoxSleepTime.property("value"), ui.comBoxLanguage.currentText(), ui.comBoxTranslation.currentText(),
              ui.lwDisplay, ui.keySequenceRecord.keySequence().toString(),
              ui.keySequenceOpenChat.keySequence().toString(), ui.keySqeuenceCloseChat.keySequence().toString())


# Sets all ui Element states and starts Stop in STT
def Stop():
    # Main Window
    ui.lwDisplay.clear()
    ui.btnRun.setEnabled(True)
    ui.btnStop.setEnabled(False)

    # Settings
    ui.btnSave.setEnabled(True)
    ui.btnLoad.setEnabled(True)
    ui.comBoxLanguage.setEnabled(True)
    ui.chBoxTranslation.setEnabled(True)
    ui.comBoxTranslation.setEnabled(ui.chBoxTranslation.isChecked())
    ui.spBoxRecording.setEnabled(True)
    ui.spBoxSleepTime.setEnabled(True)
    ui.keySqeuenceCloseChat.setEnabled(True)
    ui.keySequenceRecord.setEnabled(True)
    ui.keySequenceOpenChat.setEnabled(True)

    # Stoping the Recognition
    STT.Stop()


def Translation():
    ui.comBoxTranslation.setEnabled(not ui.comBoxTranslation.isEnabled())
    if not ui.comBoxTranslation.isEnabled():
        ui.comBoxTranslation.setCurrentIndex(0)
    else:
        ui.comBoxTranslation.setCurrentIndex(ui.comBoxTranslation.findText("english"))


# Connects the UI Element Events to Functions
def connectUiElements():
    ui.btnExit.clicked.connect(sys.exit)
    ui.btnRun.clicked.connect(Run)
    ui.btnStop.clicked.connect(Stop)
    ui.chBoxTranslation.clicked.connect(Translation)
    ui.btnSave.clicked.connect(lambda: parser.Parse(ui.spBoxRecording.property("value"), ui.spBoxSleepTime.property("value"),
                                                   ui.comBoxLanguage.currentText(), ui.comBoxTranslation.currentText(),
                                                   ui.keySequenceRecord.keySequence().toString(),
                                                   ui.keySequenceOpenChat.keySequence().toString(),
                                                   ui.keySqeuenceCloseChat.keySequence().toString()))
    ui.btnLoad.clicked.connect(lambda: parser.Load(ui.spBoxRecording, ui.spBoxSleepTime, ui.comBoxLanguage,
                                                   ui.comBoxTranslation, ui.keySequenceRecord, ui.keySequenceOpenChat,
                                                   ui.keySqeuenceCloseChat))


# Sets all the Combo Box Languages and standard values
def SetComboBoxes():
    langcodes = googletrans.LANGCODES.keys()

    ui.comBoxTranslation.addItem("None")
    ui.comBoxTranslation.addItems(langcodes)
    ui.comBoxTranslation.setCurrentIndex(0)

    ui.comBoxLanguage.addItems(langcodes)
    ui.comBoxLanguage.setCurrentIndex(ui.comBoxLanguage.findText("english"))


def Main():
    ui.Form.show()
    SetComboBoxes()
    connectUiElements()


Main()
sys.exit(app.exec_())
