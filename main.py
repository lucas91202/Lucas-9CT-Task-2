import utime #For the Raspberry Pico Pi timer
from machine import Pin, PWM, Timer #For the Raspberry Pico Pi
from time import sleep #For pausing code
from dht import DHT11 #For temperature and humidity sensor
soundsensor = Pin(22,Pin.IN, Pin.PULL_UP) #Sound sensor
buzzer1 = PWM(0) #Both buzzers for temperature and humidity
buzzer2 = PWM(14)
buzzer1.freq(500) #Frequency of both buzzers
buzzer2.freq(750)
sensor = DHT11(Pin(15, Pin.IN, Pin.PULL_UP)) #temperature and humidity sensor pin
r1 = Pin(18,Pin.OUT) #First rgb light Pin setup
g1 = Pin(17,Pin.OUT)
b1 = Pin(16,Pin.OUT)
r2 = Pin(21,Pin.OUT) #Second rgb light Pin setup
g2 = Pin(20,Pin.OUT)
b2 = Pin(19,Pin.OUT)

r1.value(1) #Turn all lights off. Note that rgb1 uses opposite values for lighting, so 1 is off and 0 is on. Rgb2 uses 0 as off and 1 as on.
g1.value(1)
b1.value(1)
r2.value(0)
g2.value(0)
b2.value(0)

def timer1():
    """Starts a timer using time.tick_ms for temperature. This code is taken and edited from 3.5 of the Raspberry Pi Pico tutorials."""
    global start1
    start1 = utime.ticks_ms() #Starts a timer

def checktimer1():
    """Calculates the time, checking what time the timer has reached since it has started. Used for temperature. Code is 
    taken and edited from 3.5 of the Raspberry Pi Pico tutorials"""
    finish1 = utime.ticks_ms() - start1 #Calculates how long it has been since the timer has been started
    return finish1

def disablebuzzer1():
    """Acts as a timer function to disable the buzzer for a certain amount of time. Used for temperature and does NOT turn the buzzer off. Code borrowed from 3.5 of Raspberry Pi Pico Tutorials."""
    global disable1
    disable1 = utime.ticks_ms() #Starts a timer

def checkbuzzer1():
    """Used whenever the buzzer is supposed to turn on. Checks if 10 minutes is up before allowing the buzzer to turn on. Used for temperature. Code borrowed from 3.5 of Raspberry Pi Pico Tutorials."""
    try:
        current_time1 = utime.ticks_ms() - disable1 #Calculates how long it has been since the timer has started
        if current_time1 < 600000: #Checks if it has been 10 minutes to determine if the buzzer can be turned on again
            return False
        else:
            return True
    except: #Used for the first time running code and the buzzer hasn't been disabled yet.
        return True # Allows the buzzer to turn on.
    
def timer2(): #Same as timer, for humidity
    """Starts a timer using time.tick_ms for humidity. This code is taken and edited from 3.5 of the Raspberry Pi Pico tutorials."""
    global start2
    start2 = utime.ticks_ms()

def checktimer2(): #For humidity
    """Calculates the time, checking what time the timer has reached since it has started. To be used with humidity. Code is 
    taken and edited from 3.5 of the Raspberry Pi Pico tutorials"""
    finish2 = utime.ticks_ms() - start2
    return finish2

def disablebuzzer2(): #For humidity
    """Acts as a timer function to disable the buzzer for a certain amount of time. Used for humidity and does NOT turn the buzzer off. Code borrowed from 3.5 of Raspberry Pi Pico Tutorials."""
    global disable2
    disable2 = utime.ticks_ms()

def checkbuzzer2(): #For humidity
    """Used whenever the buzzer is supposed to turn on. Checks if 10 minutes is up before allowing the buzzer to turn on. Used for humidity. Code borrowed from 3.5 of Raspberry Pi Pico tutorials."""
    try:
        current_time2 = utime.ticks_ms() - disable2
        if current_time2 < 600000:
            return False
        else:
            return True
    except:
        return True
    
def high1():
    """Used for the temperature whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound detected. Code for buzzer adapted from https://randomnerdtutorials.com/raspberry-pi-pico-pwm-micropython/"""
    if r1.value() == 1: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r1.value(0)
        g1.value(1)
        b1.value(1)
        timer1() #Start the timer
    if sound() == True: #Checks for sound, if sound is detected it disables the buzzer
        buzzer1.duty_u16(0)
        disablebuzzer1()
        r1.value(1) #Used to ensure the timer can start again, without this the timer does not reset.
    else:
        if checkbuzzer1(): #If buzzer is available
            if checktimer1() > 60000: #Check if a minute has passed to turn on the buzzer
                buzzer1.duty_u16(32768)
            else:
                buzzer1.duty_u16(0) #If the buzzer is disabled then make sure its off
        else:
            buzzer1.duty_u16(0) #Buzzer is unavailable
        
def high2():
    """Used for the humidity whenever it goes too high. Turns on a red LED and a buzzer a minute later if there is no sound. Code for buzzer adapted from https://randomnerdtutorials.com/raspberry-pi-pico-pwm-micropython/"""
    if r2.value() == 0: #This is done to ensure the timer is enabled once, only when the red light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r2.value(1)
        g2.value(0)
        b2.value(0)
        timer2() #Start timer
    if sound() == True:
        buzzer2.duty_u16(0)
        disablebuzzer2()
        r2.value(0)
    else:
        if checkbuzzer2(): #If buzzer is available
            if checktimer2() > 60000: #Check if a minute has passed to turn on the buzzer
                buzzer2.duty_u16(32768)
            else:
                buzzer2.duty_u16(0) #If the buzzer is disabled then make sure its off
        else:
            buzzer2.duty_u16(0) #Buzzer unavailable

