import speech_recognition as sr
import os
import subprocess
#import pdb #debug
#import time
#import glob #alternativní výpis souborů
import ts3
import params

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


#def ts3kick(user):
#    os.system('ts3cli --host localhost --username loupo --password xzHjtnwP kick ' + user)
#    legacy

def ts3kick(client_name):
    with ts3.query.TS3ServerConnection("localhost") as ts3conn:
        try:
            ts3conn.login(
                        client_login_name="loupo",
                        client_login_password="xzHjtnwP"
            )
        except ts3.query.TS3QueryError as err:
            print("Login failed:", err.resp.error["msg"])
            #exit(1)
        ts3conn.use(sid=1)
        for client in ts3conn.clientlist():
            #print(client,client_name)
            if client["client_nickname"].lower() == client_name.lower():
                ts3conn.clientkick(reasonid=5, reasonmsg="Franta tě kopl", clid=client["clid"])
                print("František osobu úspěšně vykopl")
                break
        #ts3conn.login(client_login_name="loupo", client_login_password="xzHjtnwP")


def app_start():
    mic_input = recognize_speech_from_mic(rec, mic)
    print(mic_input["transcription"])
    if mic_input["transcription"]:
        noprogram = 0 #kvůli hláškám
        program = mic_input["transcription"]
        try:
            if "Františku" in program:
                noprogram = 0
                program = program.replace('Františku ', '')
                program_start(program)
            elif "vypni stroj" in program: #testovat -- "František vypne stroj hlásí, že program nenalezen", neodpočítává, pouze hlásí že vypíná za 10 secs
                noprogram = 1
                os.system('shutdown -s -t 10')
                print("Vypínám systém za 10 sekund")
                abort_cmd = input("Vypínám za 10 sekund, pro zrušení vypnutí použjite command a nebo abort - ")
                if ["a", "abort"] in abort_cmd:
                    os.system('shutdown -a')
                    print("Vypnutí systému zrušeno")
            elif "Teamspeak query kopni" in program:
                noprogram = 1
                client_name = program.replace('Teamspeak query kopni ', '')
                if "Lukáš" in client_name:
                    client_name = params.namca
                if "Tomáš" in client_name:
                    client_name = params.repak
                if "Epik" in client_name:
                    client_name = params.epik
                ts3kick(client_name)
            else:
                noprogram = 0
                program_start(program)
        except:
            if noprogram == 0:
                print("Program nenalezen")
        finally:
            reset = input("František dokončil dotaz, chcete restartovat?")
            if reset in ["y", "yes", "ano"]:
                app_start()
            else:
                exit(0)
    else:
        print("error")


start = input("Pro spuštění skriptu stiskni enter")
app_start()

