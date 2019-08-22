import speech_recognition as sr
import os #na spouštění programů
#import subprocess #pro práci s cmd
#import pdb #debug
#import time
#import glob #alternativní výpis souborů
import ts3 #ts3query
import params #pomocný .py s vars
import re #regex

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


def number_check(num):
    return bool(re.search(r'\d', num))


def frantisek_replace(inp):
    val = inp.replace('Františku ', '')
    return val


def ts3login(ts3conn):
    try:
        ts3conn.login(
            client_login_name="loupo",
            client_login_password="xzHjtnwP"  # hodit hesla do samostatného .py a gitignorovat jej ??
        )
    except ts3.query.TS3QueryError as err:
        print("Login failed:", err.resp.error["msg"])


def ts3kick(client_name):
    with ts3.query.TS3ServerConnection(params.ts_ip) as ts3conn:
        ts3login(ts3conn)
        ts3conn.use(sid=1)
        for client in ts3conn.clientlist():
            if client["client_nickname"].lower() == client_name.lower():
                ts3conn.clientkick(reasonid=5, reasonmsg="Franta tě kopl", clid=client["clid"])
                print("František osobu úspěšně vykopl")
                break


def ts3ban(client_name, duration):
    with ts3.query.TS3ServerConnection(params.ts_ip) as ts3conn:
        ts3login(ts3conn)
        ts3conn.use(sid=1)
        for client in ts3conn.clientlist():
            if client["client_nickname"].lower() == client_name.lower():
                ts3conn.banclient(clid=client["clid"], time=duration, banreason="František tě zabanoval, zřejmě jsi byl neposlušný")
                print("František osobu úspěšně zabanoval")
                break


def ts3names(client_name):
    if "Lukáš" == client_name:
        name = params.namca
    elif "Tomáš" == client_name:
        name = params.repak
    elif "Epic" == client_name:
        name = params.epik
    elif "Karel" == client_name:
        name = params.karel
    else:
        name = client_name

    return name


def app_start():
    mic_input = recognize_speech_from_mic(rec, mic)
    print(mic_input["transcription"])
    if mic_input["transcription"]:
        noprogram = 0 #kvůli hláškám
        program = mic_input["transcription"]
        try:
            if "Františku" in program:
                noprogram = 0
                program = frantisek_replace(program)
                program_start(program)
            elif "vypni stroj" in program:
                noprogram = 1
                os.system('shutdown -s -t 10')
                print("Vypínám systém za 10 sekund")
                abort_cmd = input("Vypínám za 10 sekund, pro zrušení vypnutí použjite command a nebo abort - ")
                if abort_cmd in params.dialog_aborts:
                    os.system('shutdown -a')
                    print("Vypnutí systému zrušeno")
            elif "kopni" in program:
                noprogram = 1
                client_name = program.replace('kopni ', '')
                if "Františku" in program:
                    client_name = frantisek_replace(program)
                client_name = ts3names(client_name)
                ts3kick(client_name)
            elif "zlikviduj" in program:
                noprogram = 1
                client_name = program.replace('zlikviduj ', '')
                if "Františku" in program:
                    client_name = frantisek_replace(program)
                if number_check(client_name):
                    ban_duration = int(re.search(r'\d+', client_name).group(0)) #získání čísla ze stringu (regex + převedení na int)
                    client_name = client_name.replace(' ' + str(ban_duration), '') #nutné replacnout číslo i mezeru před ním
                else:
                    ban_duration = 30 #defaultní čas pro bany
                client_name = ts3names(client_name)
                ts3ban(client_name, ban_duration)
            elif "vypni se" in program:
                print("František se vypíná...")
                exit(0)
            else:
                noprogram = 0
                program_start(program)
        except:
            if noprogram == 0:
                print("Program nenalezen")
        finally:
            reset = input("František dokončil dotaz, chcete restartovat?")
            if reset in params.dialog_confirmations:
                app_start()
            else:
                exit(0)
    else:
        err_msg = input("Chyba - František nebyl schopen rozeznat příkaz, resetovat?") #ošetření proti pádu programuu
        if err_msg in params.dialog_confirmations:
            app_start()


start = input("Pro spuštění skriptu stiskni enter")
app_start()
