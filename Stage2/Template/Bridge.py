import RPi.GPIO as GPIO
import time

#HBridge Class
class HBridge:
    #Init or Constructor to instantiate an object of type Motor
    def __init__(self,EnablePin):
        self.__EnablePin = EnablePin #HBridge Enable Pin
        #Setting up the HBridge Enable Pin
        GPIO.setup(self.__EnablePin,GPIO.OUT)
    
    #Method to Enable the H Bridge    
    def EnableBridge(self):
        #Enabling the H-Bridge
        GPIO.output(self.__EnablePin,GPIO.HIGH)
        
    #Method to Disable the H Bridge    
    def DisableBridge(self):
        #Enabling the H-Bridge
        GPIO.output(self.__EnablePin,GPIO.LOW)