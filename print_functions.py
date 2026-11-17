import json
import os
import random
import shutil
import sys
import traceback
from datetime import timedelta

from fancycli.user_input import get_user_choice

# Global flag to control interactive wait on errors in CLI printing
# Set to False by default to avoid NameError and unintended prompts
WAIT_ON_ERRORS = False


def _stdout_is_journal() -> bool:
    """True when stdout goes straight into the systemd journal (e.g. running as a systemd service).

    systemd sets JOURNAL_STREAM to "<device>:<inode>" of the journal stream; comparing it to stdout's
    own device and inode avoids false positives when a child of a service has its stdout redirected elsewhere.
    """
    journal_stream = os.environ.get("JOURNAL_STREAM")
    if not journal_stream:
        return False
    try:
        stat = os.fstat(sys.stdout.fileno())
    except (OSError, ValueError):  # stdout replaced by something without a file descriptor
        return False
    return journal_stream == f"{stat.st_dev}:{stat.st_ino}"


TO_JOURNAL = _stdout_is_journal()

# journald reads a "<N>" prefix at the start of a line as its syslog priority; 3 is "err"
JOURNAL_ERROR_PREFIX = "<3>"


class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    CYAN = "\033[36m"
    BOLD = "\033[1m"


if TO_JOURNAL:
    # escape codes make journalctl show the whole line as "[N B blob data]"
    for _name in ("RESET", "RED", "GREEN", "CYAN", "BOLD"):
        setattr(Colors, _name, "")


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


FACE_EMOJIS = []


def print_celebration(message: str | None = None):
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
    stack_str = "".join(traceback.format_exception(exception)) if exception else None

    if TO_JOURNAL:
        # one journal entry per line, each tagged as an error so `journalctl -p err` finds it
        lines = [f"{emojis}  {message}  {emojis}"] + (stack_str.rstrip("\n").splitlines() if stack_str else [])
        print("\n".join(JOURNAL_ERROR_PREFIX + line for line in lines))
    else:
        print()  # flush out any fancy shit going on in the console
        print(f"{Colors.RED}{emojis}  {message}  {emojis}{Colors.RESET}")
        if stack_str:
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


def print_pretty_json(obj):
    j = json.dumps(obj, indent=2, sort_keys=True, default=str)
    print_line(j)
