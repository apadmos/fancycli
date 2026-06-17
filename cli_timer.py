import datetime

from .print_functions import print_line, format_timedelta


class CLITimer:

    def __init__(self, message: str):
        self.start_time = None
        self.end_time = None
        self.message = message

    def start(self):
        """Start the timer"""
        self.start_time = datetime.datetime.now()
        self.end_time = None

    def stop(self):
        """Stop the timer and calculate elapsed time"""
        if not self.start_time:
            print_line("Timer hasn't been started yet!")
            return None

        self.end_time = datetime.datetime.now()
        elapsed_time = self.end_time - self.start_time

        print_line(
            f"⏲ {self.message} took {format_timedelta(elapsed_time)} started at {self.start_time.strftime('%H:%M:%S.%f')[:-3]} ⏰")
        return elapsed_time

    def __enter__(self):
        """Context manager entry - start timer"""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - stop timer"""
        self.stop()
