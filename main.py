# Imports
import os
import random

# Word Banks for Different Difficulty Levels

easy_words = [
    "apple", "bread", "chair", "drink", "flame", "grape", "lemon", "plant", "storm", "water",
    "smile", "beach", "grace", "light", "stone", "candy", "fruit", "green", "house", "juice",
    "music", "night", "olive", "peach"
]

medium_words = [
    "amber", "bloom", "brisk", "climb", "creek", "dream", "eagle", "frost", "ghost", "glove",
    "hover", "jelly", "knife", "leech", "mercy", "naval", "ocean", "prism", "quilt", "raven",
    "spear", "thorn", "union", "valve", "waltz"
]

hard_words = [
    "abyss", "blitz", "crisp", "dwarf", "fjord", "glyph", "hazel", "ivory", "jumps", "kayak",
    "lynch", "myths", "nymph", "ovary", "pique", "quasi", "rhyme", "sphinx", "twist", "vapor",
    "wretch", "xenon", "yacht", "zesty", "zilch"
]

expert_words = [
    "azure", "banjo", "cacti", "delta", "equip", "focal", "gipsy", "haiku", "injury", "jazzy",
    "khaki", "length", "matrix", "numb", "oxygen", "plaza", "quartz", "rhythm", "squad", "thyme",
    "uncut", "vodka", "whack", "xylem", "zonal"
]

legendary_words = [
    "axiom", "blaze", "croak", "duchy", "ethos", "froth", "glyph", "hymen", "ivory", "jumbo",
    "kudzu", "leech", "mauve", "nexus", "onyx", "phlox", "quake", "repel", "siren", "trove",
    "umbra", "vortex", "waltz", "xenon", "yacht"
]

# Function to select a word based on difficulty level
def select_word(difficulty):
    if difficulty == 'easy':
        return random.choice(easy_words).upper()
    elif difficulty == 'medium':
        return random.choice(medium_words).upper()
    elif difficulty == 'hard':
        return random.choice(hard_words).upper()
    elif difficulty == 'expert':
        return random.choice(expert_words).upper()
    elif difficulty == 'legendary':
        return random.choice(legendary_words).upper()
    else:
        raise ValueError("Invalid difficulty level. Choose from: easy, medium, hard, expert, legendary.")

# Enemies and Their Difficulty Distributions
enemies = {
    "Grunt": {"easy": 30, "medium": 40, "hard": 20, "expert": 1, "legendary": 9},
    "Warrior": {"easy": 20, "medium": 30, "hard": 30, "expert": 10, "legendary": 10},
    "Champion": {"easy": 10, "medium": 20, "hard": 40, "expert": 20, "legendary": 10},
    "Overlord": {"easy": 5, "medium": 15, "hard": 40, "expert": 25, "legendary": 15},
    "God": {"easy": 10, "medium": 20, "hard": 20, "expert": 35, "legendary": 15}
}

# Function to select a word based on an enemy's difficulty distribution
def select_word_for_enemy(enemy_name):
    difficulty_weights = enemies[enemy_name]
    difficulties = list(difficulty_weights.keys())
    weights = list(difficulty_weights.values())
    chosen_difficulty = random.choices(difficulties, weights=weights, k=1)[0]
    return select_word(chosen_difficulty)

