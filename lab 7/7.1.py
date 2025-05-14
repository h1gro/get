import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

dac  = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]

#CONSTS:
comp   = 4
troyka = 17
maxV   = 3.3 #voltage

bits = len(dac)
levels = 2 ** bits

GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)

GPIO.output(troyka, 0)

data_volts = []
data_times = []

def dectobin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

def adc():

    level = 0
    for i in range(bits - 1, -1, -1):
        level += 2**i

        GPIO.output(dac, dectobin(level))

        time.sleep(0.03)

        comp_val  = GPIO.input(comp)

        if (comp_val == 0):
            level -= 2**i

    return level

def num2_dac_leds(value):
    signal = dectobin(value)
    GPIO.output(dac, signal)
    return signal

try:
    start_time = time.time()
    val = 0

    while(val < 120):

        val = adc()

        #print("Volts = {:3}".format(val / levels * maxV))
        
        num2_dac_leds(val)
        data_volts.append(val)
        data_times.append(time.time() - start_time)

    GPIO.output(troyka, 1)

    while(val != 0):

        val = adc()

        #print("Volts = {:3}".format(val/levels * maxV))
        
        num2_dac_leds(val)
        data_volts.append(val)
        data_times.append(time.time() - start_time)

    end_time = time.time()

    with open("settings.txt", "w") as file:

        file.write(str((end_time - start_time) / (len(data_volts) + 1)))
        file.write(("\n"))
        file.write(str(maxV / 256))

    print(end_time - start_time, "Seconds\n", len(data_volts) / (end_time - start_time), "\n", maxV / 256)

finally:
    
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka, GPIO.LOW)
    GPIO.cleanup()

data_times_str = [str(item) for item in data_times]
data_volts_str = [str(item) for item in data_volts]

with open("data.txt", "w") as file:

    file.write("\n".join(data_volts_str))

plt.plot(data_times, data_volts)
plt.show()
print("End program\n")