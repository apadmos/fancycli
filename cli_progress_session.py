import datetime
import sys

from .env import FANCY_VERBOSE
from .print_functions import format_timedelta, print_celebration


class CLIProgressSession:
    def __init__(self, total_count=None,
                 length: int = 20,
                 throb_length: int = 20):
        self.started: datetime.datetime = None
        self.completed_count: int = -1
        self.elapsed = None
        self.total_count = total_count
        # rendering options/state
        self.length = length
        self.throb_length = throb_length
        self.succinct = not FANCY_VERBOSE
        self._last_filled: int | None = None
        self._dot_count: int = 0
        self._last_throb_render: datetime.datetime | None = None

    def start(self):
        self.started = datetime.datetime.now()
        self.completed_count = 0
        self.elapsed = datetime.timedelta()
        self.print(increment=0, completed=0)

    def update_total_count(self, new_count):
        self.total_count = new_count

    def _render_throb(self, message: str = ""):
        # Only render every minute when in succinct mode
        if self.succinct:
            now = datetime.datetime.now()
            if self._last_throb_render and (now - self._last_throb_render).total_seconds() < 60:
                return
            self._last_throb_render = now

        # Make it cycle continuously
        filled = self.completed_count % (self.throb_length + 1)
        bar = "🙂" * filled + "🫥" * (self.throb_length - filled)

        if self.elapsed and self.completed_count:
            average = self.elapsed / self.completed_count
            average_str = format_timedelta(average)
            elapsed_str = f" ⏱️ {str(self.elapsed).split('.')[0]} {average_str}/item"
        else:
            elapsed_str = ""

        sys.stdout.write(f"\r{bar} ({self.completed_count}){elapsed_str} {message}")
        sys.stdout.flush()

    def _render_bar(self, message: str = ""):
        total = self.total_count or 0
        if total <= 0:
            print("❌ Invalid total")
            return

        completed = self.completed_count
        if completed > total:
            total = completed

        perc = float(completed) / float(total) if total else 0.0
        filled = int(self.length * perc)

        if self.elapsed and completed:
            average = self.elapsed / completed
            remaining = average * (total - completed)
            average_str = format_timedelta(average)
            elapsed_str = f" ⏱️ {str(self.elapsed).split('.')[0]} {average_str}/item"
            remaining_str = f" ⏳ {format_timedelta(remaining)} left"
        else:
            elapsed_str = ""
            remaining_str = ""

        should_render = (not self.succinct) or (self._last_filled != filled)
        if should_render:
            bar = "🙂" * filled + "🫥" * (self.length - filled)
            output = f"{bar}{perc * 100:.2f}% ({completed}/{total}){elapsed_str} {remaining_str} {message}"
            self._last_filled = filled
            sys.stdout.write(f"\x1b[2K\r{output}")
            sys.stdout.flush()
            self._dot_count = 0
        else:
            pass
            """self._dot_count += 1
            sys.stdout.write(".")
            sys.stdout.flush()"""

    def print(self, message=None, increment=1, completed=0):
        if not message:
            message = ""

        if completed:
            self.completed_count = completed
        elif increment:
            self.completed_count += increment

        self.elapsed = datetime.datetime.now() - self.started

        if self.total_count and self.total_count > 0:
            self._render_bar(message=message)
        else:
            self._render_throb(message=message)

    def end(self):
        if not self.elapsed or self.completed_count < 1:
            print("No action taken")
            return
        average = self.elapsed / self.completed_count
        average = format_timedelta(average)
        print_celebration(
            f"{self.completed_count} completed items.\n{self.elapsed} total time\n {average} per item")

    def __enter__(self):
        """Context manager entry - start timer"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - stop timer"""
        self.end()
