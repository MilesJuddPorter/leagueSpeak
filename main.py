import sys
import googletrans

if __name__ != "__main__":
    sys.exit()

# Only gets executes when program is main
from winMain import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
import SpeechToText as STT

# Variables for the UI Elements and the App Itself
app = QtWidgets.QApplication(sys.argv)
ui = Ui_Form()


# Sets all ui Element states and starts Run in STT
def Run():
    ui.btnRun.setEnabled(False)
    ui.btnStop.setEnabled(True)
    ui.comBoxLanguage.setEnabled(False)
    ui.comBoxTranslation.setEnabled(False)
    ui.chBoxTranslation.setEnabled(False)
    ui.spBoxSeconds.setEnabled(False)
    ui.keySequenceRecord.setEnabled(False)
    ui.keySequenceOpenChat.setEnabled(False)
    STT.Setup(ui.spBoxSeconds.property("value"), ui.keySequenceRecord.keySequence().toString(),
              ui.comBoxLanguage.currentText(), ui.lwDisplay, ui.comBoxTranslation.currentText(),
              ui.keySequenceOpenChat.keySequence().toString())


# Sets all ui Element states and starts Stop in STT
def Stop():
    ui.lwDisplay.clear()
    ui.btnRun.setEnabled(True)
    ui.btnStop.setEnabled(False)
    ui.comBoxLanguage.setEnabled(True)
    ui.chBoxTranslation.setEnabled(True)
    ui.comBoxTranslation.setEnabled(ui.chBoxTranslation.isChecked())
    ui.spBoxSeconds.setEnabled(True)
    ui.keySequenceRecord.setEnabled(True)
    ui.keySequenceOpenChat.setEnabled(True)
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
