import tkinter as tk
import random
from pokeapi_client import PokeAPIClient
from tkinter import messagebox, StringVar

# Constants for game setup
DIFFICULTIES = ["Normal", "Hard"]
REGIONS = [
    "All", "Kanto", "Johto", "Hoenn", "Sinnoh",
    "Unova", "Kalos", "Alola", "Galar"
]
INSTRUCTIONS_TEXT = """
Welcome to the Pokémon Quiz Game!

Instructions:
1. Choose your difficulty and region.
2. A random Pokémon ID will appear.
3. Type the name of the Pokémon.
4. If wrong, you'll receive hints.
5. You have limited lives in Hard mode.
6. Try to score as high as possible!
"""

class PokemonQuizGame:
    def __init__(self, root):
        self.client = PokeAPIClient()
        self.root = root
        self.root.title("Pokémon Quiz Game")

        # Initialize game variables
        self.score = 0
        self.lives = 3  # Default for hard mode, adjust based on difficulty
        self.current_pokemon = None
        self.hint_text = tk.StringVar()  # For updating hints

        # Set up all screens
        self.setup_welcome_screen()
        self.setup_instructions_screen()
        self.setup_game_setup_screen()
        self.setup_game_screen()
        self.setup_game_over_screen()

        # Show the welcome frame first
        self.show_frame(self.welcome_frame)

    def show_frame(self, frame):
        frame.tkraise()

    def setup_welcome_screen(self):
        self.welcome_frame = tk.Frame(self.root)
        self.welcome_frame.grid(row=0, column=0, sticky='news')

        tk.Label(self.welcome_frame, text="Pokémon Quiz Game", font=("Helvetica", 18)).pack(pady=20)
        tk.Button(self.welcome_frame, text="Play", command=lambda: self.show_frame(self.setup_frame)).pack()
        tk.Button(self.welcome_frame, text="Instructions", command=lambda: self.show_frame(self.instructions_frame)).pack()

    def setup_instructions_screen(self):
        self.instructions_frame = tk.Frame(self.root)
        self.instructions_frame.grid(row=0, column=0, sticky='news')

        tk.Label(self.instructions_frame, text="Instructions", font=("Helvetica", 18)).pack(pady=20)
        tk.Label(self.instructions_frame, text=INSTRUCTIONS_TEXT, justify=tk.LEFT).pack(pady=10)
        tk.Button(self.instructions_frame, text="Back", command=lambda: self.show_frame(self.welcome_frame)).pack()

    def setup_game_setup_screen(self):
        self.setup_frame = tk.Frame(self.root)
        self.setup_frame.grid(row=0, column=0, sticky='news')

        # Difficulty and region selection
        tk.Label(self.setup_frame, text="Select Difficulty:", font=("Helvetica", 14)).pack(pady=5)
        self.difficulty_var = StringVar(self.root)
        self.difficulty_var.set(DIFFICULTIES[0])  # default value
        tk.OptionMenu(self.setup_frame, self.difficulty_var, *DIFFICULTIES).pack()

        tk.Label(self.setup_frame, text="Select Region:", font=("Helvetica", 14)).pack(pady=5)
        self.region_var = StringVar(self.root)
        self.region_var.set(REGIONS[0])  # default value
        tk.OptionMenu(self.setup_frame, self.region_var, *REGIONS).pack()

        tk.Button(self.setup_frame, text="Start Game", command=self.prepare_game).pack(pady=20)

    def setup_game_screen(self):
        self.game_frame = tk.Frame(self.root)
        self.game_frame.grid(row=0, column=0, sticky='news')

        # Game UI elements
        tk.Label(self.game_frame, text="Pokémon Quiz Game", font=("Helvetica", 18)).pack(pady=10)
        self.score_label = tk.Label(self.game_frame, text="Score: 0 | Lives: 3", font=("Helvetica", 14))
        self.score_label.pack(pady=10)
        self.pokedex_label = tk.Label(self.game_frame, text="Pokédex ID: ???", font=("Helvetica", 12))
        self.pokedex_label.pack(pady=10)
        self.hint_label = tk.Label(self.game_frame, textvariable=self.hint_text)
        self.hint_label.pack(pady=10)

        self.user_input = tk.Entry(self.game_frame)
        self.user_input.pack(pady=10)
        tk.Button(self.game_frame, text="Guess", command=self.check_answer).pack()

    def setup_game_over_screen(self):
        self.game_over_frame = tk.Frame(self.root)
        self.game_over_frame.grid(row=0, column=0, sticky='news')

        tk.Label(self.game_over_frame, text="Game Over", font=("Helvetica", 18)).pack(pady=20)
        self.final_score_label = tk.Label(self.game_over_frame, text="Your final score was: 0", font=("Helvetica", 14))
        self.final_score_label.pack(pady=10)
        tk.Button(self.game_over_frame, text="Play Again", command=self.play_again).pack(side=tk.LEFT, padx=20)
        tk.Button(self.game_over_frame, text="Quit", command=self.quit_game).pack(side=tk.RIGHT, padx=20)

    def prepare_game(self):
        # Set game parameters and move to the game screen
        self.setup_game()
        self.show_frame(self.game_frame)
        self.start_new_round()

    def start_new_round(self):
        # Reset hint text
        self.hint_text.set("")

        # Fetch a new Pokémon based on selected region
        region = self.region_var.get().lower()
        difficulty = self.difficulty_var.get().lower()
        self.lives = 3 if difficulty == "hard" else float('inf')

        start_id, end_id = self.get_generation_id(region)
        pokemon_id = random.randint(start_id, end_id)
        self.current_pokemon = self.client.get_pokemon(pokemon_id)
        if self.current_pokemon:
            self.pokedex_label.config(text=f"Pokédex ID: {self.current_pokemon['id']}")
            self.user_input.delete(0, tk.END)  # Clear input field for the new round
        else:
            messagebox.showerror("Error", "Failed to fetch Pokémon data.")

    def check_answer(self):
        user_answer = self.user_input.get().lower()
        if user_answer == self.current_pokemon['name']:
            self.score += 5 - 2 * self.hint_level  # Adjust based on hints used
            messagebox.showinfo("Correct!", f"You got it right! It's {self.current_pokemon['name'].title()}.")
            self.update_score_and_lives()
            self.start_new_round()
        else:
            self.hint_level += 1
            if self.hint_level == 1:
                self.hint_text.set(f"Hint 1 - Type: {', '.join(self.current_pokemon['types'])}")
            elif self.hint_level == 2:
                self.hint_text.set(f"Hint 2 - Abilities: {', '.join(self.current_pokemon['abilities'])}")
            else:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.hint_text.set("No more hints!")
            self.update_score_and_lives()

    def update_score_and_lives(self):
        lives_text = f"Lives: {'∞' if self.lives == float('inf') else self.lives}"
        self.score_label.config(text=f"Score: {self.score} | {lives_text}")

    def game_over(self):
        self.final_score_label.config(text=f"Your final score was: {self.score}")
        self.show_frame(self.game_over_frame)

    def play_again(self):
        self.setup_game()
        self.show_frame(self.welcome_frame)

    def quit_game(self):
        self.root.destroy()

    def setup_game(self):
        # Reset game variables and update UI as needed for a new game
        self.score = 0
        self.lives = 3
        self.hint_level = 0  # Reset hint level for a new game
        self.update_score_and_lives()

    def get_generation_id(self, region):
        """Return the range of Pokédex IDs corresponding to the given region (generation)."""
        generations = {
            'all': (1, 898),
            'kanto': (1, 151),
            'johto': (152, 251),
            'hoenn': (252, 386),
            'sinnoh': (387, 493),
            'unova': (494, 649),
            'kalos': (650, 721),
            'alola': (722, 809),
            'galar': (810, 898)  # Update these ranges as new Pokémon or regions are added
        }
        return generations.get(region.lower(), (1, 898))  # Default to all if region not found

def main():
    root = tk.Tk()
    root.geometry("500x400")  # Adjust size as needed
    game = PokemonQuizGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
