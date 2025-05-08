print("Problem 1: Find common elements")

'''
Task: Write a program to find common elements between two lists without duplicates.
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
Hints:
Use set operations to find common elements, as sets automatically remove duplicates.
Convert lists to sets using set().
Use the intersection method (&) or the .intersection() method to find common elements.
Convert the result back to a list using list()
'''

print("Solutions to Problem 1")

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

set1 = set(a)   # convert list a to set a
set2 = set(b)   # convert list b to set b
common_elements = set1.intersection(set2)   # common elements between the two new sets
list1 = list(common_elements)   # change back to list
print("Common elements between a and b =", list1)


print("\nProblem 2: Elements Less Than 5")
'''
Task: Print out all the elements of a list that are less than 5.
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
Hints:
Use a loop to iterate through the list.
Use an if statement to check if an element is less than 5.
Print the element if the condition is true.
'''
print("Solutions to Problem 2")

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

for element in a:   # loop through each of the element in a
    if element < 5:
        print(element)


print("\nProblem 3: Check Palindrome")
'''
Task: Take a given string from a user or static variable, check if a given string is a palindrome.
Hints:
Use string slicing to reverse the string.
Compare the original string with its reversed version.
Remember that string comparison is case-sensitive.
'''
print("Solutions to Problem 3")

users_string = input("Enter a string: ").lower() # convert to lowercase, ignoring capitalization/case sensitivity

# check if the string is a palindrome; word or phrase that reads the same forward and backward
if users_string == users_string[::-1]:   # reverse users string and compare
    print("It's a palindrome")
else:
    print("It's not a palindrome")


print("\nProblem 5: Extract Even Elements")
'''
Task: From a given list, create a new list containing only the even elements.
a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
Hints:
Use a *list comprehension* to iterate through the original list and select even numbers.
The modulo operator (%) can be used to check if a number is even.
'''

print("Solutions to Problem 5")
a = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# even_numbers = []
#
# for number in a:
#     if number % 2 == 0:
#         even_numbers.append(number)
# print(even_numbers)

# Extract even numbers using list comprehension
even_numbers = [num for num in a if num % 2 == 0]

# Print the result
print("Even elements:", even_numbers)