# Function to generate an enemy sequence based on the number of rounds
def generate_enemy_sequence(num_rounds):
    enemy_types = ["Grunt", "Warrior", "Champion", "Overlord", "God"]
    sequence = []
    for i in range(num_rounds):
        enemy = enemy_types[min(i // 2, len(enemy_types) - 1)]  # Adjust enemy type based on round
        sequence.append(enemy)
    return sequence

# Class Definitions
class Book:
    def __init__(self, name, description, base_trigger_chance, effect):
        self.name = name
        self.description = description
        self.base_trigger_chance = base_trigger_chance
        self.effect = effect  # Function defining the book's effect
        self.modifiers = []  # List to hold any modifiers applied to the book

    def get_trigger_chance(self, game_state):
        # Calculate the actual trigger chance, considering modifiers and global modifiers
        chance = self.base_trigger_chance + game_state['global_trigger_chance_bonus']
        for modifier in self.modifiers:
            chance += modifier.trigger_chance_bonus
        # Ensure the chance does not exceed 100%
        return min(chance, 1.0)

    def apply_effect(self, game_state):
        # Apply the book's effect to the game state
        self.effect(game_state)

class Modifier:
    def __init__(self, name, trigger_chance_bonus=0):
        self.name = name
        self.trigger_chance_bonus = trigger_chance_bonus

# Book Effect Functions
def reveal_first_position(game_state):
    # Reveal the first letter of the answer in the current guess
    game_state['current_guess'][0] = game_state['answer'][0].upper()
    game_state.setdefault('active_effects', []).append("Reveal First Position")

def reveal_last_position(game_state):
    # Reveal the last letter of the answer in the current guess
    game_state['current_guess'][-1] = game_state['answer'][-1].upper()
    game_state.setdefault('active_effects', []).append("Reveal Last Position")

def reveal_middle_position(game_state):
    # Reveal the middle letter of the answer in the current guess
    middle_index = len(game_state['answer']) // 2
    game_state['current_guess'][middle_index] = game_state['answer'][middle_index].upper()
    game_state.setdefault('active_effects', []).append("Reveal Middle Position")

def spot_random_vowel(game_state):
    # Add a random vowel from the answer to correct letters
    vowels = [ch for ch in game_state['answer'] if ch.upper() in 'AEIOU']
    if vowels:
        revealed_vowel = random.choice(vowels).upper()
        game_state['correct_letters'].add(revealed_vowel)
        game_state.setdefault('active_effects', []).append(f"Spot Random Vowel: {revealed_vowel}")

def increase_global_trigger_chance(game_state):
    # Increase global trigger chance bonus by 5%
    game_state['global_trigger_chance_bonus'] += 0.05
    game_state.setdefault('active_effects', []).append("Global Trigger Chance Increased by 5%")

# Game Functions
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_ui(game_state, last_book_used=None, book_triggered=None, books_used_this_round=None):
    clear_screen()
    print("Guess the 5-letter word!\n")
    print(f"Current Guess: {' '.join(game_state['current_guess'])}\n")
    print("Guess History:")
    for guess in game_state['guess_history']:
        print(' '.join(guess))
    print()
    print("[O] | " + (', '.join(sorted(game_state['correct_letters'])) if game_state['correct_letters'] else "[none]"))
    print("[X] | " + (', '.join(sorted(game_state['incorrect_letters'])) if game_state['incorrect_letters'] else "[none]"))
    print()
    # Show any additional information such as active effects
    if game_state and 'active_effects' in game_state and game_state['active_effects']:
        print("Active Effects:")
        for effect in game_state['active_effects']:
            print(f"- {effect}")
    if last_book_used:
        print(f"\nBook Used: {last_book_used.name}")
        if book_triggered:
            print(f"The effect of '{last_book_used.name}' was applied!")
        else:
            print(f"The effect of '{last_book_used.name}' did not trigger.")
    print()
    # Show books used this round if provided
    if books_used_this_round is not None:
        print("Books Used This Round:")
        for book_name, used in books_used_this_round.items():
            status = "Used" if used else "Available"
            print(f"- {book_name}: {status}")
    print()

# Book Management Functions
# Create a repository of available books
available_books = [
    Book(
        name="Reveal First Position",
        description="40% chance to reveal the first letter of the answer.",
        base_trigger_chance=0.4,
        effect=reveal_first_position
    ),
    Book(
        name="Reveal Last Position",
        description="40% chance to reveal the last letter of the answer.",
        base_trigger_chance=0.4,
        effect=reveal_last_position
    ),
    Book(
        name="Reveal Middle Position",
        description="40% chance to reveal the middle letter of the answer.",
        base_trigger_chance=0.4,
        effect=reveal_middle_position
    ),
    Book(
        name="Spot Random Vowel",
        description="40% chance to identify a random vowel in the answer.",
        base_trigger_chance=0.4,
        effect=spot_random_vowel
    ),
    Book(
        name="Global Trigger Chance Increase",
        description="Permanently increases trigger chance of all books by 5%.",
        base_trigger_chance=1.0,  # This effect always applies when the book is used
        effect=increase_global_trigger_chance
    ),
    # Add more books as needed
]

# Initialize the bookbag
bookbag = []  # List to hold Book instances

def add_book_to_bookbag(book):
    if len(bookbag) < 5:
        bookbag.append(book)
        print(f"You have added '{book.name}' to your bookbag.")
    else:
        print("Your bookbag is full. You need to remove a book before adding a new one.")
        remove_book_from_bookbag()
        bookbag.append(book)
        print(f"You have added '{book.name}' to your bookbag.")

def remove_book_from_bookbag():
    if bookbag:
        print("Select a book to remove:")
        for idx, book in enumerate(bookbag):
            print(f"{idx + 1}. {book.name} - {book.description}")
        choice = int(input("Enter the number of the book to remove: ")) - 1
        if 0 <= choice < len(bookbag):
            removed_book = bookbag.pop(choice)
            print(f"You have removed '{removed_book.name}' from your bookbag.")
        else:
            print("Invalid selection. No book was removed.")
    else:
        print("Your bookbag is empty. No book to remove.")

def list_books_in_bookbag():
    if bookbag:
        print("Your Bookbag:")
        for idx, book in enumerate(bookbag):
            print(f"{idx + 1}. {book.name} - {book.description}")
    else:
        print("Your bookbag is empty.")

def choose_book_reward():
    print("Choose one of the following books as your reward:")
    # Exclude books already in the bookbag
    available_choices = [book for book in available_books if book not in bookbag]
    if len(available_choices) == 0:
        print("No new books are available.")
        return
    # Provide up to two random book choices
    reward_books = random.sample(available_choices, min(2, len(available_choices)))
    for idx, book in enumerate(reward_books):
        print(f"{idx + 1}. {book.name} - {book.description}")
    choice = int(input("Enter the number of the book you want: ")) - 1
    if 0 <= choice < len(reward_books):
        selected_book = reward_books[choice]
        add_book_to_bookbag(selected_book)
    else:
        print("Invalid selection. You did not receive a new book.")

# Main Game Loop
def main():
    global bookbag  # Ensure we're using the global bookbag

    # Ask the player how many rounds they want to play
    num_rounds = input("Enter the number of rounds you want to play (e.g., 8): ")
    if not num_rounds.isdigit():
        num_rounds = 8
    else:
        num_rounds = int(num_rounds)

    enemy_sequence = generate_enemy_sequence(num_rounds)
    round_number = 1

    for enemy_name in enemy_sequence:
        print(f"Round {round_number}: Facing {enemy_name}!")
        # Reset game state variables for the new round
        answer = select_word_for_enemy(enemy_name)
        current_guess = ['_'] * 5
        guess_history = []
        correct_letters = set()
        incorrect_letters = set()
        guessed_letters = set()
        attempts = 0

        # Initialize the tracking of book usage for this round
        books_used_this_round = {book.name: False for book in bookbag}

        game_state = {
            'current_guess': current_guess,
            'answer': answer,
            'correct_letters': correct_letters,
            'incorrect_letters': incorrect_letters,
            'guessed_letters': guessed_letters,
            'guess_history': guess_history,
            'active_effects': [],
            'global_trigger_chance_bonus': 0.0  # Carry over global modifiers if needed
        }

        last_book_used = None
        book_triggered = None

        max_attempts = 6  # You can adjust this if needed

        # Start the guessing game loop for this enemy
        while attempts < max_attempts:
            display_ui(game_state, last_book_used, book_triggered, books_used_this_round)
            list_books_in_bookbag()  # Display the books in the player's bookbag

            # Reset book tracking variables
            last_book_used = None
            book_triggered = None
            game_state['active_effects'] = []  # Reset active effects for this turn

            # If it's after the first guess and there are books available to use this round
            if attempts > 0:
                available_books_to_use = [book for book in bookbag if not books_used_this_round.get(book.name, False)]
                if available_books_to_use:
                    print("Would you like to use a book from your bookbag? (Y/N)")
                    use_book = input().strip().upper()
                    if use_book == 'Y':
                        # Display list of available books
                        print("Choose a book to use:")
                        for idx, book in enumerate(available_books_to_use):
                            print(f"{idx + 1}. {book.name} - {book.description}")
                        choice = input("Enter the number of the book to use: ").strip()
                        if choice.isdigit():
                            choice = int(choice) - 1
                            if 0 <= choice < len(available_books_to_use):
                                selected_book = available_books_to_use[choice]
                                last_book_used = selected_book
                                trigger_chance = selected_book.get_trigger_chance(game_state)
                                if random.random() <= trigger_chance:
                                    selected_book.apply_effect(game_state)
                                    book_triggered = True
                                    print(f"The effect of '{selected_book.name}' has been applied!")
                                else:
                                    book_triggered = False
                                    print(f"The effect of '{selected_book.name}' did not trigger.")
                                # Mark the book as used in this round
                                books_used_this_round[selected_book.name] = True
                            else:
                                print("Invalid selection. No book was used.")
                        else:
                            print("Invalid input. No book was used.")
                    else:
                        print("No book used this turn.")
                else:
                    print("You have used all your books this round.")
            else:
                print("No books can be used on the first guess.")

            # Proceed to get player's guess
            player_input = input("Enter your guess: ").upper()

            if len(player_input) != 5 or not player_input.isalpha():
                print("Please enter a valid 5-letter word.")
                continue

            guess = list(player_input)
            guess_history.append(guess)
            guessed_letters.update(guess)

            # Check each letter in the guess
            for i, letter in enumerate(guess):
                if letter == answer[i]:
                    current_guess[i] = letter
                    correct_letters.add(letter)
                elif letter in answer:
                    correct_letters.add(letter)
                else:
                    incorrect_letters.add(letter)

            attempts += 1

            # Check win condition
            if ''.join(current_guess) == answer:
                display_ui(game_state, last_book_used, book_triggered, books_used_this_round)
                print(f"Congratulations! You've defeated {enemy_name} by guessing the word '{answer}'!")
                choose_book_reward()  # Allow the player to choose a book reward after winning
                break
        else:
            display_ui(game_state, last_book_used, book_triggered, books_used_this_round)
            print(f"Game Over! You were defeated by {enemy_name}. The correct word was '{answer}'.")
            return  # End the game if the player loses

        round_number += 1

    print("Congratulations! You have defeated all enemies!")

if __name__ == "__main__":
    main()
