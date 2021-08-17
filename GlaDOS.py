import datetime
import numpy as np
import face_recognition
from datetime import datetime
import pyttsx3
import os
import random
import webbrowser
import time
import speech_recognition as sr
import pandas as pd
from tkinter import *
from fuzzywuzzy import fuzz
from colorama import *
import pyfirmata
import time
from pyfirmata import Arduino, util
import cv2
# раздел глобальных переменных
board = pyfirmata.Arduino('COM3')



r = sr.Recognizer()
m = sr.Microphone(device_index=1)
with m as source:
    r.adjust_for_ambient_noise(source)
engine = pyttsx3.init()
text = ''
j = 0
task_number = 0
ndel = ['глэдос', "глэдас", 'глонасс', 'гладос', 'glados', 'gledos','глаза', 'ладно', 'не могла бы ты', 'пожалусйта']

commands = ['привет', 'открой файл', 'выключи комп', 'выруби компьютер', 'пока', 'покажи файл', 'покажи список команд',
            'открой vk', 'открой браузер', 'включи vk', "Видео", 'открой интернет', 'открой youtube', 'включи музон', 'зови меня',
            'вруби музыку', 'открой дверь', 'закрой дверь', "включи свет", 'выключи свет','есть работа', 'хватит', 'называй',
            'открой стату', 'покажи cтатистику', 'я хочу расслабиться', 'переведи', 'на будущее', 'что планируется']

# раздел описания функций комманд
os.startfile(r'C:\Users\User\Downloads\GLaDOS-248565.wav')

servo = board.get_pin('d:8:s')
def pri_com():  # выводит на экран историю запросов
    z = {}
    mas = []
    mas2 = []
    mas3 = []
    mas4 = []
    file = open('commands.txt', 'r', encoding='UTF-8')
    k = file.readlines()
    for i in range(len(k)):
        line = str(k[i].replace('\n', '').strip())
        mas.append(line)
    file.close()
    for i in range(len(mas)):
        x = mas[i]
        if x in z:
            z[x] += 1
        if not (x in z):
            b = {x: 1}
            z.update(b)
        if not (x in mas2):
            mas2.append(x)
    for i in mas2:
        mas3.append(z[i])
    for i in range(1, len(mas3) + 1):
        mas4.append(str(i) + ') ')
    list = pd.DataFrame({
        'command': mas2,
        'count': mas3
    }, index=mas4)
    list.index.name = '№'
    print(list)

def face():
    servo.write(0)

def arduino2():
    path = 'KnownFaces'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cls in myList:
        curImg = cv2.imread(f'{path}/{cls}')
        images.append(curImg)
        classNames.append(os.path.splitext(cls)[0])

    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print("Декодирование закончено")

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        board.digital[13].write(0)
        board.digital[11].write(0)
        board.digital[12].write(1)

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            matchIndex = np.argmin(faceDis)
            name = classNames[matchIndex]
            if matches[matchIndex]:
                name = classNames[matchIndex]
                # print(name)
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                if name == 'Samuel':
                    board.digital[13].write(1)
                    board.digital[12].write(0)
                    board.digital[11].write(0)
                    servo.write(180)
                    os.startfile(r'C:\Users\User\Downloads\GLaDOS-308343.wav')
                    time.sleep(2)
                    board.digital[13].write(0)
                    board.digital[12].write(0)
                    board.digital[11].write(0)
                    cv2.destroyAllWindows()
                    return
                if name == 'Kasia':
                    os.startfile(r'C:\Users\User\Downloads\GLaDOS-320018.wav')
                    time.sleep(4)
                    cv2.destroyAllWindows()
                    return
                else:
                    board.digital[13].write(0)
                    board.digital[12].write(0)
                    board.digital[11].write(1)
        cv2.imshow("WebCam", img)
        cv2.waitKey(1)



def clear_analis():  # очистка файла с историей запросов
    global engine
    file = open('commands.txt', 'w', encoding='UTF-8')
    file.close()
    engine.say('Файл аналитики очищен!')


def add_file(x):
    file = open('commands.txt', 'a', encoding='UTF-8')
    if x != '':
        file.write(x + '\n')
    file.close()


def comparison(x):  # осуществляет поиск самой подходящей под запрос функции
    global commands, j, add_file
    ans = ''
    for i in range(len(commands)):
        k = fuzz.ratio(x, commands[i])
        if (k > 50) & (k > j):
            ans = commands[i]
            j = k
    if (ans != 'пока') & (ans != 'привет'):
        add_file(ans)
    return (str(ans))

def web_search():  # осуществляет поиск в интернете по запросу (adress)
    global adress
    webbrowser.open('https://yandex.ru/yandsearch?clid=2028026&text={}&lr=11373'.format(adress))


def check_searching():  # проверяет нужно-ли искать в интернете
    global text, wifi_name, add_file
    global adress
    global web_search
    if 'найди' in text:
        add_file('найди')
        adress = text.replace('найди', '').strip()
        text = text.replace(adress, '').strip()
        web_search()
        text = ''
    elif 'найти' in text:
        add_file('найди')
        adress = text.replace('найти', '').strip()
        text = text.replace(adress, '').strip()
        web_search()
        text = ''
    adress = ''

def arduino():

    board.digital[10].write(1)

def arduino1():
    board.digital[10].write(0)



