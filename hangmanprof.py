import random  # import random library
import time

class Hangman:
    def __init__(self):
        # Read the word list from the file
        with open("sowpods.txt", "r") as file:
            word_list = file.read().splitlines()
        
        # Choose a random word from the word list
        self.word = random.choice(word_list).upper()
        
        # Set of letters to guess in the word
        self.letters_to_guess = set(self.word)
        
        # Set of correct letters guessed by the user
        self.correct_letters_guessed = set()
        
        # Set of incorrect letters guessed by the user
        self.incorrect_letters_guessed = set()
        
        # Number of remaining guesses
        self.num_guesses = 8
        
        # Start time of the game
        self.start_time = time.time()

    def ask_user_for_next_letter(self):
        # Prompt the user to guess a letter
        letter = input("Guess a letter: ")
        return letter.strip().upper()  # Stripping away spaces and keeping letters in upper case

    @staticmethod
    def pick_random_word():
        # This function picks a random word from the SOWPODS dictionary.
        # Open the sowpods dictionary as a text file in readable format
        with open("sowpods.txt", 'r') as f:  # 'r' stands for read instead of write
            words = f.readlines()

        # Generate a random index
        # -1 because len(words) is not a valid index into the list `words`
        index = random.randint(0, len(words) - 1)

        # Print out the word at that index
        # The .strip() function removes all trailing spaces before and after the word
        word = words[index].strip()
        return word

    def generate_word_string(self):
        # Generate a string representation of the word with correct letters filled in
        output = []
        for letter in self.word:
            if letter in self.correct_letters_guessed:
                output.append(letter.upper())
            else:
                output.append("_")
        return " ".join(output)

    def draw_hangman(self):
        # Method to draw the hangman based on the number of remaining guesses
        graphics = [
            '''_____
|/  |
|   O
|  /|\\
|  / \\
|''',
            '''_____
|/  |
|   O
|  /|\\
|  / \\
|''',
            '''_____
|/  |
|   O
|  /|\\
|  /
|''',
            '''_____
|/  |
|   O
|  /|\\
|
|''',
            '''_____
|/  |
|   O
|  /|
|
|''',
            '''_____
|/  |
|   O
|   |
|
|''',
            '''_____
|/  |
|   O
|
|
|''',
            '''_____
|/  |
|
|
|
|''',
            ''
        ]
        print(graphics[self.num_guesses])

    def play(self):
        print("Welcome to Hangman! We have picked a word, now it's your time to guess!")
        NO_GUESSES_LEFT = 0
        while (len(self.letters_to_guess) > 0) and self.num_guesses > NO_GUESSES_LEFT:
            guess = self.ask_user_for_next_letter()

            if not guess.isalpha():
                print("Invalid guess. Please enter a letter.")
                continue

            if guess in self.correct_letters_guessed or guess in self.incorrect_letters_guessed:
                print("You already guessed that letter.")
                continue

            if guess in self.letters_to_guess:
                self.letters_to_guess.remove(guess)
                self.correct_letters_guessed.add(guess)
            else:
                self.incorrect_letters_guessed.add(guess)
                self.num_guesses -= 1

            word_string = self.generate_word_string()
            print(word_string)
            print(f"You have {self.num_guesses} guesses left")
            self.draw_hangman()

        if self.num_guesses > NO_GUESSES_LEFT:
            print(f"Congratulations! You correctly guessed the word {self.word}")
        else:
            print(f"Sorry, you lost! Your word was {self.word}")

class UserData:
    def __init__(self, username):
        # Initialize the UserData object with a username and an empty data list
        self.username = username
        self.data = []

    def read_data_from_file(self, filename):
        # Read data from a file and store it in the data list
        with open(filename, "r") as file:
            self.data = file.read().splitlines()

    def save_data(self, game):
        # Save game data to a file
        end_time = time.time()
        time_used = end_time - game.start_time
        num_guesses = len(game.correct_letters_guessed) + len(game.incorrect_letters_guessed)
        word_guessed = len(game.letters_to_guess) == 0
        with open("userdata.txt", "a") as file:
            file.write(f"{time.asctime()},{self.username},{num_guesses},{time_used},{word_guessed}\n")

username = input("Enter your username: ")
user = UserData(username)
game = Hangman()
game.play()
user.save_data(game)