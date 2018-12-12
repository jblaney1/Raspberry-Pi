""" Joshua Blaney
Design Experience with Devices
Homework 3
Nov 6, 2018"""

#Necissary import statements for GPIO pin use and complex math
import RPi.GPIO as GPIO
from math import sqrt,pow

#Set the GPIO mode to broadcom
GPIO.setmode(GPIO.BCM)

#A class to control the LED's used in this program
class LED:
    #Default Constructor
    def __init__(self, pin):
        self.pin = pin                          #Store the pin number in the class object                                                                               
        GPIO.setup(pin, GPIO.OUT)    #Set the pin specified to output
        GPIO.output(pin,True)           #Turn on the specified pin
        
    #Simple mothod to turn the LED off
    def off(self):
        GPIO.output(self.pin,False)   #Turn off the LED
        
#A class to compute the roots of the  equation
class Quadrat:
    #Defualt Constructor
    def __init__(self,a,b,c):
        self.a = a                               #Store the value of a in the class object
        self.b = b                               #Store the value of b in the class object
        self.c = c                                #Store the value of c in the class object
        
    #A method to solve the quadratic
    def solve(self):
        #Try to solve the radicand first
        try:
            self.rad = sqrt(pow(b,2.0)-(4*a*c))
            
            #If the roots are real continure solving the quadratic
            self.i = 0
            self.x1 = (-b+ self.rad) / (2 * a)
            self.x2 = (-b - self.rad) / (2 * a)
        except ValueError:        
            #If the roots are not real find the radicand and mark the roots as complex
            self.rad = sqrt((4*a*c) - pow(b,2.0))
            self.i = 1
        
if __name__ =='__main__':
    #Setup the variables that will be used for LED pin numbers in this program
    #Change the led pin numbering if necissary
    #Done is used to signify the completion of the program
    done = False
    rled = 6
    yled = 13
    gled = 19
    
    while(done != True):      #While the user wants to compute more roots do not end the program
        #Get the value of a from the user
        a = input('What is a: ')
        a = float(a)
        
        #Get the value of b from the user
        b = input('What is b: ')
        b = float(b)
        
        #Get the vlaue of c from the user
        c = input('What is c: ')
        c = float(c)
        
        #Determine if the quadratic has any roots a > tolerance
        if a <= .356:
            #If it does not, then set the red led to on and print an apropriate statement
            flag = LED(rled)  #Flag the equation as having no roots
            #Let the user know that the funciton has no roots
            print("a is zero, thus this function has no roots\n")
            #Ask the user if they want to continue
            temp = input('Type e to exit or any other key to continue: ')  
            if (temp == 'e'):
                #End the program
                done = True;
                GPIO.cleanup()
            else:
                #turn the LED off and run again
                 flag.off()
        else:
            function = Quadrat(a,b,c)    #Setup the object for this function
            function.solve()                    #Try to solve the function 
            if(function.i == 1):               #Test to see if the function has complex roots
                flag = LED(yled)               #flag the equation as having complex roots
                
                #Output the results of the root calculations in a format that is easy to understand
                print("The complex roots of the function are as follows\n")
                print("    -{:.2f} + {:.2f}i" .format(function.b,function.rad))
                print("x = ______________\n")
                print("         {:.2f}           \n".format(2 * function.a))
                print("And\n")
                print("    -{:.2f} - {:.2f}i" .format(function.b,function.rad))
                print("x = ______________\n")
                print("         {:.2f}           \n".format(2 * function.a))
                
                #Check to see if the user wants to run the program again
                temp = input('Type e to exit or any other key to continue: ')
                if (temp == 'e'):
                    done = True;
                    GPIO.cleanup()
                else:
                    flag.off()
            else:
                #If all other conditions are false then the function has real roots
                flag = LED(gled)  #Flag the equation as having real roots
                
                #Print the results of the root calculations in a meaningful and easy to read manner
                print("The roots of the provided equation are as follows")
                print("x = {:.2f}".format(function.x1))
                print("x = {:.2f}".format(function.x2))
                
                #Check to see if the user wants to run the program again
                temp = input('Type e to exit or any other key to continue: ')
                if (temp == 'e'):
                    done = True;
                    GPIO.cleanup()
                else:
                    flag.off()     
