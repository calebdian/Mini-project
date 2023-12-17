import speech_recognition as sr
import antigravity
from time import ctime
import webbrowser
import time
import pyaudio
import os
import random
from gtts import gTTS
from playsound import playsound
from mutagen.mp3 import MP3
from flask import Flask, render_template, request, redirect, url_for




app = Flask(__name__)

r = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record():
    voice_data = record_audio()
    response = respond(voice_data)
    return response



def record_audio(ask = False):
    with sr.Microphone() as source:
        if ask:
            speech_feedback(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speech_feedback('Sorry, I did not get that')
        except sr.RequestError:
            speech_feedback('Sorry, my speech service is down')
        voice_data = r.recognize_google(audio)
        speech_feedback(voice_data)
        return voice_data

def speech_feedback(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

def respond(voice_data):
    if 'What is your name' in voice_data:
        speech_feedback('My name is Speech to Text')
    if 'What is the time' in voice_data:
        speech_feedback(ctime())
    if 'Search' in voice_data:
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        speech_feedback('Here is what I found for' + search)
    if 'Find location' in voice_data:
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place' + location + '/amp;'
        webbrowser.get().open(url)
        speech_feedback('Here is the location of' + location)
    if 'exit' in voice_data:
        exit()



time.sleep(1)
speech_feedback('How can I help you?')
while 1:
    voice_data = record_audio()
    respond(voice_data)

if __name__ == '__main__':
    app.run(debug=True)