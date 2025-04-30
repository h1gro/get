import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

comp   = 14
troyka = 13
#dac    = [26, 19, 13, 6, 5, 11, 9, 10]
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]

GPIO.setup(dac, GPIO.OUT)
#GPIO.setup(leds, GPIO.OUT)
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

    count = 0
    for i in range(7, -1, -1):

        count += 2**i
        dac_val = my_bin(i)
        GPIO.setup(dac, GPIO.OUT)
        GPIO.output(dac, dac_val)

        val = GPIO.input(comp)

        #sleep(0.011)
        
        if val == 0:
            count -= 2**i

    return count

def Vol(number):
    
    number = int(number / 256 * 10)

    bit_mask = [0] * 8

    for i in range(number - 1):
        bit_mask[i] = 1
    
    return bit_mask

try:
    while True:
        
        adc_return = adc()

        if (adc_return):

            volume = Vol(adc_return)
            GPIO.setup(leds, GPIO.OUT)
            GPIO.output(leds, volume)
            print("{:.3f}".format(adc_return * 3.3 / 256.0))

finally:

    GPIO.output(dac, 0)
    GPIO.cleanup()