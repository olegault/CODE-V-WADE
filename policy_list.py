import sql_statements
import utilities
from configuration import Configuration
from database import Database
from urllib.parse import unquote


class PolicyList:
    """Class used to provide method for operating on a list of urls from the database."""

    def __init__(self, logger):
        """Method to initialize the URL list class."""

        # Setup the logger
        self.logger = logger

        # Get the configuration from the configuration file.
        self.configuration = Configuration().get_configuration()

    def get_policies(self):
        """Method to get the list of uncleaned policy entries.
        :return: a list of policy IDs for the current run id and node process id.
        """

        # Get a database connection.
        database_connection = Database().get_database_connection()

        # Try with the database connection as a resource.
        with database_connection:

            with database_connection.cursor() as cursor:

                # Select the policies by Policy ID.
                cursor.execute(sql_statements.select_cleaned_policies)

                # Fetch all Policy IDs.
                result_rows = cursor.fetchall()

        # Initialize an policy list.
        policy_list = []

        # Initialize a row counter.
        row_count = 0

        # For each row in the result rows.
        for row in result_rows:

            # Increment the row counter.
            row_count += 1

            # Append the Policy ID to the Policy list
            policy_list.append(row['id'])

            # For the first ten rows log the url information.
            if row_count <= 10:
                self.logger.info("Row #%d  Policy ID = %s",
                                 row_count, row['id'])

        self.logger.info("Row count = %d,  number of rows in policy ID list = %d", row_count, len(policy_list))

        return policy_list
    
    def get_classified_policy_ids(self):
        """Method to get the list of classified policy entries.
        :return: a list of policy IDs from the policy database.
        """
        # Get a database connection.
        database_connection = Database().get_database_connection()

        # Try with the database connection as a resource.
        with database_connection:

            with database_connection.cursor() as cursor:

                # Select the Policy IDs for cleaned policies.
                cursor.execute(sql_statements.select_classified_policy_ids)

                # Fetch all Policy IDs.
                result_rows = cursor.fetchall()

        # Initialize an policy ID list.
        policy_list = []

        # Initialize a row counter.
        row_count = 0

        self.logger.info("Extracting Previously Cleaned Policy IDs.")

        # For each row in the result rows.
        for row in result_rows:

            # Increment the row counter.
            row_count += 1

            # Append the Policy ID to the Policy list
            policy_list.append(row['policy_id'])

            # For the first ten rows log the url information.
            if row_count <= 10:
                self.logger.info("Row #%d  Policy ID = %s",
                                 row_count, row['policy_id'])

        policy_list = set(policy_list)

        self.logger.info("Row count = %d,  number of rows in already cleaned Policy ID list = %d", row_count, len(policy_list))

        return policy_list


