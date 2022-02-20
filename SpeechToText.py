from time import sleep

import speech_recognition
import sounddevice
import soundfile
import googletrans
import keyboard
import kthread
import queue
import timeit
import io

FILE_NAME = "recording.wav"
SAMPLE_RATE = 16000
stt = None

global recording
recording = False
global key_pressed
key_pressed = False

data_queue = queue.Queue()

recognizer = speech_recognition.Recognizer()
translator = googletrans.Translator()


# fileLength, recognitionLanguage, translationLanguage, display, recordKey, openChatKey, closeChatKey


def Setup(fileLength, sleepLength, recognitionLanguage, translationLanguage, display, recordKey, openChatKey, closeChatKey):
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
        target=lambda: Run(fileLength,sleepLength / 1000, recognitionLanguage, translationLanguage, display, recordKey, openChatKey,
                           closeChatKey))
    stt.setDaemon(True)
    stt.start()


# Kills the thread
def Stop():
    global stt
    stt.kill()


def Run(fileLength, sleepLength, recognitionLanguage, translationLanguage, display, recordKey, openChatKey, closeChatKey):
    display.addItem(f"Started: \nLanguage ={recognitionLanguage}\nTranslation = {translationLanguage}\n"
                    f"File Length = {fileLength} sec")

    # setting up tracking for key to avoid counting holding as multiple pressing
    global recording

    def change_recording(_):
        global key_pressed
        if not key_pressed:
            global recording
            recording = not recording
            key_pressed = True

    def change_key_pressed(_):
        global key_pressed
        key_pressed = False

    keyboard.on_press_key(recordKey, change_recording)
    keyboard.on_release_key(recordKey, change_key_pressed)

    while True:
        display.addItem(f"Waiting for Key Input {recordKey}")
        keyboard.wait(recordKey)
        # timer to break if recording time is reached
        start = timeit.default_timer()
        file_stream = io.BytesIO()
        display.addItem("Recording")

        def callback(indata, frames, time, status):
            data_queue.put(indata.copy())

        with soundfile.SoundFile(file_stream, format="WAV", mode='w', samplerate=SAMPLE_RATE, channels=1) as file:
            with sounddevice.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback):
                # write Stream to file while recording is not stopped by keypress or time
                while recording:
                    if timeit.default_timer() - start > fileLength:
                        display.addItem("Max recording Time elapsed...")
                        recording = False
                    file.write(data_queue.get())
                file.write(data_queue.get())

        # Open the File
        file_stream.seek(0)
        with speech_recognition.AudioFile(file_stream) as source:
            # Records the Audio in the recognizer
            audioData = recognizer.record(source)

        # Tries to recognize with google in the set Language
        try:
            text = recognizer.recognize_google(audioData, language=recognitionLanguage)
        except BaseException as error:
            display.addItem(f"Error while recognizing: {error}")
            text = ""

        # Translates when a Translation language is set
        if translationLanguage is not None:
            # Tries to translate with google
            try:
                message = translator.translate(text, dest=translationLanguage).text
            except BaseException as error:
                display.addItem(f"Error while Translating: {error}")
                message = ""
        else:
            message = text

        if message:
            display.addItem(f"Sending: {message}")
            keyboard.press_and_release(openChatKey)
            sleep(sleepLength)
            keyboard.write(message)
            sleep(sleepLength)
            keyboard.press_and_release(closeChatKey)
        else:
            display.addItem('Nothing to send')