def arduino3():
    servo.write(0)
    time.sleep(2)
    os.startfile(r'C:\Users\User\Downloads\GLaDOS-271939.wav')

def clear_task():  # удаляет ключевые слова
    global text, ndel
    for z in ndel:
        text = text.replace(z, '').strip()
        text = text.replace('  ', ' ').strip()


def hello():  # функция приветствия
    global engine
    c = os.startfile(r'C:\Users\User\Downloads\GLaDOS-308343.wav')
    v = os.startfile(r'C:\Users\User\Downloads\GLaDOS-308343.wav')
    z = [c, v]
    x = random.choice(z)



def quit():  # функция выхода из программы
    global engine
    os.startfile(r'C:\Users\User\Downloads\GLaDOS-248563.wav')
    engine.runAndWait()
    engine.stop()
    os.system('cls')
    exit(0)


def show_cmds():  # выводит на экран список доступных комманд
    my_com = ['привет', 'открой файл', 'выключи компьютер', 'пока', 'покажи список команд',
              'открой vk', 'открой интернет', 'открой youtube', 'включи музыку', 'очисти файл',
              'плотва','покажи cтатистику','ведьмак','называй', "зови меня"]
    for i in my_com:
        print(i)



def brows():  # открывает браузер
    webbrowser.open('https://google.ru')


def ovk():  # открывает вк
    webbrowser.open('https://vk.com/feed')


def youtube():  # открывает ютюб
    webbrowser.open('https://www.youtube.com')
    engine.runAndWait()


def shut():  # выключает компьютер
    global quit
    os.system('shutdown /s /f /t 10')
    quit()


def musik():  # включает музыку
    webbrowser.open('https://vk.com/')

def plotwa():
    os.startfile(r'C:\Users\User\Downloads\GLaDOS_Please_stand_clear_of_the_doors_.wav')
def pl():
    os.startfile(r'C:\Users\User\Downloads\GLaDOS-261795.wav')



def theme():
    global text, tr
    tr = 0
    sam = ['называй меня', 'зови меня', 'зовут', 'меня зовут', "называй"]
    for s in sam:
        if (s in text) & (tr == 0):
            word = text
            word = word.replace(s, '').strip()
            engine.say(word)
            tr = 1
            text = ''

def check_translate():
    global text, tr
    tr = 0
    variants = ['переведи', 'перевести', 'называть', 'называй']
    for i in variants:
        if (i in text) & (tr == 0):
            word = text
            word = word.replace('называй', '').strip()
            word = word.replace('меня', '').strip()
            word = word.replace('переводить', '').strip()
            word = word.replace('перевод', '').strip()
            word = word.replace('слово', '').strip()
            word = word.replace('слова', '').strip()
            engine.say('хорошо буду звать тебя как' + word)
            print(word)
            tr = 1
            text = ''



cmds = {
    'привет': hello, 'выруби компьютер': shut, 'выключи комп': shut, 'хватит': quit,
    'пока': quit, 'покажи  cтатистику': pri_com, 'покажи список команд': show_cmds,
    'открой браузер': brows, 'включи vk': ovk, 'открой интернет': brows,
    'открой youtube': youtube, 'вруби музыку': musik, 'открой vk': ovk,
    'открой  стату': pri_com, 'включи музон': musik, 'открой дверь': arduino2, 'закрой дверь': arduino3,
    'покажи файл': pri_com, 'открой файл': pri_com, 'я хочу расслабиться': musik,
    'на будущее': plotwa, 'включи свет': arduino, 'выключи свет': arduino1, "Видео": face,
    'называй': check_translate, 'плотва': plotwa, 'сюда плотва': pl, 'есть работа': pl, 'включи ведьмака': plotwa
}


# распознавание

def talk():
    global text, clear_task
    text = ''
    with sr.Microphone() as sourse:
        print('Я вас слушаю: ')
        r.adjust_for_ambient_noise(sourse)
        audio = r.listen(sourse, phrase_time_limit=2.5)
        try:
            text = (r.recognize_google(audio, language="ru-RU")).lower()
        except(sr.UnknownValueError):
            pass
        except(TypeError):
            pass
        os.system('cls')
        lb['text'] = text
        clear_task()

# выполнение команд

def cmd_exe():
    global cmds, engine, comparison, check_searching, task_number, text, lb
    check_translate()
    theme()
    text = comparison(text)
    print(text)
    check_searching()
    if (text in cmds):
        if (text != 'привет') & (text != 'пока') & (text != 'покажи список команд') & (text != "называй"):
            os.startfile(r'C:\Users\User\Downloads\GLaDOS-261794.wav')
        cmds[text]()
    elif text == 'глэдос':
        pass
    else:
        print('Команда не найдена!')
    task_number += 1
    if (task_number % 10 == 0):
        engine.say('У вас будут еще задания?')
    engine.runAndWait()
    engine.stop()


# исправляет цвет

print(Fore.GREEN + '', end='')
os.system('cls')


# основной бесконечный цикл

def main():
    global text, talk, cmd_exe, j
    try:
        talk()
        if text != '':
            cmd_exe()
            j = 0
    except(UnboundLocalError):
        pass
    except(TypeError):
        pass
    time.sleep(0.05)
    return main()
# раздел создания интерфейса

root = Tk()

lb = Label(root, text=text)

main()




while True:
    main()