import random
import time
from pokeapi_client import PokeAPIClient

def display_time_bar(time_left, total_time=30, bar_length=30):
    """Displays a simple text-based timer bar."""
    proportion_left = time_left / total_time
    num_bars = int(proportion_left * bar_length)
    return '[' + '#' * num_bars + '-' * (bar_length - num_bars) + ']'

def get_generation_id(region):
    """Return the range of Pokédex IDs corresponding to the given region (generation)."""
    generations = {
        'kanto': (1, 151),
        'johto': (152, 251),
        'hoenn': (252, 386),
        'sinnoh': (387, 493),
        'unova': (494, 649),
        'kalos': (650, 721),
        'alola': (722, 809),
        'galar': (810, 898)  # Update these ranges as new Pokémon are added or based on your API's data
    }
    return generations.get(region.lower(), (1, 898))  # Default to all if region not found

def main():
    client = PokeAPIClient()
    score = 0

    # Difficulty setup
    difficulty = input("Select difficulty (Normal/Hard): ").strip().lower()
    hard_mode = difficulty == "hard"
    lives = 3 if hard_mode else int(5)  # Infinite lives for Normal, 3 for Hard
    total_time = 30  # Total time for each round in Hard mode

    # Region setup
    print("Regions: Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar, or All")
    region = input("Choose a region: ").strip().lower()
    start_id, end_id = get_generation_id(region)

    print(f"Welcome to the Pokémon Quiz Game! You are playing on {difficulty.title()} mode.")

    try:
        while lives > 0:
            random_id = random.randint(start_id, end_id)
            pokemon = client.get_pokemon(random_id)

            if pokemon:
                print(f"\nPokédex ID: {random_id}")

                start_time = time.time()
                hint_level = 0  # Track the level of hint provided

                while True:
                    if hard_mode:
                        # Calculate remaining time
                        time_left = total_time - (time.time() - start_time)
                        if time_left <= 0:
                            print("Time's up! -1 life")
                            lives -= 1
                            break  # Exit the inner loop to start a new round
                        
                        # Display the time bar
                        print(f"Time left: {display_time_bar(time_left, total_time)}")

                    guess = input("Guess the Pokémon: ").strip().lower()

                    if guess == pokemon['name']:
                        # Correct guess, award points based on the hint level
                        print(f"Correct! +{5 - 2 * hint_level} points")
                        score += 5 - 2 * hint_level
                        break
                    else:
                        hint_level += 1
                        if hint_level == 1:
                            print(f"Wrong! Here's a hint. Types: {', '.join(pokemon['types']).title()}")
                        elif hint_level == 2:
                            print(f"Still not right. Another hint. Abilities: {', '.join(pokemon['abilities']).title()}")
                        else:
                            print(f"Out of hints! The correct Pokémon was {pokemon['name'].title()}. -1 life")
                            lives -= 1
                            break

                print(f"Current Score: {score}, Lives Remaining: {'∞' if lives == float('inf') else lives}")
            else:
                print("Failed to fetch data for Pokémon. Please try again.")
                break  # Exit if unable to fetch data

    except KeyboardInterrupt:
        # Handles the user exiting the game
        print(f"\nGame Over! Your final score was {score}.")

if __name__ == '__main__':
    main()
