print("Question 1: Integer division.")
'''
You are given two values a and b.
Perform integer division and print a//b .
'''

#!/usr/bin/env python3
"""
Integer Division

You’ll be asked how many test cases you want to run, then for each case
you’ll be prompted to enter two values a and b. The script will attempt
to compute a // b, handling ZeroDivisionError and ValueError.
"""

def get_positive_int(prompt):
    """Prompt until the user enters a valid positive integer."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if val <= 0:
                print("Please enter a positive integer: ")
                continue
            return val
        except ValueError as e:
            print(f"Invalid number: {e}")

def get_two_tokens(prompt):
    """Prompt until the user enters exactly two non‑empty tokens."""
    while True:
        tokens = input(prompt).split()
        if len(tokens) != 2:
            print("Please enter exactly two values separated by space: ")
            continue
        return tokens

def main():
    print("\n=== Interactive Integer Division Tester ===\n")

    # 1) How many test cases?
    T = get_positive_int("How many test cases would you like to run? ")

    # 2) Loop through each test case
    for i in range(1, T + 1):
        print(f"\n--- Test case #{i} ---")
        a_str, b_str = get_two_tokens("Enter two values (a b): ")

        try:
            # Convert inputs to integers
            a = int(a_str)
            b = int(b_str)

            # Perform integer division
            result = a // b
            print(f"Result: {a} // {b} = {result}")

        except ZeroDivisionError as zde:
            print(f"  Error Code: {zde}")

        except ValueError as ve:
            print(f"  Error Code: {ve}")

    print("\nAll done! Thank you.\n")

if __name__ == "__main__":
    main()


print("Question 2: ")
'''
You are given a text of N lines. The text contains && and || symbols.
Your task is to modify those symbols to the following:
&& → and
|| → or
Both && and || should have a space " " on both sides.

'''

# !/usr/bin/env python3
"""
AND/OR Replacer

Prompts you for a number of lines, then for each line.
Replaces only occurrences of " && " → " and "
and " || " → " or "
(so it won’t touch &&& or ||| or standalone & or |).
"""


def get_positive_int(prompt):
    """Keep asking until the user enters a valid positive integer."""
    while True:
        raw = input(prompt).strip()
        try:
            n = int(raw)
            if n <= 0:
                print("Please enter a number greater than zero.")
                continue
            return n
        except ValueError:
            print(f" '{raw}' is not a valid integer.")


def main():
    print("\n=== Interactive AND/OR Replacer ===")

    # 1) Ask for how many lines
    N = get_positive_int("How many lines will you enter? ")

    # 2) Collect the lines
    lines = []
    for i in range(1, N + 1):
        line = input(f"Line {i}: ")
        lines.append(line)

    # 3) Perform replacements
    print("\n--- Modified Text ---")
    for line in lines:
        # Only replace " && " with " and "
        # and " || " with " or "
        modified = line.replace(" && ", " and ").replace(" || ", " or ")
        print(modified)

    print("\nDone")


if __name__ == "__main__":
    main()

