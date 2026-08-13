from machine import Pin, Timer
from time import sleep, time
sound = Pin(20,Pin.IN, Pin.PULL_UP)
buzzer = Pin(0,Pin.OUT)
r = Pin(16,Pin.OUT)
g = Pin(17,Pin.OUT)
b = Pin(18,Pin.OUT)

def timer():
    global start
    start = time.ticks_s()

def checktimer():
    finish = time.tick_s() - start
    return finish

def high():
    r.value(1)
    g.value(0)
    b.value(0)
    while r.value() == 1:
        timer()
        if sound() == True:
            if timer() > 60:
                buzzer.value(1)
            else:
                buzzer.value(0)
        else:
            buzzer.value(0)
                
def low():
    r.value(0)
    g.value(0)
    b.value(1)
    while b.value() == 1:
        timer()
        if sound() == True:
            if timer() > 60:
                buzzer.value(1)
            else:
                buzzer.value(0)
        else:
            buzzer.value(0)

def optimal():
    r.value(0)
    g.value(1)
    b.value(0)
    buzzer.value(0)

def warning():
    r.value(1)
    g.value(1)
    b.value(0)

def sound():
    if buzzer.value() or r.value() == 1:
        while True:
            sound = sound.value()
            if sound == 1:
                buzzer.value(0)
                sleep(0.1)
            else:
                led.value(0)

def main():
    #temp = sensor code
    #wet = sensor code
    while True:
        if temp >= 21:
            if temp > 22:
                high()
            else:
                warning()
        else:
            if temp <= 16:
                if temp < 15:
                    low()
                else:
                    warning()
            else:
                optimal()

        if wet >= 51:
            if temp > 60:
                high()
            else:
                warning()
        else:
            if wet <= 34:
                if wet < 30:
                    low()
                else:
                    warning()
            else:
                optimal()









