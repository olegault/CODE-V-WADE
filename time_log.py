import atexit
from datetime import datetime, timedelta
from time import localtime, strftime, time


def seconds_to_string(elapsed=None):
    """Function to convert seconds to a string.

    :param elapsed: The elapsed time between start and stop in seconds.
    :return: The seconds as a string.
    """
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))


class TimeLog:
    """"Class to setup the time logging and provide time logging methods."""

    def __init__(self, logger):
        """Method to initialize the TimeLog class."""

        # Setup the logger.
        self.logger = logger

        # Setup a time format.
        self.time_format = '%Y-%m-%d %H:%M:%S'

        # Initialize the start time variable and start the program timer.
        self.start_time = time()

        # Write the start message to the log.
        self.start_log()

        # Readable start program time string.
        self.start_program_time_string = seconds_to_string()

        # Register the end log function to run at program exit.
        atexit.register(self.end_log)

    def log_start_and_stop_time(self, start_or_end_time_log_label_string, elapsed=None):
        """Method to cleanly log the start and stop time.

        :param start_or_end_time_log_label_string: A string appended to the log stating if this is a start or stop log.
        :param elapsed: The elapsed time between start and stop in seconds.
        """

        # Create a string of 40 equals signs in a row.
        line = "=" * 40

        # Log a line of 40 equals signs to clarify the start of this log event.
        self.logger.info(line)

        # Log the current time or the
        self.logger.info(seconds_to_string() + '-' + start_or_end_time_log_label_string)

        if elapsed:
            self.logger.info("Elapsed time: " + elapsed)

        # Log a line of 40 equals signs to clarify the end of this log event.
        self.logger.info(line)

    def calculate_elapsed_time(self):
        """Method to calculate the elapsed time."""

        # The end time.
        end = time()

        # Calculate the elapsed time.
        elapsed_time = end - self.start_time

        return seconds_to_string(elapsed_time)

    def start_log(self):
        """Method to log the start of the program."""
        self.log_start_and_stop_time("Start Program")

    def end_log(self):
        """Method to log the end of the program."""

        # Log the start and stop times, including the elapsed time.
        self.log_start_and_stop_time("End Program", self.calculate_elapsed_time())

    def get_start_time(self):
        """Method to return a formatted start time."""
        return datetime.fromtimestamp(self.start_time).strftime(self.time_format)

    def get_end_time(self):
        """Method to return a formatted end time."""
        return datetime.fromtimestamp(time()).strftime(self.time_format)
