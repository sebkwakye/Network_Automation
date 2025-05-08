'''
A Python script that:

1. Takes a movie title as input
2. Makes a request to the OMDb API
3. Displays basic movie information (title, year, director, runtime, IMDB Rating, plot)
'''

import requests
import json
import webbrowser

# Convert runtime from the format "125 min" to "2 Hrs 5 Min
def convert_runtime(runtime_str):
    try:
        minutes = int(runtime_str.split()[0])
        hours = minutes // 60
        minutes_remainder = minutes % 60
        return f"{hours} Hrs {minutes_remainder} Min"
    except Exception:
        return runtime_str

# Save movie to JSON file
def save_movie_data(movie_data, filename="movie_data.json"):
    try:
        with open(filename, "w") as f:
            json.dump(movie_data, f, indent=4)
        print(f"Movie data saved to {filename}")
    except Exception as e:
        print("Error saving movie data:", e)


def main():
    # OMDb API key
    api_key = "b9a1ed52"

    # Get movie title input from user
    movie_title = input("Enter a movie title: ").strip()

    # Build the API request URL and parameters
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

    # Make the API request
    response = requests.get(url)

    # Check if the API request was successful
    if response.status_code != 200:
        print("Error: Unable to reach the OMDb API. Try again later.")
        return

    # Convert the response into JSON format
    data = response.json()

    # Check if the API response indicates the movie wasn't found
    if data.get("Response", "False") == "False":
        print("Movie not found:", data.get("Error", "No error information provided."))
        return

    # Display basic movie information
    print("\n--- Movie Information ---")
    print("Title:", data.get("Title", "N/A"))
    print("Year:", data.get("Year", "N/A"))
    print("Director:", data.get("Director", "N/A"))

    runtime_original = data.get("Runtime", "N/A")
    runtime_converted = convert_runtime(runtime_original)
    print("Runtime:", runtime_original, "->", runtime_converted)

    print("IMDB Rating:", data.get("imdbRating", "N/A"))
    print("Plot:", data.get("Plot", "N/A"))
    print("---------------------------\n")

    # Save the movie data to a JSON file
    save_movie_data(data)

    # Display the movie poster image using your default web browser
    poster_url = data.get("Poster", "N/A")
    if poster_url != "N/A" and poster_url.startswith("http"):
        print("Opening movie poster in your browser...")
        webbrowser.open(poster_url)
    else:
        print("Poster image not available.")


if __name__ == "__main__":
    main()
