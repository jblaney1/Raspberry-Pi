import RPi.GPIO as GPIO
import time

#Motor Class 
class Motor:
    FORWARD = True #Static or Class attribute for Forward Rotation
    BACKWARD = False #Static or Class attribute for Backward Rotation
    #Init or Constructor to instantiate an object of type Motor
    def __init__(self,Name,Forward,Backward):
        self.__MotorName = Name #Name of the motor
        #self.__EnablePin = EnablePin #HBridge Enable Pin
        self.__Frequency = 500 #Pulse Width Modulation Frequency
        self.__dc = 0.0 #Default Duty Cycle
        self.__RotationDir =  Motor.FORWARD #Default rotation in the Forward Direction
        
        #Setting up the HBridge Enable Pin
        #GPIO.setup(self.__EnablePin,GPIO.OUT)
        
        #Setting up the Forward and Backward Pins as output pins
        GPIO.setup(Forward,GPIO.OUT)
        GPIO.setup(Backward,GPIO.OUT)
        
        #Setting up the PWM operations on forward and backward GPIO pins
        self.__ForwardPin = GPIO.PWM(Forward,self.__Frequency)
        self.__BackwardPin = GPIO.PWM(Backward,self.__Frequency)
        
        #Start PWM using the default Duty Cycle
        self.__ForwardPin.start(self.__dc)
        self.__BackwardPin.start(self.__dc)
    
    #Method to run or start the motor
    def Run(self):
        #Enabling the H-Bridge
        #GPIO.output(self.__EnablePin,GPIO.HIGH)
        #Running the motor in the desired direction
        if self.__RotationDir: #Forward Direction
            print("Forward Direction at Speed of ",self.__dc)
            self.__BackwardPin.ChangeDutyCycle(0.0)
            self.__ForwardPin.ChangeDutyCycle(self.__dc)
        else: #Backward Direction
            print("Backward Direction at Speed of ",self.__dc)
            self.__ForwardPin.ChangeDutyCycle(0.0)
            self.__BackwardPin.ChangeDutyCycle(self.__dc)
    
    #Getter Function for the rotation direction of Motor
    @property #Directive property indicates the Direction is a property method
    def Direction(self):
        #Return the current direction of the motor
        return self.__RotationDir
    
    #Setter function for the rotation direction of Motor
    @Direction.setter
    def Direction(self,value):
        #Set the direction of the motor
        self.__RotationDir = value
        
    #Getter function of the Speed of the motor
    @property #Directive property indicates the Speed is a property method
    def Speed(self):
        #Return the current duty cycle of the motor
        return self.__dc
    
    #Setter function of the Speed of the motor
    @Speed.setter
    def Speed(self,value):
        #Checking for a valid duty cycle value
        if value <= 100.00 and value > 20.0:
            self.__dc = value
        else:
            self.__dc = 20.0
    
    #Method to stop the motor
    def Stop(self):
        #Reducing the Speed of the motor to zero
        self.__ForwardPin.ChangeDutyCycle(0.0)
        self.__BackwardPin.ChangeDutyCycle(0.0)
        