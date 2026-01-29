import random
import shutil
import sys
from datetime import timedelta


# Global flag to control interactive wait on errors in CLI printing
# Set to False by default to avoid NameError and unintended prompts
WAIT_ON_ERRORS = False


class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"


def print_line(message: str):
    print(message)


def print_headline(message, border_char="*"):
    """Print a headline with a border across the screen width."""

    def _repeat_to_width(char):
        """Repeat a character to fill the terminal width."""
        width = shutil.get_terminal_size((80, 20)).columns
        return char * width

    border = _repeat_to_width(border_char)
    print(border)
    print(Colors.BOLD + message.center(len(border)) + Colors.RESET)
    print(border)


def format_timedelta(td: timedelta) -> str:
    total_ms = td.total_seconds() * 1000
    total_s = td.total_seconds()
    total_m = total_s / 60
    total_h = total_s / 3600

    if total_s < 1:
        return f"{total_ms:.0f}ms"
    elif total_s < 60:
        return f"{total_s:.2f}s"
    elif total_s < 3600:
        minutes = int(total_m)
        seconds = int(total_s % 60)
        return f"{minutes}m:{seconds}s"
    else:
        hours = int(total_h)
        minutes = int(total_m % 60)
        return f"{hours}h:{minutes}m"


def print_celebration(message: str = None):
    emojis = [
        "🎉", "✨", "🥳", "🎊", "💯", "🚀", "🌟", "🎶", "🎈", "🔥",
        "🙌", "🍾", "😁", "👏", "🌈", "💎", "🎂", "🍀", "🌍", "💃",
        "🏍️", "😎", "💦", "🥂", "🪅", "🎁", "😄", "🤗"
    ]
    # pick 15 emojis per line, allowing repeats
    line1 = "".join(random.choice(emojis) for _ in range(15))
    line2 = "".join(random.choice(emojis) for _ in range(15))

    print("\n" + line1)
    if message:
        print(message)
    print(line2 + "\n")


def print_error(message, exception=None, allow_wait: bool = True):
    """Print an error with random emojis and red text."""
    emojis = " ".join(random.sample(["❌",
                                     "🚫",
                                     "💥",
                                     "😡",
                                     "⚠️",
                                     "🔥",
                                     "🤯"], k=3))
    print()  # flush out any fancy shit going on in the console
    print(f"{Colors.RED}{emojis}  {message}  {emojis}{Colors.RESET}")
    stack_str = None
    if exception:
        # You can format this however your CLI class handles output
        import traceback
        stack_str = traceback.format_exc()
        print(stack_str)

    # If wait_on_errors is enabled, prompt user for action
    if WAIT_ON_ERRORS and allow_wait:
        print(f"{Colors.CYAN}Error encountered. What would you like to do?{Colors.RESET}")
        choice = get_user_choice(["Continue program execution", "Exit program"])
        if choice == "Exit program":
            print(f"{Colors.RED}Exiting program as requested.{Colors.RESET}")
            sys.exit(1)
        else:
            print(f"{Colors.GREEN}Continuing program execution...{Colors.RESET}")

    return f"{message} {stack_str}" if stack_str else message


def print_success(message):
    emojis = ["🎉", "🥳", "😎", "🎇",
              "✨", "💥", "🔥", "🎊", "🪅", "🎶", "💃",
              "🎈", "🪩", "🍰", "🏍️", "🍹", ]
    """Print a celebration message with random party emojis."""
    emojis_start = "".join(random.sample(emojis, k=4))
    emojis_end = "".join(random.sample(emojis, k=4))
    print(f"{Colors.GREEN}{emojis_start}  {message}  {emojis_end}{Colors.RESET}")
