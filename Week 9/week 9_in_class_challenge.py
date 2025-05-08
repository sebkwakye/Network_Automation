'''
The File Scraper script should:

1. Connect to a specified webpage.  Some examples here, but you do not have to use these (University friendly links only)
   https://www.dhs.gov/publications-library/cybersecurity
   https://csrc.nist.gov/publications
2. Parse the HTML to find all links (href)
3. Filter the links to identify files of a specific type (e.g., PDFs, DOCs)
4. Download each file, saving it with a meaningful name (Make a directory if you prefer)
5. Include proper error handling and rate limiting (1 file per second, time.sleep() works well)
6. Provide user feedback on progress of downloads (filename and count)
'''


import requests
from bs4 import BeautifulSoup
import time
import os

# Connect to the specified webpage
url = "https://www.dhs.gov/publication/zero-trust-implementation-strategy"  # URL of the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print(f"Successfully connected to {url}")
else:
    print(f"Failed to connect to {url}. Status code: {response.status_code}")
    exit()

# Parse the HTML content to find all links
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a')  # Find all <a> tags

# Filter the links to identify files of specific types (.pdf)
file_count = 0
download_folder = "downloads"

# Create download folder if it doesn't exist
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Download each file
for link in links:
    href = link.get('href')

    # Check if the link contains a PDF file
    if '.pdf' in href:
        file_count += 1
        print(f"PDF found, downloading file #{file_count}: {href}")

        # Construct the full URL for the file
        file_url = requests.compat.urljoin(url, href)  # Ensure we have a complete URL
        file_name = f"file_{file_count}.pdf"  # Use a meaningful name for the file

        try:
            # Request the file content
            pdf_response = requests.get(file_url)
            pdf_response.raise_for_status()

            # Save the file to the downloads folder
            file_path = os.path.join(download_folder, file_name)
            with open(file_path, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)

            print(f"File #{file_count} downloaded: {file_name}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {file_url}: {e}")

        time.sleep(1)  # Rate limit to 1 file per second

# Final message
print(f"Completed! {file_count} files downloaded.")
