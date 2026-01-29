def get_user_choice(options):
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_user_string(prompt: str, default: str = None) -> str:
    while True:
        try:
            if default:
                prompt = f"{prompt} (default: {default}): "
            choice = input(prompt)
            if not choice and default:
                choice = default
            if choice:
                return str(choice).strip()
        except ValueError:
            print("Invalid input")


def get_user_confirmation(question:str, full_word:bool=True) -> bool:
    while True:
        try:
            answer = str(input(question)).lower().strip()
            if full_word:
                if answer == "yes":
                    return True
                if answer == "no":
                    return False
            else:
                if answer[0] == "y":
                    return True
                if answer[0] == "n":
                    return False
        except:
            if full_word:
                print("Invalid input. Please enter yes or no.")
            else:
                print("Invalid input. Please a word that starts with Y or N")
