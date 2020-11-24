timetable = {
    "montag": {
        "08:00": "",
        "08:45": "",
        "09:30": "",
        "10:15": "Pause",
        "10:35": "",
        "11:20": "",
        "12:05": "Aus",
        "23:59": "Aus",
    },
    "dienstag": {
        "08:00": "",
        "08:45": "",
        "09:30": "",
        "10:15": "Pause",
        "10:35": "",
        "11:20": "",
        "12:05": "",
        "23:59": "Aus",
    },
    "mittwoch": {
        "08:00": "",
        "08:45": "",
        "09:30": "",
        "10:15": "Pause",
        "10:35": "",
        "11:20": "",
        "12:05": "Aus",
        "23:59": "Aus",
    },
    "donnerstag": {
        "08:00": "",
        "08:45": "",
        "09:30": "",
        "10:15": "Pause",
        "10:35": "",
        "11:20": "",
        "12:05": "",
        "23:59": "Aus",
    },
    "freitag": {
        "08:00": "",
        "08:45": "",
        "09:30": "",
        "10:15": "Pause",
        "10:35": "",
        "11:20": "",
        "12:05": "",
        "23:59": "Aus",
    },
}

import selenium.webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import requests
import json
from googletrans import Translator
translator = Translator()
from datetime import datetime
from random import randint

driver = selenium.webdriver.Firefox()
driver.get("https://login.schulmanager-online.de/#/modules/messenger/messages")

def login():
    username = driver.find_element_by_class_name("email-or-username-input")
    username.send_keys("Deine E-Mail/Benutzername")
    password = driver.find_element_by_id("password")
    password.send_keys("Dein Passwort")
    password.send_keys(Keys.RETURN)

def enterChat():
    print('Enter a channel id:')
    id = input()
    driver.get("https://login.schulmanager-online.de/#/modules/messenger/messages/" + id)

def send(text):
    textarea = driver.find_element_by_tag_name('textarea')
    textarea.send_keys(text)
    sendBtn = driver.find_element_by_class_name("send-button")
    sendBtn.send_keys(Keys.RETURN)

def read():
    global message
    message = driver.find_elements_by_class_name("message-text")[-1].get_attribute('innerHTML')

def calc(arg):
    solution = str(eval(arg))
    solutionMessage = "Dein Ergebnis für die Aufgabe " + arg + " ist " + solution
    send(solutionMessage)

def corona():
    global response

    response = requests.post("https://wrapapi.com/use/triggeredLife/corona/counter/0.0.1", json={
      "wrapAPIKey": "D0DSlqUlwxEb27wXyxteTVPQOULzBXOO"
    })
    response = response.json()
    response = response["data"]
    response = response["output"]

def trans(arg):
    print(arg)
    if(arg.startswith("de")):
        arg = arg.replace("de ", "")
        send("Original: " + arg + "\nDeutsch: " + str(translator.translate(arg, dest='de').text))
    elif(arg.startswith("en")):
        arg = arg.replace("en ", "")
        send("Original: " + arg + "\nEnglisch: " + str(translator.translate(arg, dest='en').text))
    elif(arg.startswith("fr")):
        arg = arg.replace("fr ", "")
        send("Original: " + arg + "\nFranzösisch: " + str(translator.translate(arg, dest='en').text))
    else:
        send("Diese Sprache kann ich noch nicht.")

def gong():
    now = datetime.now()
    dayNum = datetime.today().weekday()
    if(dayNum == 5 or dayNum == 6):
        return
    current_time = now.strftime("%H:%M:%S")
    if(current_time == "8:00:00"):
        send("Gong")
    elif(current_time == "8:45:00"):
        send("Gong")
    elif(current_time == "9:30:00"):
        send("Gong")
    elif(current_time == "10:15:00"):
        send("Gong")
    elif(current_time == "10:35:00"):
        send("Gong")
    elif(current_time == "11:20:00"):
        send("Gong")
    elif(current_time == "12:05:00"):
        send("Gong")
    elif(current_time == "12:50:00"):
        send("Gong")

def ssp(arg):
    random = randint(1, 3)
    # 1: Schere, 2: Stein, 3: Papier
    if(arg.upper() == "SCHERE" or arg.upper() == "STEIN" or arg.upper() == "PAPIER"):
        if(random == 1):
            if(arg.upper() == "SCHERE"):
                send("Unentschieden! Ich hatten auch Schere.")
            elif(arg.upper() == "STEIN"):
                send("Du hast gewonnen! Ich hatte Schere.")
            elif(arg.upper() == "PAPIER"):
                send("Du hast verloren! Ich hatte Schere.")
        elif(random == 2):
            if(arg.upper() == "SCHERE"):
                send("Du hast verloren! Ich hatte Stein.")
            elif(arg.upper() == "STEIN"):
                send("Unentschieden! Ich hatten auch Stein.")
            elif(arg.upper() == "PAPIER"):
                send("Du hast gewonnen! Ich hatte Stein.")
        elif(random == 3):
            if(arg.upper() == "SCHERE"):
                send("Du hast gewonnen! Ich hatte Papier.")
            elif(arg.upper() == "STEIN"):
                send("Du hast verloren! Ich hatte Papier.")
            elif(arg.upper() == "PAPIER"):
                send("Unentschieden! Ich hatten auch Papier.")
    else:
        return send("Bitte schreibe Schere, Stein oder Papier nach /ssp")

def next():
    now = datetime.now()

    time = now.strftime("%H:%M")
    dayNum = datetime.today().weekday()
    weekDays = ["montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag", "sonntag"]
    day = weekDays[dayNum]

    if(dayNum == 5 or dayNum == 6):
        send("Heute ist frei (:")
    else:
        tableToday = timetable[day]
        for i in tableToday:
            if(time < i):
                send("Nächste Stunde haben wir " + tableToday[i])
                break

login()
time.sleep(5)
enterChat()
time.sleep(2)
global oldMessage
oldMessage = ""
while True:
    gong()
    read()
    if oldMessage != message:
        print("Neue Nachricht: " + message)
        if message.startswith('/calc '):
            calc(message.replace("/calc ", ""))
        if message == "/corona":
            corona()
            send("Infizierte: " + response[0] + "\nTote: " + response[1] + "\nWiederhergestellte: " + response[2])
        if(message.startswith('/trans')):
            trans(message.replace("/trans ", ""))
        if(message == "/help"):
            send("Aktuelle Befehle:\n/help\n   Zeigt alle Befehle an\n/next\n   Zeigt an, was man in der nächsten Stunde hat.\n/calc <Aufgabe>\n   Taschenrechner Plus: + ,  Minus: - ,  Mal: * ,  Geteiltdurch: /\n/trans <Zielsprache> <Text>\n   Übersetzt deinen Text in Deutsch, Englisch oder Französisch.\n   Nach Deutsch: de\n   Nach Englsich: en\n   Nach Französisch: fr\n/ssp <Schere/Stein/Papier>\n   Spiele Schere, Stein oder Papier.")
        if(message.startswith("/ssp")):
            ssp(message.replace("/ssp ", ""))
        if(message == "/next"):
            next()

    oldMessage = message
    time.sleep(1)
