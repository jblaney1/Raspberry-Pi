""" Joshua Blaney
Design Experience with Devices
Homework 2
Nov 6, 2018"""

"""A Python program to determine whether a list of ten random integers
has even numbers or odd numbers and is divisible by the integer 5"""

import random #A Python module to generate random numbers
import math #A Python module of math library functions

"""Math operator to be used in this code
% is the modulus operator and the variable z will contain the remainder of x divided by y.
z = x%y"""
"""Logic Operators that can be used in this code
!= or is not
== equal to """

#The Function to Generate "size" number of random integers
def GenerateRandomIntegers(data,size):
    random.seed()
    randMin = 1
    randMax = 100
    for i in range (size):
        RandomSample = random.randint(randMin,randMax)
        data.append(RandomSample)
        
#The function to display the integers stored in the list "data"
def PrintIntegers(data):
    print("Randomly Generated Ten Integers")
    print(data)
    
if __name__ == '__main__':
    #Desired size of a list
    VectorSize = 10
    #A empty list to pepulate with "VectorSize" number of random integers
    Vector = []
    
    """Write a single line of code below to call the function GenerateRadomIntegers to populate
    the empty list "Vector" with VectorSize number of random integers:"""
    
    GenerateRandomIntegers(Vector,VectorSize)
    
    """Write a single line of code to call the function PrintIntegers
    to display the randomly generated integers of size VectorSize:"""
    
    PrintIntegers(Vector)
    
    #Code to determine even or odd and divisible by 5
    for i in range(VectorSize):
            """Using an if and else statements with the modulus operator %
            determine whether a number in the Vector is even or odd and print the appropriate statement:"""
            
            if(Vector[i] % 2) == 0:
                print('{:d} is an even number' .format(Vector[i]))
            else:
                print('{:d} is an odd number' .format(Vector[i]))
            
            
            """Using only an if statement with modulus operator %
            determine whether a number in the Vector is also divisible by the integer 5
            and print the appropriate statement:"""
            
            if(Vector[i] % 5) == 0:
                print('{:d} is also divisible by 5' .format(Vector[i]))
            
    input("Press any key to exit the program")
