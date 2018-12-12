"""Python Program to Control
    the Speed and Rotational Direction
    of a DC Motor using Two Push Button Switches"""

from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

#DC Motor Class
class DCMotor:
    def __init__(self,ChannelPin,ForwardPin,ReversePin,pwmFreq):
        self.__ChannelPin = ChannelPin #GPIO Pin for enabling the H-Bridge
        self.__pwmFreq = pwmFreq #Pulse Width Frequency
        self.__dc = 10 #Default Speed of the Motor
        self.__DirForward = True #Default Direction of Rotation of the Motor
        
        #Setting up the Enable Pin of the H Bridge
        GPIO.setup(self.__ChannelPin,GPIO.OUT)
        
        #Setting up Pulse Width Modulation on the Forward direction pin
        #Set the GPIO Pin for Output
        GPIO.setup(ForwardPin,GPIO.OUT) 
        #Setup PWM on the Forward Pin with the pwmFreq
        self.__ForwardPin = GPIO.PWM(ForwardPin,self.__pwmFreq)
        
        #Setting up Pulse Width Modulation on the Reverse direction pin
        GPIO.setup(ReversePin,GPIO.OUT) #Set the GPIO Pin for Output
        #Setup PWM on the Forward Pin with the pwmFreq
        self.__ReversePin = GPIO.PWM(ReversePin,self.__pwmFreq)
        
        #et up the motor with default speed in the forward direction
        self.__ForwardPin.start(self.__dc)
        self.__ReversePin.start(0)
    
    #Method for enabling the H Bridge  
    def Enable(self):
        print("Speed = ",self.__dc,"%"," Direction: Forward")
        GPIO.output(self.__ChannelPin,GPIO.HIGH)
        
    
    #Method for changing the speed of the motor in the set direction
    def ChangeSpeed(self):
        if(self.__dc == 100):
            self.__dc = 10
        else:
            self.__dc = self.__dc + 10
        if self.__DirForward:
            self.__ForwardPin.ChangeDutyCycle(self.__dc)
            print("Speed = ",self.__dc,"%"," Direction: Forward")
        else:
            self.__ReversePin.ChangeDutyCycle(self.__dc)
            print("Speed = ",self.__dc,"%"," Direction: Reverse")
        
    #Method for changing the direction of rotation
    def ChangeRotDirection(self):
        if self.__DirForward:
            self.__DirForward = False
            self.__ForwardPin.ChangeDutyCycle(0)
            self.__ReversePin.ChangeDutyCycle(self.__dc)
            print("Speed = ",self.__dc,"%"," Direction: Reverse")
        else:
            self.__DirForward = True
            self.__ReversePin.ChangeDutyCycle(0)
            self.__ForwardPin.ChangeDutyCycle(self.__dc)
            print("Speed = ",self.__dc,"%"," Direction: Forward")
    
    #Method for reducing the motor speed to zero and disable the H-Bridge
    def Disable(self):
        self.__ForwardPin.ChangeDutyCycle(0)
        self.__ReversePin.ChangeDutyCycle(0)
        GPIO.output(self.__ChannelPin,GPIO.LOW)
        print("Resetting GPIO Pins")
        GPIO.cleanup()
        
#Class Pushbutton to create Pushbutton Objects
class PushButton:
    def __init__(self,pin,pull,motor):
        self.__gpio = pin #GPIO Pin connected to the Push Button
        self.__PullState = pull #Pull-down or Pull-up state
        #Set the attribute __Motor to the motor object which is operated by the push button instance
        self.__Motor = motor 
        """Write code to setup the GPIO pin connected to the PushButton as an input pin
        with pull_up_down set to either pull down or up using the attribute __PullState"""
        GPIO.setup(self.__gpio,GPIO.IN,pull_up_down = self.__PullState)
    
    #Method to setup the Speed Button Callback Interrupt or Event
    def SetupSpeedCallback(self):
        """Write code to setup for the Pi OS to detect an event of type rising edge on
            the gpio pin of the Speed Button and assign the Method: SpeedButton as the
            callback function with a bounce time of 400 msecs"""
        GPIO.add_event_detect(self.gpio,GPIO.RISING,callback = SpeedButton(),bouncetime = 400)
    
    #The callback method for the Speed Button
    def SpeedButton(self,channel):
        #Write code to call the Method: ChangeSpeed on the motor object using the attribute __Motor
		self.__Motor.ChangeSpeed(1)
        
    def SetupDirectionCallback(self):
        """Write code to setup for the Pi OS to detect an event of type rising edge on
            the gpio pin of the direction button and assign the Method: Directionbutton as the
            callback function"""
        GPIO.add_event_detect(self.gpio,GPIO.RISING,callback = DirectionButton(),bouncetime = 400)
    
    #The callback method for the Direction Button
    def DirectionButton(self,channel):
        #Write code to call the Method: ChangeRotDirection on the motor object using the attribute __Motor
        self.__Motor.ChangeRotDirection()

         
if __name__ == '__main__':
    Frequency = 500 #PWM Frequency of 500 Hz for Speed Control of the Motor
    Channel = 12 #Channels 1 & 2 of the H-Bridge are enabled using GPIO12
    ForwardPin = 20 #GPIO20 is used to rotate the motor in the forward direction
    ReversePin = 21 #GPIO21 is used to rotate the motor in the reverse direction
    
    #Write code to instantiate a DC Motor Object named Motor by examining the __init__ function of the Class DCMotor
    motor = Motor(Channel,ForwardPin,ReversePin,Frequency)
    
    #Start the DC Motor by Calling the Method: Enable on the DCMotor object Motor (H Bridge Channel)
    motor.Enable()
    
    SpeedPin = 6 #The Speed Pushbutton is connected to GPIO6
    DirPin = 19 #The Direction Pushbutton is connected to GPIO19
    
    """Write code to instantiate a PushButton object named SpeedButton to abstract the Speed PushButton operation. 
        Examine the __init__ function of the Class PushButton"""
    speedButton = PushButton(SpeedPin,GPIO.PUD_DOWN,motor)
    """Write code to instantiate a PushButton object named DirButton to abstract the Direction PushButton operation. 
        Examine the __init__ function of the Class PushButton"""
    dirButton = PushButton(DirPin,GPIO.PUD_DOWN,motor)
    
    #Write code to call the Method: SetupCallback on the SpeedButton Object
    speedButton.SetupCallback()
    #Write code to call the Method: SetupCallback on the DirButton Object
    dirButton.SetupCallback()

    try:
        input("Press any key to stop")
        Motor.Disable()
    except KeyboardInterrupt:
        Motor.Disable()
    

    

    

