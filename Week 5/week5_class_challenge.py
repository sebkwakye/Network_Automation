'''
Write a function that will scan a system directory for any file types such as pdf (or other file extension .py) and document and print the final count
   <example>.pdf


    1.  Create a list of the file's found.
    2.  Provide feedback for the counter, every 10 files found.

# Hint:  Use os.walk()
for r, d, f, in os.walk()

'''

import os


def scan_directory_for_files(directory, extensions):
    """
    Scans a directory for files with specific extensions like .pdf,.py, etc
    """
    file_list = []  # List to store found files
    file_count = 0  # Counter for matching files

    # Walk through the directory
    for root, dir, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(extensions):  # Check file extension
                file_list.append(os.path.join(file))  # Store full file path
                file_count += 1

                # Feedback for every 10 files found
                if file_count % 10 == 0:
                    print(f"Found {file_count} files so far...")

    # Final results
    print(f"Total {len(file_list)} files found with extensions {extensions}.\n")

    # Print list of found files
    for file in file_list:
        print(file)

# Example scan
directory_to_scan = "/Users/sebastiankwakye/PycharmProjects/TCOM570_Network_Automation"
file_extensions = (".py")  # File types to search for

scan_directory_for_files(directory_to_scan, file_extensions)