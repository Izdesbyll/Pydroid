import random
import time

# Define the category lists for each country
# This structure makes the script easy to update if the categories change.
CHOICES = {
    "Canada": [
        "season's greetings", "movies", "comedy", "south park", "classic tv comedy",
        "classic tv", "westerns", "crime drama", "true crime", "sci-fi",
        "house of horror", "drama", "reality", "competition reality", "game shows",
        "daytime & talk shows", "documentary + science", "news + opinion",
        "local news", "home + food", "sports"
    ],
    "Britain": [
        "iplayer", "sports", "Merry Christmas!", "movies", "crime drama",
        "bingeable drama", "sci-fi & fantasy", "comedy", "true crime",
        "entertainment", "classic tv", "reality", "real life adventure",
        "documentaries", "living", "news", "paranormal"
    ],
    "USA": [
        "movies", "season's greetings", "comedy", "classic tv", "westerns",
        "sci-fi", "drama", "true crime", "reality", "competition reality",
        "entertainment", "daytime + game shows", "news + opinion", "sports",
        "history + science", "home + food", "animals + nature", "local news"
    ]
}
COUNTRIES = list(CHOICES.keys())

def generate_initial_picks():
    """Picks a random country and a random category based on that country."""
    # 1. Pick Country out of "USA", "Britain", "Canada"
    country = random.choice(COUNTRIES)

    # 2. Pick Category based on the chosen Country
    categories = CHOICES[country]
    category = random.choice(categories)

    return country, category

def generate_day_number():
    """Picks a random number from 1 to 31."""
    # 3. Pick a number from 1 to 31
    return random.randint(1, 31)

def display_picks(country, category, day):
    """Prints the current set of picks in a nicely formatted box."""
    print("\n" + "🌟" * 20)
    print("      🎁 YOUR RANDOM PICKS 🎁")
    print("🌟" * 20)
    print(f"1. Country:    {country}")
    print(f"2. Category:   {category}")
    print(f"3. Day Number: {day}")
    print("🌟" * 20)

def main():
    """Main function to run the interactive picker."""
    print("--- Random Country, Category, and Day Picker ---")
    
    # Initial generation of Country and Category
    try:
        country, category = generate_initial_picks()
        day = generate_day_number()
    except IndexError as e:
        # Failsafe if the CHOICES lists are empty
        print(f"Error: Could not generate initial picks. Check the CHOICES lists. {e}")
        return

    # Main interactive loop
    while True:
        display_picks(country, category, day)
        
        # User prompt for interaction
        print("\n--- Interaction Menu ---")
        print(" 'r' : Repick ONLY the Day Number (random number lower than current).")
        print(" 'n' : Generate ALL new picks (Country, Category, Day).")
        print(" 'q' : Quit the script.")
        
        # Get user input
        user_input = input("Your choice ('r', 'n', or 'q'): ").strip().lower()

        if user_input == 'r':
            # Repick ONLY the day number, but lower than the current one
            if day > 1:
                print(f"\nProcessing... Repicking Day Number (lower than {day})...")
                time.sleep(0.5)
                # Generate a new random number from 1 up to (but not including) the current day.
                # The upper limit of random.randint is inclusive, so we use day - 1.
                day = random.randint(1, day - 1)
            else:
                print("\nCannot repick a lower day number. The current day is 1 (the lowest possible).")
            # Loop continues to display the new results
        elif user_input == 'n':
            # Generate all new picks
            print("\nProcessing... Generating ALL new picks...")
            time.sleep(0.5)
            country, category = generate_initial_picks()
            day = generate_day_number()
            # Loop continues to display the new results
        elif user_input == 'q':
            # Quit the program
            print("\nThank you for using the random picker! Have a great day.")
            break
        else:
            print("\nInvalid input. Please enter 'r', 'n', or 'q'.")

if __name__ == "__main__":
    # Ensure the main function is called when the script is run
    main()