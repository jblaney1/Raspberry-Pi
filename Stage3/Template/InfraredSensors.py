import RPi.GPIO as GPIO
import time

class TrackSensor:
    def __init__(self,SensorPin):
        self.__TrackPin = SensorPin
        GPIO.setup(self.__TrackPin,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    
    #Method to detect the track  
    def DetectTrack(self):
        if GPIO.input(self.__TrackPin) == GPIO.HIGH:
            return True
        else:
            return False
        
