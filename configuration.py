import json


class Configuration:
    """Configuration class for storing configuration info.

    The configuration class will read the configuration JSON file and make the config object available.
    """

    def __init__(self):
        """Method to initialize the Config class."""

        # Read the configuration file.
        with open("config_file.json") as config_file:
            self.configuration = json.load(config_file)

    def get_configuration(self):
        """Method to return the config object"""
        return self.configuration
