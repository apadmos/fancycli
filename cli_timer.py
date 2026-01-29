import datetime

from subs.fancy_cli import print_line


class CLITimer:

    def __init__(self, message: str):
        self.start_time = None
        self.end_time = None
        self.message = message

    def start(self):
        """Start the timer"""
        self.start_time = datetime.datetime.now()
        self.end_time = None
        print_line(f"{self.message} started at {self.start_time.strftime('%H:%M:%S.%f')[:-3]}")

    def stop(self):
        """Stop the timer and calculate elapsed time"""
        if not self.start_time:
            print_line("Timer hasn't been started yet!")
            return None

        self.end_time = datetime.datetime.now()
        elapsed_time = self.end_time - self.start_time

        print_success(f"{self.message} time {format_timedelta(elapsed_time)}")
        return elapsed_time

    def __enter__(self):
        """Context manager entry - start timer"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - stop timer"""
        self.stop()
