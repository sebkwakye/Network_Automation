print("Problem 4: Rock-Paper-Scissors Game")
'''
Task: Create a two-player Rock-Paper-Scissors game.
Hints:
Use input() to get choices from both players.
Implement a function to determine the winner based on the game rules.
Use if statements to cover all possible scenarios.
Consider using a loop to allow the players to play multiple rounds.
Example Logic:
Compare the choices.
Declare the winner.
Ask if they want to play again.
'''
print("Solutions to Problem 4")

import sys     # System-specific parameters and functions

# Function to determine the winner
def determine_winner(player1, player2):
    if player1 == player2:
        return "It's a tie!"

    # Define winning combinations
    winning_combinations = {("rock", "scissors"), ("scissors", "paper"), ("paper", "rock")}

    # Check winner
    if (player1, player2) in winning_combinations:
        return "Player 1 wins!"
    elif player1 == player2:
        return "It's a tie!"
    else:
        return "Player 2 wins!"


# Main game loop
while True:
    print("\nRock-Paper-Scissors Game!")

    # Get choices from players
    player1 = input("Player 1, enter rock, paper, or scissors: ").strip().lower()
    player2 = input("Player 2, enter rock, paper, or scissors: ").strip().lower()

    # Validate input
    valid_choices = ["rock", "paper", "scissors"]
    if player1 not in valid_choices or player2 not in valid_choices:
        print("Invalid input! Please enter rock, paper, or scissors.")
        continue  # Restart the loop

    # Determine the winner
    result = determine_winner(player1, player2)
    print("\nResult:", result)

    # Ask if they want to play again
    play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
    if play_again != "yes":
        print("Thanks for playing! Goodbye!")
        sys.exit()  # Exit the program

