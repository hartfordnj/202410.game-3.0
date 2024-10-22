import os
import random

class Book:
    def __init__(self, name, description, base_trigger_chance, effect):
        self.name = name
        self.description = description
        self.base_trigger_chance = base_trigger_chance
        self.effect = effect  # Function defining the book's effect
        self.modifiers = []

    def get_trigger_chance(self):
        # Calculate the actual trigger chance, considering modifiers
        chance = self.base_trigger_chance
        for modifier in self.modifiers:
            chance += modifier.trigger_chance_bonus
        # Ensure the chance does not exceed 100%
        return min(chance, 1.0)

    def apply_effect(self, game_state):
        # Apply the book's effect to the game state
        self.effect(game_state)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

word_list = ["apple", "bread", "chair", "drink", "flame", "grape", "lemon", "plant", "storm", "water"]

def select_word():
    return random.choice(word_list).upper()

def display_ui(game_state):
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
    print()

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

def main():
    answer = select_word()
    current_guess = ['_'] * 5
    guess_history = []
    correct_letters = set()
    incorrect_letters = set()
    guessed_letters = set()
    max_attempts = 6
    attempts = 0

    game_state = {
        'current_guess': current_guess,
        'answer': answer,
        'correct_letters': correct_letters,
        'incorrect_letters': incorrect_letters,
        'guessed_letters': guessed_letters,
        'guess_history': guess_history,
        'active_effects': []
    }

    while attempts < max_attempts:
        display_ui(game_state)
        list_books_in_bookbag()  # Display the books in the player's bookbag

        # If it's after the first guess and the bookbag is not empty
        if attempts > 0 and bookbag:
            print("Would you like to use a book from your bookbag? (Y/N)")
            use_book = input().strip().upper()
            if use_book == 'Y':
                # Display list of books
                print("Choose a book to use:")
                for idx, book in enumerate(bookbag):
                    print(f"{idx + 1}. {book.name} - {book.description}")
                choice = input("Enter the number of the book to use: ").strip()
                if choice.isdigit():
                    choice = int(choice) - 1
                    if 0 <= choice < len(bookbag):
                        selected_book = bookbag[choice]
                        trigger_chance = selected_book.get_trigger_chance()
                        if random.random() <= trigger_chance:
                            selected_book.apply_effect(game_state)
                            print(f"The effect of '{selected_book.name}' has been applied!")
                        else:
                            print(f"The effect of '{selected_book.name}' did not trigger.")
                    else:
                        print("Invalid selection. No book was used.")
                else:
                    print("Invalid input. No book was used.")
            else:
                print("No book used this turn.")
        else:
            print("No books available or this is your first guess.")

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
            display_ui(game_state)
            print(f"Congratulations! You've guessed the word '{answer}' correctly!")
            choose_book_reward()  # Allow the player to choose a book reward after winning
            break
    else:
        display_ui(game_state)
        print(f"Game Over! The correct word was '{answer}'.")

if __name__ == "__main__":
    main()
