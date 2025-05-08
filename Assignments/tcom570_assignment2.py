print("Problem 1: Complex Number Operations")
'''
The Problem:
You need to create a Complex class that can store a complex number (with real and imaginary parts)
The class should implement operations: addition, subtraction, multiplication, division, and modulus
Results should be formatted with 2 decimal places
'''

import math

class Complex:
    def __init__(self, real, imag):
        # Initialize the complex number with real and imaginary parts
        self.real = real
        self.imag = imag

    def __add__(self, other):
        # Add two complex numbers
        return Complex(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        # Subtract two complex numbers
        return Complex(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        # Multiply two complex numbers using (a+bi)(c+di) = (ac - bd) + (ad + bc)i
        r = self.real * other.real - self.imag * other.imag
        i = self.real * other.imag + self.imag * other.real
        return Complex(r, i)

    def __truediv__(self, other):
        # Divide two complex numbers using the formula:
        # [(a*c + b*d) + (b*c - a*d)i] / (c^2 + d^2)
        denom = other.real**2 + other.imag**2
        # Division by zero, case where denominator == 0
        r = (self.real * other.real + self.imag * other.imag) / denom
        i = (self.imag * other.real - self.real * other.imag) / denom
        return Complex(r, i)

    def mod(self):
        # Return the modulus (absolute value) as a complex number with 0 imaginary part
        magnitude = math.sqrt(self.real**2 + self.imag**2)
        return Complex(magnitude, 0)

    def __str__(self):
        # Format the complex number as a string with two decimal places (2f)
        # To give a more readable and formatted output when printing objects.
        r = f"{self.real:.2f}"
        i = f"{abs(self.imag):.2f}"   # strip the negative sign and convert to a string with 2 decimal places
        sign = '+' if self.imag >= 0 else '-'   # sign between real and imaginary parts
        return f"{r}{sign}{i}i"

if __name__ == '__main__':
    # Read and parse two lines of input: "real imag"
    x = Complex(*map(float, input("Enter real and imaginary part of first complex number (e.g. 2 1): ").split()))
    y = Complex(*map(float, input("Enter real and imaginary part of second complex number (e.g. 5 6): ").split()))

    # Perform and print results of operations
    print(f"Addition: ", x + y)
    print(f"Subtraction: ", x - y)
    print(f"Multiplication", x * y)
    print(f"Division: ", x / y)
    print(f"Modulus of first number: ", x.mod())
    print(f"Modulus of second number: ", y.mod())



print("\nProblem 2: List Operations")
'''
The Problem:
You'll be working with a list and performing operations based on input commands
There are 7 different operations: insert, print, remove, append, sort, pop, reverse
You need to execute each command and print the list when the "print" command is given
'''
if __name__ == '__main__':
    print("Please enter all your input below:")
    print("First, enter the number of commands.")
    print("Then enter each command on a new line (e.g., append 5, insert 1 10, etc.).")
    print("---- Begin Input ----")

    try:
        N = int(input("Please enter the number of commands: "))   # Read the number of commands
    except ValueError:
        print("Invalid number of commands. Please enter an integer.")
        exit(1)

    mylist = []   # Initialize an empty list

    # Process each command
    for i in range(N):
        # Read the entire command line and split into parts
        try:
            command_line = input().strip()
            if not command_line:
                raise ValueError("Empty command line.")

            inputs = command_line.split()
            cmd = inputs[0]   # The first part is the command, eg. "insert", "print"

            if cmd == 'insert':
                if len(inputs) != 3:
                    raise ValueError("insert command requires two arguments: index and value.")
                # insert element and position; index
                index = int(inputs[1])
                element = int(inputs[2])
                mylist.insert(index, element)

            elif cmd == 'append':   # add element to the end of the list
                if len(inputs) != 2:
                    raise ValueError("append command requires one argument: value.")
                element = int(inputs[1])
                mylist.append(element)

            elif cmd == 'remove':   # remove the first occurrence of element
                if len(inputs) != 2:
                    raise ValueError("remove command requires one argument: value.")
                element = int(inputs[1])
                mylist.remove(element)

            elif cmd == 'print':   # print the current state of the list
                print(mylist)

            elif cmd == 'sort':   # sort the list in ascending order
                mylist.sort()

            elif cmd == 'pop':   # remove the last element
                if not mylist:
                    raise IndexError("Cannot pop from an empty list.")
                mylist.pop()

            elif cmd == 'reverse':   # reverse the list
                mylist.reverse()

            else:
                print(f"Unknown command: '{cmd}'")

        except ValueError as ve:
            print(f"[Error] {ve}")
        except IndexError as ie:
            print(f"[Error] {ie}")
        except Exception as e:
            print(f"[Unexpected Error] {e}")

    print("Done")