import random
from json import load
from returns.pipeline import flow, pipe
from returns.pointfree import bind
from returns.io import IO, IOResultE, impure_safe
from returns.result import Result, Success, Failure
from assets import display_hangman


@impure_safe
def get_word() -> str:
    with open('words.json') as json_file:
        data = load(json_file)
    wordArray = data["word_list"]
    return random.choice(wordArray).upper()


def get_initial_state(word: str) -> dict:
    return {
        "word": word, 
        "word_completion": "_" * len(word),
        "guessed_letters": [],
        "guessed_words": [],
        "tries": 6,
        "last_guess_result": "",
    }


@impure_safe
def get_user_input(state: dict) -> str:
        print(display_hangman(state["tries"]))
        print(state["word_completion"])
        print("\n")
        print("Length of the word: ", len(state["word"]))
        print("\n")
        return input("Please guess a letter or the word: ").upper()


def update_state_with_guess(state: dict, guess: str) -> Result[dict, str]:
    def _update_word_completion(state: dict, guess: str) -> str:
        word_as_list = list(state["word_completion"])
        indices = [i for i, letter in enumerate(state["word"]) if letter == guess]
        for index in indices:
            word_as_list[index] = guess
        return "".join(word_as_list)

    def _update_state_for_letter_guess(state: dict, guess: str) -> dict:
        if guess in state["guessed_letters"]:
            state["last_guess_result"] = f"You already guessed the letter {guess}"
        elif guess not in state["word"]:
            state["last_guess_result"] = f"{guess} is not in the word."
            state["tries"] -= 1
            state["guessed_letters"].append(guess)
        else:
            state["last_guess_result"] = f"Good job, {guess} is in the word!"
            state["guessed_letters"].append(guess)
            state["word_completion"] = _update_word_completion(state, guess)
        return state

    def _update_state_for_word_guess(state: dict, guess: str) -> dict:
        if guess in state["guessed_words"]:
            state["last_guess_result"] = f"You already guessed the word {guess}"
        elif guess != state["word"]:
            state["last_guess_result"] = f"{guess} is not the word."
            state["tries"] -= 1
            state["guessed_words"].append(guess)
        else:
            state["last_guess_result"] = f"Good job, {guess} is the word!"
            state["guessed_words"].append(guess)
            word_completion = word
        return state


    if len(guess) == 1 and guess.isalpha():
        return Success(_update_state_for_letter_guess(state, guess))
    elif len(guess) == len(state["word"]) and guess.isalpha():
        return Success(_update_state_for_word_guess(state, guess))
    else:
        return Failure("Not a valid guess.")


def play(initial_state: dict):
    def game_over(state):
        return game_state["word"] == game_state["word_completion"] or game_state["tries"] <= 0 

    game_state = initial_state
    while not game_over(game_state):
        guess = get_user_input(game_state)
        match guess.bind(lambda x: update_state_with_guess(game_state, x)):
            case Success(new_state):
                game_state = new_state
            case Failure(err):
                print(err)

    if game_state["word"] == game_state["word_completion"]:
        print("Congrats, you guessed the word! You win!")
    else:
        print("Sorry, you ran out of tries. The word was " + game_state["word"] + ". Maybe next time!")


# main function to start the game
def main():
    print("Let's play Hangman!")

    play_round_with_word = pipe(
        bind(get_initial_state),
        play
    )

    play_round_with_word(get_word())
    while input("Play Again? (Y/N): ").upper() == "Y":
        play_round_with_word(get_word())


if __name__ == "__main__":
    main()
