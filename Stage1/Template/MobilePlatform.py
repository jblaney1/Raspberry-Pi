import RPi.GPIO as GPIO
import time
from Bridge import HBridge
from RotationDevices import Motor

#Class MobilePlatform to create a tank Object
class MobilePlatform:
    def __init__(self,H_Bridge,L_Motor,R_Motor):
        self.__HBridge = H_Bridge #HBridge Object of the Tank Object.
        
        #Left Motor Object of the Tank Object
        self.__LeftMotor = L_Motor
        
        #Right Motor Object of the Tank Object
        self.__RightMotor = R_Motor
        
        #Turn Operation Sleep Time
        self.__TurnSleep = 1
    
    #Method to Enable the H Bridge - Turning on the Tank
    def On(self):
        self.__HBridge.EnableBridge()
    
    #Method to Disable the H Bridge - Turning off the Tank   
    def Off(self):
        self.__HBridge.DisableBridge()
        
    #Method for moving the mobile platform forward by enabling the H Bridge  
    def Drive(self):
        DesiredSpeed = float(input("Enter the driving speed as a percentage of full speed: "))
        """Set both the motors to rotate in the forward direction
            using the property Direction on the left and right motor objects
            of the Tank Object"""
        self.__LeftMotor.Direction = Motor.FORWARD
        self.__RightMotor.Direction = Motor.FORWARD
        """Set the speed of both the motors using the property Speed
            on the left and right motor objects
            of the Tank Object"""
        self.__LeftMotor.Speed = DesiredSpeed
        self.__RightMotor.Speed = DesiredSpeed
        """Start both the motors by calling the Run method  on both
            the motor objects of the Tank Object"""
        self.__LeftMotor.Run()
        self.__RightMotor.Run()
        
    
    #Method for moving the mobile platform reverse by enabling the H Bridge  
    def Reverse(self):
        DesiredSpeed = float(input("Enter the reverse speed as a percentage of full speed: "))
        print("Moving Reverse")
        #Write code to reverse the direction of the travel of the tank
        self.__LeftMotor.Direction = Motor.BACKWARD   #Set the direction of the left motor to backwards
        self.__RightMotor.Direction = Motor.BACKWARD #Set the direction of the right motor to backwards
        self.__LeftMotor.Speed = DesiredSpeed             #Set the speed the left motor should turn at
        self.__RightMotor.Speed = DesiredSpeed           #Set the speed of the right motor to match the left motor
        self.__LeftMotor.Run()                                          #Have the left motor run with the new parameters
        self.__RightMotor.Run()                                        #Have the right motor run with the new parameters
        
        
    #Method for stopping the mobile platform by disabling the H Bridge 
    def Stop(self):
        """Stop both the motors by calling the Stop method  on both
            the motor objects of the Tank Object"""
        self.__LeftMotor.Stop()
        self.__RightMotor.Stop()
    
    """Method to accelerate or decelerate the mobile platform in the
        forward or Reverse direction."""
    def ChangeSpeed(self):
        SpeedInc = float(input("Enter increase or decrease (Negative) in speed(%): "))
        print("Changing Speed")
        """Write code to increase or decrease the speed from the current speed.
            1. First, using the property Speed obtain the current speed
            2. You should add the current speed to the increase or decrease speed increment variable SpeedInc 
            3. Set the new speed for both the motors using the property Speed
            4. Call the run method on both the motors to rotate at the new speed"""
        self.__LeftMotor.Speed = self.__LeftMotor.Speed + SpeedInc       #Set the speed of the left motor to itself plus the speed change variable
        self.__RightMotor.Speed = self.__RightMotor.Speed + SpeedInc   #Set the speed of the right motor to itself plus the speed change variable
        self.__LeftMotor.Run()                                                                      #Have the left motor run with the new parameters
        self.__RightMotor.Run()                                                                    #Have the right motor run with the new parameters
        
    def TurnLeft(self):
        print("Turning Left")
        #Write code to turn the tank approximately left by 90 degrees"
        LeftDir = self.__LeftMotor.Direction                    #Store the current direction of the left motor
        RightDir = self.__RightMotor.Direction                #Store the current direction of the right motor
        LeftSpeed = self.__LeftMotor.Speed                  #Store the current speed of the left motor
        RightSpeed = self.__RightMotor.Speed              #Store the current speed of the right motor
        self.__LeftMotor.Direction = Motor.BACKWARD  #Change the left motors direction to backward
        self.__RightMotor.Direction = Motor.FORWARD  #Change the right motors direction to forward
        self.__LeftMotor.Speed = 75.0                           #Set the speed of the left motor to 75
        self.__RightMotor.Speed = 75.0                         #Set the speed of the right motor to 75
        self.__LeftMotor.Run()                                         #Run the left motor with the new parameters
        self.__RightMotor.Run()                                       #Run the right motor with the new parameters
        time.sleep(self.__TurnSleep)                              #Sleep so that the tank will turn
        self.__LeftMotor.Direction = LeftDir                    #Reset the left motors direction to its previous value
        self.__RightMotor.Direction = RightDir                #Reset the right motors direction to its previous value
        self.__LeftMotor.Speed = LeftSpeed                  #Reset the left motors speed to its previous value
        self.__RightMotor.Speed = RightSpeed              #Reset the right motors speed to its previous value
        self.__LeftMotor.Run()                                         #Run the motor with the new parameters
        self.__RightMotor.Run()                                       #Run the motor with the new parameters
        
    def TurnRight(self):
        print("Turning Right")
        #Write code to turn the tank approximately right by 90 degrees"
        LeftDir = self.__LeftMotor.Direction                    #Store the current direction of the left motor
        RightDir = self.__RightMotor.Direction                #Store the current direction of the right motor
        LeftSpeed = self.__LeftMotor.Speed                  #Store the current speed of the left motor
        RightSpeed = self.__RightMotor.Speed              #Store the current speed of the right motor
        self.__LeftMotor.Direction = Motor.FORWARD    #Change the left motors direction to backward
        self.__RightMotor.Direction = Motor.BACKWARD#Change the right motors direction to forward
        self.__LeftMotor.Speed = 75.0                           #Set the speed of the left motor to 75
        self.__RightMotor.Speed = 75.0                         #Set the speed of the right motor to 75
        self.__LeftMotor.Run()                                         #Run the left motor with the new parameters
        self.__RightMotor.Run()                                       #Run the right motor with the new parameters
        time.sleep(self.__TurnSleep)                              #Sleep so that the tank will turn
        self.__LeftMotor.Direction = LeftDir                    #Reset the left motors direction to its previous value
        self.__RightMotor.Direction = RightDir                #Reset the right motors direction to its previous value
        self.__LeftMotor.Speed = LeftSpeed                  #Reset the left motors speed to its previous value
        self.__RightMotor.Speed = RightSpeed              #Reset the right motors speed to its previous value
        self.__LeftMotor.Run()                                         #Run the motor with the new parameters
        self.__RightMotor.Run()                                       #Run the motor with the new parameters
        

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    #GPIO Pin to Enable the H-Bridge to control both the motors of the Tank
    HBEnablePin = 5 #Channels (1 & 2) and (3 & 4) of the H-Bridge are enabled using GPIO5
    
    #Right Motor Direction Control GPIO Pins
    RightMotorForwardPin = 13 #GPIO13 - Forward direction
    RightMotorBackwardPin = 26 #GPIO26 - Backward direction
    
    #Left Motor Direction Control GPIO Pins
    LeftMotorForwardPin = 16 #GPIO16 - Forward direction
    LeftMotorBackwardPin = 21 #GPIO21 - Backward direction

    """Write a single line of code to Instantiate a single H-Bridge Object of type HBridge with the reference name
        as hBridge using the HBEnablePin parameter"""
    hBridge = HBridge(HBEnablePin) #Create an object to represent the hbridge on the tank
    
    """Instantiate the Right Motor Object of type Motor with the reference name
        as RightMotor using the parameters:
            RightMotorForwardPin and RightMotorBackwardPin"""
    RightMotor = Motor("Right Motor",RightMotorForwardPin,RightMotorBackwardPin) #Create a motor object to represent the Right motor on the tank
    
    """Write a single line of code to Instantiate the Left Motor Object of type Motor with the reference name
        as LeftMotor using the parameters:
            LeftMotorForwardPin and LeftMotorBackwardPin"""
    LeftMotor = Motor("Left Motor",LeftMotorForwardPin,LeftMotorBackwardPin) #Create a motor object to represent the Left motor on the tank
    
    """Write a single line of code to Instantiate a Mobile Platform Object with the reference name Tank
        using the following parameters
        H-Bridge object
        Left Motor object
        Right Motor object"""
    Tank = MobilePlatform(hBridge,LeftMotor,RightMotor) #Create a Platform object to represent the tank with the motos and hbridge object defined earlier
    
    #Write a single line of code to turn on the Tank (Enable the H Bridge) by calling the On Method on the Tank Object
    Tank.On() #Turn the tank on so that we can drive it
    
    try:
        while(True):
            print("1 - Drive\n2 - Accelerate or Decelerate\n3 - Turn Left\n4 - Turn Right\n5 - Reverse\n6 - Stop\n7 - Exit")
            choice = int(input("Enter the integer choice: "))
            if choice == 1:
                """Start the Tank performing the by calling the Start Method
                on the MobilePlatform object"""
                Tank.Drive()
            elif choice == 2:
                """Call the Accelerate method on the on the MobilePlatform object"""
                Tank.ChangeSpeed()
            elif choice == 3:
                Tank.TurnLeft()
            elif choice == 4:
                Tank.TurnRight()
            elif choice == 5:
                Tank.Reverse()
            elif choice == 6:
                print("Stopping the Tank")
                Tank.Stop()
            else:
                print("Exiting the Program")
                Tank.Stop()
                #Turn Off the Tank (Disabling the H Bridge) by calling the Off Method
                Tank.Off()
                GPIO.cleanup()
                break
    except KeyboardInterrupt:
        Tank.Stop()
        Tank.Off()
        GPIO.cleanup()
        print("Exiting")