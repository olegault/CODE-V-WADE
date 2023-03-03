import logging
from configuration import Configuration
from time import strftime


class Log:
    """"Log class to provide logging setup and ability to retrieve the logger after it is setup."""

    def __init__(self, log_name):
        """Method to initialize the Log class and configure the logger.

        :param log_name: The name of this log.
        """

        # Get the configuration from the configuration file.
        self.configuration = Configuration().get_configuration()

        # The time the log was created, used to name the log file.
        self.log_time = strftime("%Y_%m_%d-%H_%M_%S")

        # Set the format in the logging configuration.
        logging.basicConfig(
            filename=self.configuration["logging"]["logDirectory"] + log_name + "-" + self.log_time + ".log",
            format=self.configuration["logging"]["logFormat"],
            level=self.configuration["logging"]["logLevel"])

        # Set the logger name.
        self.logger = logging.getLogger()
