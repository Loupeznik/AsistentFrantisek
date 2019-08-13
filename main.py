import speech_recognition as sr
import os
import pdb
import time
import glob


rec = sr.Recognizer()
mic = sr.Microphone()


def recognize_speech_from_mic(recognizer, microphone):

    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='cs-CZ')
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response


def program_start(program):
    os.startfile('src\{}'.format(program))
    print("František startuje " + program)


def app_start():
    mic_input = recognize_speech_from_mic(rec, mic)
    # apps = ["apex", "šestka", "coso", "stellaris"]
    print(mic_input["transcription"])
    #input("Press Enter to continue...")
    # if mic_input["transcription"].lower() == "františku":
    #    print("František připraven")
    # time.sleep(10)
    # pdb.set_trace()
    # input("Press Enter to continue...")
    #    mic_query = recognize_speech_from_mic(rec, mic)
    if mic_input["transcription"]:
        program = mic_input["transcription"]
        # print(program)
        #dir_list = os.listdir("src")
        #dir_list = glob.glob('src\*')
        #print(dir_list) #debug
        try:
            if "Františku" in program:
                program = program.replace('Františku ', '')
                program_start(program)
                # input("Press Enter to continue...")
            else:
                program_start(program)
        except:
            print("Program nenalezen")
        finally:
            reset = input("František dokončil dotaz, chcete restartovat?")
            if reset in ["y", "yes", "ano"]:
                app_start()
            else:
                exit(0)
    else:
        print("error")

start = input("Pro spuštění skriptu stiskni S: ")
if start in ["S", "s"]:
    app_start()

