sound = Pin(18,Pin.IN, Pin.PULL_UP)
led = Pin(16, Pin.OUT)

def high():

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
        if '''temp >= 21''':

from machine import Pin, ADC
from time import sleep








