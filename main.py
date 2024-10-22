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

def display_ui(current_guess, guess_history, correct_letters, incorrect_letters):
    clear_screen()
    print("Guess the 5-letter word!\n")
    print(f"Current Guess: {' '.join(current_guess)}\n")
    print("Guess History:")
    for guess in guess_history:
        print(' '.join(guess))
    print()
    print("[O] | " + (', '.join(sorted(correct_letters)) if correct_letters else "[none]"))
    print("[X] | " + (', '.join(sorted(incorrect_letters)) if incorrect_letters else "[none]"))
    print()

def reveal_first_position(game_state):
    # Reveal the first letter of the answer in the current guess
    game_state['current_guess'][0] = game_state['answer'][0].upper()

def reveal_last_position(game_state):
    # Reveal the last letter of the answer in the current guess
    game_state['current_guess'][-1] = game_state['answer'][-1].upper()

def reveal_middle_position(game_state):
    # Reveal the middle letter of the answer in the current guess
    middle_index = len(game_state['answer']) // 2
    game_state['current_guess'][middle_index] = game_state['answer'][middle_index].upper()

def spot_random_vowel(game_state):
    # Add a random vowel from the answer to correct letters
    vowels = [ch for ch in game_state['answer'] if ch.upper() in 'AEIOU']
    if vowels:
        revealed_vowel = random.choice(vowels).upper()
        game_state['correct_letters'].add(revealed_vowel)

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
        'guess_history': guess_history
    }

    while attempts < max_attempts:
        display_ui(current_guess, guess_history, correct_letters, incorrect_letters)
        list_books_in_bookbag()  # Display the books in the player's bookbag
        player_input = input("Enter your guess: ").upper()

        if len(player_input) != 5 or not player_input.isalpha():
            print("Please enter a valid 5-letter word.")
            continue

        # Apply a random book effect with a certain probability
        if bookbag:  # Only apply if there are books in the bookbag
            book = random.choice(bookbag)
            if random.random() <= book.get_trigger_chance():
                book.apply_effect(game_state)

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
            display_ui(current_guess, guess_history, correct_letters, incorrect_letters)
            print(f"Congratulations! You've guessed the word '{answer}' correctly!")
            break
    else:
        display_ui(current_guess, guess_history, correct_letters, incorrect_letters)
        print(f"Game Over! The correct word was '{answer}'.")

if __name__ == "__main__":
    main()
