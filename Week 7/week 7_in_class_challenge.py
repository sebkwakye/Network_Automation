'''
Python program to implement a simple "Guess the Number" game.
In this game, the program selects a random number within a specified range (such as 0-100),
and the user attempts to guess the number.
After each guess, the program will indicate whether the guess is too high, too low, or correct.
'''

import random   # for random number generation

def guess_the_number():
    # Generate a random number between 1 and 100
    generated_number = random.randint(1, 100)

    print("Welcome to the Guess the Number game!")
    print("I have selected a number between 1 and 100. Try to guess it!")

    tries = 0

    while True:
        try:
            # User input
            user_guess = int(input("Enter your guess: "))

            tries += 1

            # Check the guess
            if user_guess < generated_number:
                print("Too low! Try again.")
            elif user_guess > generated_number:
                print("Too high! Try again.")
            else:
                print(f"Correct! You guessed the number {generated_number} rightly at {tries} tries.")
                break  # Exit the loop when guessed correctly

        except ValueError:
            print("Invalid input! Please enter a valid number.")


# Run the game
guess_the_number()
