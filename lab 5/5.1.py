import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

comp   = 4
troyka = 17
dac    = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setup(dac, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def my_bin(number):

    number   = int(number)
    number_i = [0 for i in range(8)]
    bin_num  = bin(number)

    i = -1
    while bin_num[i] != 'b':
        number_i[i] = int(bin_num[i])
        i -= 1

    return number_i

def adc():

    for i in range(256):
        
        dac_val = my_bin(i)
        
        GPIO.output(dac, dac_val)
        
        val = GPIO.input(comp)
        
        sleep(0.02)

        if val:
            return i

    return 0

try:
    while True:

        print("{:.3f}".format(adc() * 3.3 / 256.0))

finally:

    GPIO.output(dac, 0)
    GPIO.cleanup()