def low1():
    """Used for the temperature whenever it goes too low. Turns on a blue LED and a buzzer a minute later if there is no sound. Code for buzzer adapted from https://randomnerdtutorials.com/raspberry-pi-pico-pwm-micropython/"""
    if b1.value() == 1: #This is done to ensure the timer is enabled once, only when the blue light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r1.value(1)
        g1.value(1)
        b1.value(0)
        timer1() #Start timer
    if sound() == True:
        buzzer1.duty_u16(0)
        disablebuzzer1()
        r1.value(1)
    else:
        if checkbuzzer1(): #If theres no sound, ring a buzzer that can be turned off with sound
            if checktimer1() > 60000: #Check if a minute has passed to turn on the buzzer
                buzzer1.duty_u16(32768)
            else:
                buzzer1.duty_u16(0) #If the buzzer is disabled then make sure its off
        else:
            buzzer1.duty_u16(0) #Buzzer unavailable
        
def low2():
    """Used for the humidity whenever it goes too low. Turns on a red LED and a buzzer a minute later if there is no sound. Code for buzzer adapted from https://randomnerdtutorials.com/raspberry-pi-pico-pwm-micropython/"""
    if b2.value() == 0: #This is done to ensure the timer is enabled once, only when the blue light first turns on. This code was done with AI as I could not figure out why the timer was never able to reach 1 minute.
        r2.value(0)
        g2.value(0)
        b2.value(1)
        timer2() #Start timer
    if sound() == True:
        buzzer2.duty_u16(0)
        disablebuzzer2()
        b2.value(0)
    else:
        if checkbuzzer2(): #If theres no sound, ring a buzzer that can be turned off with sound
            if checktimer2() > 60000:
                buzzer2.duty_u16(32768)
            else:
                buzzer2.duty_u16(0) #If the buzzer is disabled then make sure its off
        else:
            buzzer2.duty_u16(0)

def optimal1():
    """Used when temperature is in the optimal range. Turning buzzer off using PWM found also from 2.7 of Raspberry Pi Pico Tutorials."""
    r1.value(1) #Green light on
    g1.value(0)
    b1.value(1)
    buzzer1.duty_u16(0)

def optimal2():
    """Used when humidity is in optimal range. Turning buzzer off also found from 2.7, Raspberry Pi Pico Tutorials."""
    r2.value(0) #Green light on
    g2.value(1)
    b2.value(0)
    buzzer2.duty_u16(0)

def warning1():
    """Used when the temperature is close to exiting the optimal range. Buzzer off from 2.7 of Raspberry Pi Pico Tutorials."""
    r1.value(0) #Yellow light on
    g1.value(0)
    b1.value(1)
    buzzer1.duty_u16(0)

def warning2():
    """Used when the humidity is close to leaving the optimal range. Buzzer is turned off by PWM, code adapted from 2.7 Raspberry Pi Pico Tutorials and https://randomnerdtutorials.com/raspberry-pi-pico-pwm-micropython/"""
    r2.value(1) #Yellow light on
    g2.value(1)
    b2.value(0)
    buzzer1.duty_u16(0)

def sound():
    """Used to detect sound and return if sound is detected or not. Code and sound sensor setup borrowed from https://sensorkit.joy-it.net/en/sensors/ky-038"""
    if soundsensor.value() == 1: #If sound is detected
        return True
    if soundsensor.value() == 0: #If there is no sound
        return False

def tempwet(timer):
    """Used to give values for temperature and humidity. Code and sensor setup borrowed from https://sensorkit.joy-it.net/en/sensors/ky-015. Timer code used with temperature and humidity below borrowed from https://randomnerdtutorials.com/raspberry-pi-pico-interrupts-micropython/#blink-led-with-timer"""
    global temp, wet #Allow use for temp and wet variables through the whole project
    sensor.measure()
    temp = 99#sensor.temperature()
    wet = 1000#sensor.humidity()
    print(f'Temperature: {temp}\nHumidity: {wet}')

tempwet(0) #Define the variables at the start of the project. 0 is used as a placeholder to prevent the code from failing.
checktw = Timer()
checktw.init(mode=Timer.PERIODIC, period=2000, callback=tempwet) #Run the tempwet function every two seconds.

def main():
    """Used to run the program."""
    while True:
        if temp > 21: #If temperature is too high
            high1()
        elif temp == 21 or temp == 16: #If temperature is close to being too high
            warning1()
        elif temp > 16 and temp < 21: #If temperature is in optimal range
            optimal1()
        else: #If temperature is too low
            low1()

        if wet > 60: #Checks if humidity is too high
            high2()
        elif wet >= 51 and wet <= 60 or wet >= 30 and wet <= 34: #Checks if humidity is close to being too high
            warning2()
        elif wet >= 35 and wet <= 50: #Checks if humidity is in optimal range
            optimal2()
        else: #If humidity is in the low range
            low2() 
        
if __name__ == "__main__":
    main()