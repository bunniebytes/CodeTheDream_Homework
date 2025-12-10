# Task 4
from collections import defaultdict

def make_hangman(secret_word):
    guesses = []
    hidden = len(secret_word) * ["_"]
    idx_dictionary = defaultdict(list)
    for idx, letter in enumerate(secret_word):
            idx_dictionary[letter].append(idx)
    def hangman_closure(guess):
        guesses.append(guess)
        temp = idx_dictionary.get(guess)
        if temp:
            for idx in temp:
                hidden[idx] = guess
                del idx_dictionary[guess]
        print("".join(hidden))
        if len(idx_dictionary) == 0:
            print("Yay you won!")
            return True
        else:
            print("Try again!")
            return False
    return hangman_closure

def play_hangman():
    secret = input("Please provide a secret word to guess! ")
    game = make_hangman(secret)
    game_state = False
    while game_state is False:
        guess = input("Please guess a letter! ")
        while len(guess) > 1 or not guess.isalpha():
            guess = input("Please provide a valid guess, only a letter! ")
        game_state = game(guess)
        
play_hangman()
        