from machine import Pin, ADC
from time import sleep
sound = Pin(20,Pin.IN, Pin.PULL_UP)
r = Pin(16,Pin.OUT)
g = Pin(17,Pin.OUT)
b = Pin(18,Pin.OUT)

def high():
    r.value(1)
    while r.value == 1:
        
def low():

def optimal():

def warning():

def sound():
    led.value(0)
    while True:
        sound = sound.value()
        if sound == 1:
            led.value(1)
            sleep(0.1)
        else:
            led.value(0)

def timer():


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









