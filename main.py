import utime
from machine import Pin, PWM
from time import sleep
from dht import DHT11
soundsensor = Pin(22,Pin.IN, Pin.PULL_UP) #Sound sensor
buzzer1 = PWM(0) #Both buzzers for temperature and humidity
buzzer2 = PWM(14)
buzzer1.freq(500)
buzzer2.freq(600)
sensor = DHT11(Pin(15, Pin.IN, Pin.PULL_UP)) #temperature and humidity sensor pin
r1 = Pin(18,Pin.OUT) #First rgb light Pin setup
g1 = Pin(17,Pin.OUT)
b1 = Pin(16,Pin.OUT)
r2 = Pin(21,Pin.OUT) #Second rgb light Pin setup
g2 = Pin(20,Pin.OUT)
b2 = Pin(19,Pin.OUT)

r1.value(1)
g1.value(1)
b1.value(1)
r2.value(0)
g2.value(0)
b2.value(0)

def timer1():
    """Starts a timer using time.tick_ms. This code is taken and edited from 3.5 of the Raspberry Pi Pico tutorials."""
    global start1
    start1 = utime.ticks_ms()

def checktimer1():
    """Calculates the time, checking what time the timer has reached since it has started. Again, code is 
    taken and edited from 3.5 of the Raspberry Pi Pico tutorials"""
    finish1 = utime.ticks_ms() - start1
    return finish1

def disablebuzzer1():
    """Acts as a timer function to disable the buzzer. This starts the buzzer."""
    global disable1
    disable1 = utime.ticks_ms()

def checkbuzzer1():
    """Used whenever the buzzer is supposed to turn on. Checks if 10 minutes is up to allow the buzzer to turn on."""
    try:
        current_time1 = utime.ticks_ms() - disable1
        if current_time1 < 600000:
            return False
        else:
            return True
    except:
        return True
    
def timer2():
    """Starts a timer using time.tick_ms. This code is taken and edited from 3.5 of the Raspberry Pi Pico tutorials."""
    global start2
    start2 = utime.ticks_ms()

def checktimer2():
    """Calculates the time, checking what time the timer has reached since it has started. Again, code is 
    taken and edited from 3.5 of the Raspberry Pi Pico tutorials"""
    finish2 = utime.ticks_ms() - start2
    return finish2

def disablebuzzer2():
    """Acts as a timer function to disable the buzzer. This starts the buzzer."""
    global disable2
    disable2 = utime.ticks_ms()

def checkbuzzer2():
    """Used whenever the buzzer is supposed to turn on. Checks if 10 minutes is up to allow the buzzer to turn on."""
    try:
        current_time2 = utime.ticks_ms() - disable2
        if current_time2 < 600000:
            return False
        else:
            return True
    except:
        return True
    
def high1():
    """Used for the temperature whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound."""
    if r1.value() == 1: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r1.value(0)
        g1.value(1)
        b1.value(1)
        timer1()
    if checkbuzzer1(): #Checks if the buzzer is disabled or not
        while checktimer1() < 60000: #While the timer is at less than a minute check for sound
            if sound() == True:
                buzzer1.duty_u16(0)
                disablebuzzer1()
                r1.value(1)
                sleep(0.05)
                break
        if checkbuzzer1(): #If theres no sound, ring a buzzer that can be turned off with sound
            buzzer1.duty_u16(32768)
            while True:
                if sound() == True:
                    buzzer1.duty_u16(0)
                    disablebuzzer1()
                    r1.value(1)
                    sleep(0.05)
                    break
        else:
            buzzer1.duty_u16(0) #If the buzzer is disabled then make sure its off
    else:
        buzzer1.duty_u16(0) 
        
def high2():
    """Used for the humidity whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound."""
    if r2.value() == 0: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r2.value(1)
        g2.value(0)
        b2.value(0)
        timer2()
    if checkbuzzer2(): #Checks if the buzzer is disabled or not
        while checktimer2() < 60000: #While the timer is at less than a minute check for sound
            if sound() == True:
                buzzer2.duty_u16(0)
                disablebuzzer2()
                r2.value(0)
                sleep(0.05)
                break
        if checkbuzzer2(): #If theres no sound, ring a buzzer that can be turned off with sound
            buzzer2.duty_u16(32768)
            while True:
                if sound() == True:
                    buzzer2.duty_u16(0)
                    disablebuzzer2()
                    r2.value(0)
                    sleep(0.05)
                    break
        else:
            buzzer2.duty_u16(0) #If the buzzer is disabled then make sure its off
    else:
        buzzer2.duty_u16(0) 

                    
def low1():
    """Used for the temperature whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound."""
    if b1.value() == 1: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r1.value(1)
        g1.value(1)
        b1.value(0)
        timer1()
    if checkbuzzer1(): #Checks if the buzzer is disabled or not
        while checktimer1() < 60000: #While the timer is at less than a minute check for sound
            if sound() == True:
                buzzer1.duty_u16(0)
                disablebuzzer1()
                b1.value(1)
                sleep(0.05)
                break
        if checkbuzzer1(): #If theres no sound, ring a buzzer that can be turned off with sound
            buzzer1.duty_u16(32768)
            while True:
                if sound() == True:
                    buzzer1.duty_u16(0)
                    disablebuzzer1()
                    b1.value(1)
                    sleep(0.05)
                    break
        else:
            buzzer1.duty_u16(0) #If the buzzer is disabled then make sure its off
    else:
        buzzer1.duty_u16(0) 
        

def low2():
    """Used for the humidity whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound."""
    if b2.value() == 0: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r2.value(0)
        g2.value(0)
        b2.value(1)
        timer2()
    if checkbuzzer2(): #Checks if the buzzer is disabled or not
        while checktimer2() < 60000: #While the timer is at less than a minute check for sound
            if sound() == True:
                buzzer2.duty_u16(0)
                disablebuzzer2()
                b2.value(0)
                sleep(0.05)
                break
        if checkbuzzer2(): #If theres no sound, ring a buzzer that can be turned off with sound
            buzzer2.duty_u16(32768)
            while True:
                if sound() == True:
                    buzzer2.duty_u16(0)
                    disablebuzzer2()
                    b2.value(0)
                    sleep(0.05)
                    break
        else:
            buzzer2.duty_u16(0) #If the buzzer is disabled then make sure its off
    else:
        buzzer2.duty_u16(0) 

def optimal1():
    r1.value(1)
    g1.value(0)
    b1.value(1)
    buzzer1.duty_u16(0)

def optimal2():
    r2.value(0)
    g2.value(1)
    b2.value(0)
    buzzer2.duty_u16(0)

def warning1():
    r1.value(0)
    g1.value(0)
    b1.value(1)
    buzzer1.duty_u16(0)

def warning2():
    r2.value(1)
    g2.value(1)
    b2.value(0)

def sound():
    if soundsensor.value() == 1:
        return True
    if soundsensor.value() == 0:
        return False

def main():
    while True:
        #sensor.measure()
        #temp = sensor.temperature()
        #wet = sensor.humidity()
        temp = 16
        wet = 16
        print(temp)
        print(wet)
        if temp > 21:
            high1()
        elif temp == 21 or temp == 16:
            warning1()
        elif temp > 16 and temp < 21:
            optimal1()
        elif temp < 16:
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

main()







