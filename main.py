####################################################################################################
# IMPORTS
####################################################################################################
import speech_recognition as sr
import os
import pdb
import time
import glob
import pyttsx3 # pip3 install pyttsx3   Python text to speech offline library

####################################################################################################
# CONSTANTS, DEFINITIONS, CONFIG
####################################################################################################
tts = pyttsx3.init()
rec = sr.Recognizer()
mic = sr.Microphone()
frantisek_calls = ["Franto", "Frantisku", "Františku", "Fando"]

####################################################################################################
# FUNCTIONS
####################################################################################################
def tts_config():                           # Config text to speech voice
    voices = tts.getProperty('voices')      # getting details of current voice
    tts.setProperty('voice', voices[1].id)  # Change voice to male

                                            # optional others
    #""" RATE"""
    rate = tts.getProperty('rate')          # getting details of current speaking rate
    tts.setProperty('rate', rate - 50)      # setting up new voice rate

    #"""VOLUME"""
    #engine.setProperty('volume',1.0)       # setting up volume level  between 0 and 1
    
def tts_say(string):                        # basically typedef say(string)
    tts.say(string)
    tts.runAndWait()

def frantisek_init():                       # Initial device check
    tts_say('Frantisek assistent initializing')
    check_devices(rec, mic)
    tts_config()
    return True

def check_devices(recognizer, microphone):                              # Makes sure all devices needed are set up correctly
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")


def recognize_speech_from_mic(recognizer, microphone, audio):

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='cs-CZ')    # Convert speech to text using google
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def handle_frantisek_call(recognized):
    tts_say("I heard you..!")
    if "Vypni se" in recognized:
        exit()
    pass

def program_start(program):
    os.startfile('src\{}'.format(program))
    print("František startuje " + program)


def app_start():
    with mic as source:
        tts_say("Frantisek ready to serve, you can command him now")
        i = 0
        while True: # Infinite loop for speech grab
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)
            mic_input = recognize_speech_from_mic(rec, mic, audio)

            if mic_input["transcription"]:
                recognized = mic_input["transcription"]
                for call in frantisek_calls:
                    if call in recognized:
                        recognized = recognized.replace(call, '')
                        handle_frantisek_call(recognized)

            else: # else from if grabbed speech
                print(i)
                i+=1
                continue
####################################################################################################
# MAIN
####################################################################################################
def main():
    if frantisek_init():
        app_start()
    else:
        print('Failed to init frantisek, exitting ...')
        exit()

main()
