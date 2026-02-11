import random

def play_game():
    """One round of the guessing game."""

    secret_number = random.randint(1, 100)
    max_attempts = 7
    attempts = 0

    print("\n I'm thinking of a number between 1 and 100.")
    print(f" You have {max_attempts} attemps. Good luck!\n")

    while attempts < max_attempts:
        attempts += 1
        print(f"Attempt {attempts}/{max_attempts}")
        try:
            guess = int(input("Your guess: "))
        except ValueError:
            print("Please enter a valud number!\n")
            attempts -= 1
            continue
        
        if guess < 1 or guess > 100:
            print("Pick a number between 1 and 100!\n")
            attempt -= 1
            continue
        elif guess < secret_number:
            print("Too low")
        elif guess > secret_number:
            print("Too high")
        else:
            print(f"\nYou got it! The number was {secret_number}!")
            print(f" It took you {attempts} attempt(s).\n")
            return
    
    print(f"\n Out of attempts! The number was {secret_number}.\n")

def main():
    print("=" * 40)
    print(" WELCOME TO THE NUMBER GUESSING GAME")
    print("=" * 40)

while True:
    play_game()

    again = input("Play again? (yes/no)").lower()

    if not again.startswith("y"):
        print("\nThanks for playing! Goodbye!")
        break

if __name__ == "__main__":
    main()