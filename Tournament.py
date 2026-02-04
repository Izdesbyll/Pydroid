import random
import json
import os

def load_tournament(filename="tournament_save.json"):
    """Loads a saved tournament from a JSON file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def save_tournament(tournament_data, filename="tournament_save.json"):
    """Saves the current tournament state to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(tournament_data, f, indent=4)
    print("Tournament progress saved.")

def create_new_tournament(participants):
    """
    Creates a new single-elimination tournament grid with randomly placed participants.
    Pads the participant list with 'BYE' to the next power of 2.
    """
    num_participants = len(participants)
    
    # Calculate the next power of 2 for the tournament grid size
    power_of_2 = 1
    while power_of_2 < num_participants:
        power_of_2 *= 2
    
    # Pad the list with 'BYE's
    padded_participants = participants + ['BYE'] * (power_of_2 - num_participants)
    random.shuffle(padded_participants)
    
    # Create the tournament structure
    tournament = {
        "participants": padded_participants,
        "rounds": [],
        "current_round": 0
    }
    
    # Initialize the first round
    first_round = []
    for i in range(0, len(padded_participants), 2):
        first_round.append({
            "player1": padded_participants[i],
            "player2": padded_participants[i+1],
            "winner": None
        })
    tournament["rounds"].append(first_round)
    
    return tournament

def display_round(tournament):
    """Displays the current round's matches."""
    current_round_data = tournament["rounds"][tournament["current_round"]]
    print(f"\n--- Round {tournament['current_round'] + 1} ---")
    for i, match in enumerate(current_round_data):
        # Indicate if a winner has already been decided
        if match['winner']:
            print(f"Match {i + 1}: {match['player1']} vs. {match['player2']} -> Winner: {match['winner']}")
        else:
            print(f"Match {i + 1}: {match['player1']} vs. {match['player2']}")
    print("-" * 20)

def play_round(tournament):
    """Asks the user to decide the winner for each match in the current round."""
    current_round_data = tournament["rounds"][tournament["current_round"]]
    next_round_data = []

    for i, match in enumerate(current_round_data):
        # Skip matches that have already been played
        if match['winner'] is not None:
            # We still need to add the winner to the next round's list
            if match['winner'] != 'BYE': # Don't add 'BYE' as a winner
                next_round_data.append(match['winner'])
            continue

        player1 = match['player1']
        player2 = match['player2']

        # Handle 'BYE' cases
        if player1 == 'BYE' and player2 == 'BYE':
            print(f"Match {i + 1}: Both players are BYE. No winner.")
            winner = None
        elif player1 == 'BYE':
            winner = player2
            print(f"Match {i + 1}: {player2} receives a BYE. {winner} moves on.")
        elif player2 == 'BYE':
            winner = player1
            print(f"Match {i + 1}: {player1} receives a BYE. {winner} moves on.")
        else:
            while True:
                print(f"Match {i + 1}: {player1} vs. {player2}")
                winner_input = input(f"Who is the winner? Enter 1 for {player1} or 2 for {player2} (or 'save' to save and exit): ")
                
                if winner_input.lower() == 'save':
                    save_tournament(tournament)
                    return False  # Indicate that the user wants to exit
                
                if winner_input == '1':
                    winner = player1
                    break
                elif winner_input == '2':
                    winner = player2
                    break
                else:
                    print("Invalid input. Please enter 1, 2, or 'save'.")

        match['winner'] = winner
        if winner:
            next_round_data.append(winner)

    # If the tournament is not over, create the next round
    if len(next_round_data) > 1:
        next_round_matches = []
        for i in range(0, len(next_round_data), 2):
            next_round_matches.append({
                "player1": next_round_data[i],
                "player2": next_round_data[i+1] if i+1 < len(next_round_data) else 'BYE',
                "winner": None
            })
        tournament["rounds"].append(next_round_matches)
        tournament["current_round"] += 1
    else:
        # Tournament is over
        if next_round_data:
            tournament['winner'] = next_round_data[0]
        else:
            tournament['winner'] = None # In case of all BYEs
        return False  # Indicate that the tournament is over

    return True  # Indicate that the tournament should continue

def main():
    """Main function to run the tournament script."""
    
    # Try to load a saved tournament
    tournament = load_tournament()

    if tournament:
        print("A saved tournament was found. Do you want to continue it?")
        resume = input("Enter 'yes' to continue or 'no' to start a new tournament: ").lower()
        if resume == 'no':
            tournament = None
        
    if not tournament:
        # Start a new tournament
        while True:
            participants_string = input("Enter the names of participants, separated by a semicolon (;): ")
            participants = [name.strip() for name in participants_string.split(';') if name.strip()]
            
            if len(participants) <= 1:
                print("Please enter at least two participant names.")
            else:
                break
        
        tournament = create_new_tournament(participants)

    # Main tournament loop
    while True:
        display_round(tournament)
        
        continue_tournament = play_round(tournament)
        
        if not continue_tournament:
            break
            
    # After the tournament is over
    if 'winner' in tournament and tournament['winner']:
        print(f"\n--- Tournament Complete ---")
        print(f"Congratulations! The winner is: {tournament['winner']}")
        # Remove the save file after completion
        if os.path.exists("tournament_save.json"):
            os.remove("tournament_save.json")
            print("Tournament save file deleted.")
    else:
        print("\nTournament ended.")
    
if __name__ == "__main__":
    main()

