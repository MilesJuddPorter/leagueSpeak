import speech_recognition
import sounddevice
import keyboard
import wave
import numpy
from time import sleep
import googletrans

FILE_NAME = "recording.wav"
WAVE_LENGTH = 4  # Length of the Audio File
SAMPLE_RATE = 44100
TRANSLATION_LANGUAGE = 'EN'  # Default = EN

translate = False  # When True the Program translates into the set Destination

if translate:
    translator = googletrans.Translator()

recognizer = speech_recognition.Recognizer()

while True:
    keyboard.wait('g')  # Waits for the key G to be pressed
    print('RECORDING')  # Prints 'RECORDING' in the Console
    data = sounddevice.rec(int(WAVE_LENGTH * SAMPLE_RATE), SAMPLE_RATE, 1)
    sounddevice.wait()
    print('DONE RECORDING')

    # Normalizes, because it is recorded with 16 bits of quantization bit, it is maximized in the range of int16
    data = data / data.max() * numpy.iinfo(numpy.int16).max
    # Convert float -> int
    data = data.astype(numpy.int16)

    # Saves the file
    with wave.Wave_write(FILE_NAME) as file:
        file.setnchannels(1)
        file.setsampwidth(2)
        file.setframerate(SAMPLE_RATE)
        file.writeframes(data.tobytes())

    # Loads the file
    with speech_recognition.AudioFile(FILE_NAME) as source:
        # Records the Audio File
        audioData = recognizer.record(source)
        # Recognizes the words with google
        text = recognizer.recognize_google(audioData, language="de-DE")

    # Can translate the spoken message with google into the set destination
    # (Maybe user deepl?)
    if translate:
        message = translator.translate(text, dest=TRANSLATION_LANGUAGE).text
    else:
        message = text

    # Writes message in League of Legends Chat
    keyboard.press_and_release('enter')
    sleep(0.1)
    keyboard.write(message)
    keyboard.press_and_release('enter')
