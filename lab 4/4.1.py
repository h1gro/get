import RPi.GPIO as GPIO

GPIO.setwarnings(False)

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

try:
    while (True):

        number = input("write 0 to 255:")
        
        is_int = isinstance(number, int)

        try:
            number = int(number)
            number_i = [0 for i in range(8)]
            bin_num = bin(number)

            i = -1
            while bin_num[i] != 'b':
                number_i[i] = int(bin_num[i])
                i -= 1

            if (0 <= number <= 255):
                volt = float(number) / 256 * 3.3
                print(f"voltage = {volt:.4} volt")

            else:

                if (number < 0):
                    print("error! <0")

                elif (number > 255):
                    print("error! >255")  

        except Exception:
            
            is_int = isinstance(number, float)

            if (not is_int):
                
                print("error! float")

            else:
                print("error! not number")

            if number == "q": break

            

finally:

    GPIO.output(dac, 0)
    GPIO.cleanup()
