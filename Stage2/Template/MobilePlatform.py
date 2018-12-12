from pynput import keyboard #Library for interfacing with keyboard
from time import sleep
import threading #Library for implementing thread operation
import RPi.GPIO as GPIO
import time

from Bridge import HBridge
from RotationDevices import Motor
from SonicSensors import UltraSonicSensor

#Class MobilePlatform to create a tank Object
class MobilePlatform:
    def __init__(self,H_Bridge,L_Motor,R_Motor,Dis_Sensor):
        self.__HBridge = H_Bridge #HBridge Object of the Tank Object.
        
        #Left Motor Object of the Tank Object
        self.__LeftMotor = L_Motor
        
        #Right Motor Object of the Tank Object
        self.__RightMotor = R_Motor
        
        #Obstacle Distance Sensor
        self.__ObstacleSensor = Dis_Sensor
        
        #Turn Operation Sleep Time
        self.__TurnSleep = 1
        
        #Variable to store the status of the brake
        self.__BrakeApplied = False #Default Status
        
        #Variable to enable or disable monitor for brake
        self.__CheckForObstacle = False
        
    
    #Method to Enable the H Bridge - Turning on the Tank
    def On(self):
        self.__HBridge.EnableBridge()
    
    #Method to Disable the H Bridge - Turning off the Tank   
    def Off(self):
        self.__HBridge.DisableBridge()
    
    #Method to Apply Brake
    def ApplyBrake(self):
        print("Brake Applied")
        #Write a single line of code to disable the chip driving the two motors
        self.__HBridge.DisableBridge() #If the brake is applied turn the entire bridge off
        #Write a single line of code to update the brake variable to reflect the status of the brake
        self.__BrakeApplied = True     #Update the brake variable
        
        #Code to turn the tank when an obstacle is detected
        time.sleep(5)           #Wait for a five count to show that the brake is working
        self.ReleaseBrake() #Turn the brake off
        self.TurnLeft()          #Turn the tank 90 degrees to the left
        self.TurnLeft()          #Turn the tank another 90 degrees to the left so that the tank is facing away from the object
    
    #Method to Release Brake
    def ReleaseBrake(self):
        print("Brake Released")
        #Write a single line of code to enable the chip driving the two motors
        self.__HBridge.EnableBridge() #If the brake is being turned off, turn the bridge back on
        #Write a single line of code to update the brake variable to reflect the status of the brake
        self.__BrakeApplied = False   #Update the brake status variable
    
    #Thread Method to monitor the brake    
    def MonitorBrakes(self):
        while(self.__CheckForObstacle): #Will exit when the self.__CheckForObstacle is set to False
            """Write a single line of code to call the SendTrigger method
                on the UltraSonicSensor Object created in the __init__ of class MobilePlatform"""
            self.__ObstacleSensor.SendTrigger() #Start the distance measurement task
            
            """Write a single line of code to call the WaitForEcho method on the UltraSonicSensor object
                and store the returned distance in the variable ObstacleDistance"""
            ObstacleDistance = self.__ObstacleSensor.WaitForEcho() #Record the distance measurement in a local variable
            
            """Write an if condition to check whether the returned distance is <= to 20.0 cm
                and whether the brake has not been applied."""
            if ObstacleDistance <= 20.0 and self.__BrakeApplied == False: #if the obstacle is within 20cm and the brake is not currently on do the following            
                """In the body of the if condition
                    write a print statement to display the returned distance
                    write a single line of code to call the ApplyBrake method."""
                print("The current distance to the object is {:.2f}cm".format(ObstacleDistance)) #Print the distance to the object
                self.ApplyBrake() #apply the brake

            """Write an elif condition to check whether the returned distance is > than 20.0 cm
                and whether the brake has been applied."""
            if ObstacleDistance > 20.0 and self.__BrakeApplied == True: #If the object is not within 20cm of the tank and the brake is on do the following               
                """In the body of the elif condition
                      write a print statement to display the returned distance
                      write a single line of code to call the ReleaseBrake method."""
                print("The current distance to the object is {:.2f}cm".format(ObstacleDistance)) #Print the current distance to the object
                self.ReleaseBrake() #Turn the brake off
            time.sleep(2)
        
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
        
        #Set the variable CheckForObstacle to true allowing the brake to be monitored
        self.__CheckForObstacle = True
        """Instantiate a Thread Object executing the MonitorBrakes Method
            on a separate core of the CPU. Initially the thread is not started"""
        self.__brakeThread = threading.Thread(target = self.MonitorBrakes)
        #Start the thread to monitor the brake
        self.__brakeThread.start()
        
    #Method for moving the mobile platform reverse by enabling the H Bridge  
    def Reverse(self):
        DesiredSpeed = float(input("Enter the reverse speed as a percentage of full speed: "))
        print("Moving Reverse")
        #Write code to reverse the direction of the travel of the tank. Brakes are not monitored in the reverse.
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
        """Check whether the __CheckForObstacle is set to True indicating
            the brake monitoring thread was enabled. If true, set the __CheckForObstacle
            to False and call the join method on the __brakeThread object"""
        if self.__CheckForObstacle:
            #End the thread object
            self.__CheckForObstacle = False
            self.__brakeThread.join()
    
    """Method to accelerate or decelerate the mobile platform in the
        forward or Reverse direction. The default speed increase or decrease
        is set to zero"""
    def ChangeSpeed(self):
        SpeedInc = float(input("Enter increase or decrease (Negative) in speed(%): "))
        print("Changing Speed")
        """Write code to increase or decrease the speed from the current speed.
            1. First, using the property Speed obtain the current speed
            2. You should add the current speed to the increase or decrease speed increment variable SpeedInc 
            3. Set the new speed for both the motors using the property Speed
            4. Call the run method on both the motors to rotate at the new speed"""
        self.__LeftMotor.Speed = self.__LeftMotor.Speed + SpeedInc       #Set the speed of the left motor to the current value plus the speed change variable
        self.__RightMotor.Speed = self.__RightMotor.Speed + SpeedInc   #Set the speed of the right motor to the current value plus the speed change variable
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
    
    #Method to display the keyboard choices      
    def DisplayOperations(self):
        print("Drive - d")
        print("Change Speed - c")
        print("Turn Left - ctrl")
        print("Turn Right - shift")
        print("Reverse - r")
        print("Stop - s")
        print("End Program - esc")
    
    #Method to detect escape key release
    def on_release(self,key):
        if key == keyboard.Key.esc:
            return False
    
    #Method to monitor for keyboard selection in a separate thread
    def MonitorTank(self,key):
        try:
            if key.char == 'd':
                self.Drive()
            if key.char == 'r':
                self.Reverse()
            if key.char == 'c':
                self.ChangeSpeed()
            if key.char == 's':
                self.Stop()
        except AttributeError:
            if key == keyboard.Key.ctrl:
                self.TurnLeft()
            if key == keyboard.Key.shift:
                self.TurnRight()
        self.DisplayOperations()

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
    
    #Ultrasonic Sensor Pins
    UltraSonic_TrigPin = 18 #GPIO18 - Trigger Pin of the Ultrasonic Sensor
    UltraSonic_EchoPin = 24 #GPIO24 - Echo Pin of the Ultrasonic Sensor

    """Write a single line of code to Instantiate a single H-Bridge Object of type HBridge with the reference name
        as hBridge using the HBEnablePin parameter"""
    hBridge = HBridge(HBEnablePin)  #Create an hbridge object with the enable pin defined above to represent the hbridge on the tank
    
    """Instantiate the Right Motor Object of type Motor with the reference name
        as RightMotor using the parameters:
            RightMotorForwardPin and RightMotorBackwardPin"""
    RightMotor = Motor("Right Motor",RightMotorForwardPin,RightMotorBackwardPin) #Create a motor object to represent the right motor on the tank
    
    """Write a single line of code to Instantiate the Left Motor Object of type Motor with the reference name
        as LeftMotor using the parameters:
            LeftMotorForwardPin and LeftMotorBackwardPin"""
    LeftMotor = Motor("Left Motor",LeftMotorForwardPin,LeftMotorBackwardPin)  #Create a motor object to represent the left motor on the tank
    
    """Write a single line of code to instantiate an Ultrasonic Sensor object of type UltraSonicSensor with the
        reference name DistanceSensor using the following parameters:
        UltraSonic_TrigPin
        UltraSonic_EchoPin"""
    DistanceSensor = UltraSonicSensor(UltraSonic_TrigPin,UltraSonic_EchoPin) #Create an ultrasonicsensor object to represent our distance sensor
    
    """Write a single line of code to instantiate a Mobile Platform Object with the reference name Tank
        using the following parameters
        H-Bridge object
        Left Motor object
        Right Motor object
        UltraSonicSensor object"""
    Tank = MobilePlatform(hBridge,LeftMotor,RightMotor,DistanceSensor) #Put all of our objects together to form a platform object
    
    #Write a single line of code to turn on the Tank (Enable the H Bridge) by calling the On Method on the Tank Object
    Tank.On() #Turn the tank on so that we can drive it
    
    try:
        Tank.DisplayOperations() #A Method to display the Tank Operation choices
        """Instantiating a Thread object of the type keyboard listener which will call
            Method MonitorTank when a key is pressed
            Method on_release when a key is released
            The keyboard listen thread will run until the key esc is pressed and released"""
        with keyboard.Listener(on_press = Tank.MonitorTank,on_release = Tank.on_release) as listener:
            listener.join() #A thread method to destroy the thread.
        Tank.Stop()
        #Turn Off the Tank (Disabling the H Bridge) by calling the Off Method
        Tank.Off()
        GPIO.cleanup()
    except KeyboardInterrupt:
        Tank.Stop()
        Tank.Off()
        GPIO.cleanup()
        print("Exiting")
    
    
    
    
        
        
