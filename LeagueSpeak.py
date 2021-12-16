import speech_recognition as sr
import numpy as np
import sounddevice as sd
import wave

import keyboard
import pyautogui as pag

from time import sleep


FILE_NAME = './test.wav'  #File name to save
wave_length = 4  #Recording length (seconds)
sample_rate = 16_000  #Sampling frequency
while True:
    keyboard.wait('g')
    print("RECORDING ***")
    #Start recording (wave_length Record for seconds. Wait until the recording is finished with wait)
    data = sd.rec(int(wave_length * sample_rate), sample_rate, channels=1)
    sd.wait()
   
    #Normalize. Since it is recorded with 16 bits of quantization bit, it is maximized in the range of int16.
    data = data / data.max() * np.iinfo(np.int16).max
   
    # float -> int
    data = data.astype(np.int16)
   
    #Save file
    with wave.open(FILE_NAME, mode='wb') as wb:
        wb.setnchannels(1)  #monaural
        wb.setsampwidth(2)  # 16bit=2byte
        wb.setframerate(sample_rate)
        wb.writeframes(data.tobytes())  #Convert to byte string
       
       
   
   
    filename = "test.wav"
    r = sr.Recognizer()
   
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        print(text)

    keyboard.press_and_release('enter')
    sleep(0.01)
    pag.write(text)
    keyboard.press_and_release('enter')