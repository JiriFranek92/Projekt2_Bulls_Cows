from random import sample

while True:
    secret_num = [str(item) for item in sample(range(0, 10), 4)]
    if secret_num[0] != '0':
        break

# print(secret_num)

n_guesses = 0

while True:
    counter = {"bull": 0, "cow": 0}

    guess = input(">>> ")

    # zkontroluj vstupní hodnoty
    if not guess.isnumeric():
        print("Guess must be a number!")
        continue
    elif not len(guess) == 4:
        print("Guessed number must be 4 digits long!")
        continue
    elif guess[0] == '0':
        print("Guessed number must not start with a 0!")
        continue
    elif sum([guess.count(dig) for dig in guess]) != 4:
        print("Each digit must be unique!")
        continue

    n_guesses += 1

    # vyhodnoť tip, zapiš do počítadla
    for i, digit in enumerate(guess):
        if digit in secret_num:
            if secret_num[i] == digit:
                counter["bull"] += 1
            else:
                counter["cow"] += 1

    # vypiš verdikt
    verdict = ""
    for key, value in counter.items():
        verdict += f"{value} {key} " if value == 1 else f"{value} {key}s "
    print(verdict)

    if counter["bull"] == 4:
        print(f"Great Success! {n_guesses} guesses.")
        break
