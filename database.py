import pymysql.cursors
from configuration import Configuration


class Database:
    """The database class to manage the database connection.

        The database class will open a database connection based on the host and user name in the configuration file.
    """

    def __init__(self):
        """Method to initialize the Database class."""

        # Get the database configuration from the configuration file.
        self.configuration = Configuration().get_configuration()

    def get_database_connection(self):
        """Method to get a database connection."""
        return pymysql.connect(host=self.configuration["mysql"]["host"],
                               user=self.configuration["mysql"]["user"],
                               password=self.configuration["mysql"]["password"],
                               database=self.configuration["mysql"]["database"],
                               cursorclass=pymysql.cursors.DictCursor)
