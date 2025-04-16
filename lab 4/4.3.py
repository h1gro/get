import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)

duty_cycle = GPIO.PWM(24, 1000)
duty_cycle.start(0)

try:
    while True:

        print("get val")
        val = int(input())
        duty_cycle.ChangeDutyCycle(val)
        print("indications:")
        print(3.3*val/100)

finally:

    duty_cycle.stop()
    GPIO.output(24,0)
    GPIO.cleanup()