from .cli_progress_session import CLIProgressSession
from .cli_timer import CLITimer


def timer(message: str):
    return CLITimer(message=message)


def progress_session(total_count: int = None):
    return CLIProgressSession(total_count=total_count)

from print_functions import print_line, print_error, print_success



