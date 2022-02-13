from time import sleep

import numpy
import speech_recognition
import sounddevice
import wave
import googletrans
import keyboard
import kthread

FILE_NAME = "recording.wav"
SAMPLE_RATE = 16000
stt = None

recognizer = speech_recognition.Recognizer()
translator = googletrans.Translator()


def Setup(fileLength, recordKey, recognitionLanguage, display, translationLanguage, openChatKey):
    # Tries to get the Language code with the set Languages
    try:
        recognitionLanguage = googletrans.LANGCODES[recognitionLanguage]
        translationLanguage = googletrans.LANGCODES[translationLanguage]
    except:
        pass

    if translationLanguage == "None":
        translationLanguage = None

    global stt

    # Creates a Thread for the Voice Recognition
    stt = kthread.KThread(
        target=lambda: Run(fileLength, recordKey, recognitionLanguage, display, translationLanguage, openChatKey))
    stt.setDaemon(True)
    stt.start()


# Kills the thread
def Stop():
    global stt
    stt.kill()


def Run(fileLength, key, recognitionLanguage, display, translationLanguage, openChatKey):
    display.addItem(f"Started: \nLanguage ={recognitionLanguage}\nTranslation = {translationLanguage}\n"
                    f"File Length = {fileLength} sec")
    while True:
        display.addItem(f"Waiting for Key Input {key}")
        keyboard.wait(key)  # Waits for the set Key to be pressed

        display.addItem("Recording")
        # Starts recording. fileLength = Recording Length
        data = sounddevice.rec(int(fileLength * SAMPLE_RATE), SAMPLE_RATE, channels=1)
        sounddevice.wait()  # Waits until recording is finished

        # Normalize. Since it is recorded with 16 bits of quantization bit, it is maximized in the range of int16.
        data = data / data.max() * numpy.iinfo(numpy.int16).max
        data = data.astype(numpy.int16)  # Converts float -> int

        # Saves the File
        with wave.Wave_write(FILE_NAME) as file:
            file.setnchannels(1)
            file.setsampwidth(2)
            file.setframerate(SAMPLE_RATE)
            file.writeframes(data.tobytes())

        # Open the File
        with speech_recognition.AudioFile(FILE_NAME) as source:
            # Records the Audio in the recognizer
            audioData = recognizer.record(source)

            # Tries to recognize with google in the set Language
            try:
                text = recognizer.recognize_google(audioData, language=recognitionLanguage)
            except:
                text = ""

        # Translates when a Translation language is set
        if translationLanguage is not None:
            # Tries to translate with google
            try:
                message = translator.translate(text, dest=translationLanguage).text
            except:
                pass
        else:
            message = text

        display.addItem(f"Sending: {message}")

        keyboard.press_and_release(openChatKey)
        sleep(0.1)
        keyboard.write(message)
        sleep(0.1)
        keyboard.press_and_release(openChatKey)
