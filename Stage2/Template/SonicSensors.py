import RPi.GPIO as GPIO
import time

#Ultrasonic Sensor Class
class UltraSonicSensor:
    def __init__(self,trig_pin,echo_pin):
        self.__trigger = trig_pin
        self.__echo = echo_pin
        GPIO.setup(self.__trigger,GPIO.OUT)
        GPIO.setup(self.__echo,GPIO.IN)
    
    #Method to send the trigger
    def SendTrigger(self):
        GPIO.output(self.__trigger,True)
        time.sleep(0.00001)
        GPIO.output(self.__trigger,False)
    
    #Method to receive the reflected sound and measure elapsed time
    def WaitForEcho(self):
        start = time.time()
        stop = time.time()
        while GPIO.input(self.__echo) == False:
            start = time.time()
        while GPIO.input(self.__echo) == True:
            stop = time.time()
        distance_cm = ((stop - start)*34300.0)/2.0
        return distance_cm
