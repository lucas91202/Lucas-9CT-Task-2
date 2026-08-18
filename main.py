from machine import Pin, Timer
from time import sleep, time
from dht import DHT11
soundsensor = Pin(22,Pin.IN, Pin.PULL_UP) #Sound sensor
buzzer1 = Pin(0,Pin.OUT) #Both buzzers for temperature and humidity
buzzer2 = Pin(15,Pin.OUT)
sensor = DHT11(Pin(15, Pin.IN, Pin.PULL_UP)) #temperature and humidity sensor pin
r1 = Pin(18,Pin.OUT) #First rgb light Pin setup
g1 = Pin(17,Pin.OUT)
b1 = Pin(16,Pin.OUT)
r2 = Pin(21,Pin.OUT) #Second rgb light Pin setup
g2 = Pin(20,Pin.OUT)
b2 = Pin(19,Pin.OUT)

def timer(ticks=time.ticks_ms):
    """Starts a timer using time.tick_ms. This code is taken and edited from 3.5 of the Raspberry Pi Pico tutorials."""
    start = ticks()
    return time.ticks_diff(ticks(), start)


def checktimer():
    """Calculates the time, checking what time the timer has reached since it has started. Again, code is 
    taken and edited from 3.5 of the Raspberry Pi Pico tutorials"""
    finish = time.tick_ms() - start
    return finish

def disablebuzzer():
    """Acts as a timer function to disable the buzzer. This starts the buzzer."""
    global disable
    disable = time.tick_ms()

def checkbuzzer():
    """Used whenever the buzzer is supposed to turn on. Checks if 10 minutes is up to allow the buzzer to turn on."""
    current_time = time.tick_ms() - disable
    if current_time < 600000:
        return False
    else:
        return True
    
def high1():
    """Used for the temperature whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound."""
    if b1.value() == 0 and g1.value() == 0: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r1.value(0)
        g1.value(1)
        b1.value()
        timer()
    if sound() == True:
        buzzer1.value(0)
        disablebuzzer()
    else:
        if checktimer() > 60000:
            if checkbuzzer:
                buzzer1.value(1)
            else:
                pass

def high2():
    """Used for the temperature whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound."""
    if r2.value() == 0: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r2.value(1)
        g2.value(0)
        b2.value(0)
        timer()
    if sound() == True:
        buzzer2.value(0)
        disablebuzzer()
    else:
        if checktimer() > 60000:
            if checkbuzzer:
                buzzer2.value(1)
            else:
                pass

                    
def low1():
    if b1.value() == 0: #Reusing the AI code to make sure the timer function is only turned on once when the LEDs are turned on.
        r1.value(0)
        g1.value(0)
        b1.value(1)
        timer()
    while buzzer1.value() == 1:
        if sound() == True:
            if timer() > 60:
                buzzer1.value(1)
            else:
                buzzer1.value(0)
        else:
            buzzer1.value(0)

def optimal1():
    r1.value(0)
    g1.value(1)
    b1.value(0)
    buzzer1.value(0)

def warning1():
    r1.value(1)
    g1.value(1)
    b1.value(0)

def sound():
    if soundsensor.value() == 1:
        return True
    if soundsensor.value() == 0:
        return False

def main():
    while True:
        sensor.measure()
        temp = sensor.temperature()
        wet = sensor.humidity()
        sound()
        if temp > 22:
            high1()
        elif temp == 21 or temp == 16:
            warning1()
        elif temp >= 16 and temp <= 21:
            optimal1()
        else:
            low1()

        if wet > 60:
            high2()
        elif wet >= 51 and wet <= 60 or wet >= 30 and wet <= 34:
            warning2()
        elif wet >= 35 and wet <= 50:
            optimal2()
        else:
            low2()
        sleep(1)









