import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

flag     = 1
time     = 0 
x        = 0

def dec2bin(number):

    number = int(number)
    number_i = [0 for i in range(8)]
    bin_num = bin(number)

    i = -1
    while bin_num[i] != 'b':
        number_i[i] = int(bin_num[i])
        i -= 1

    return number_i

try:
    period = float(input("Type a period for sygnal: "))

    while True:

        GPIO.output(dac, dec2bin(x))

        if x == 0:    
            flag = 1
        elif x == 255:  
            flag = 0

        if flag == 1:
            x += 1 

        else:
            x -= 1

        sleep(period/512)
        time += 1

except ValueError:
    print("Inapropriate period!")

finally:

    GPIO.output(dac, 0)
    GPIO.cleanup()