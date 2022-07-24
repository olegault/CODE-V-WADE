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

                # Select the app urls by run id and process id.
                cursor.execute(sql_statements.select_cleaned_policy)

                # Fetch all app urls.
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
            policy_list.append({
                'id': row['id'],
                'app_id': row['app_id'],
                'policy_url': row['policy_url'],
            })

            # For the first ten rows log the url information.
            if row_count <= 10:
                self.logger.info("Row #%d  Policy ID = %s",
                                 row_count, row['id'])

        self.logger.info("Row count = %d,  number of rows in policy ID list = %d", row_count, len(policy_list))

        return policy_list
    
    def get_classified_app_ids(self):
        """Method to get the list of classified policy entries.
        :return: a list of policy IDs from the policy database.
        """
        # Get a database connection.
        database_connection = Database().get_database_connection()

        # Try with the database connection as a resource.
        with database_connection:

            with database_connection.cursor() as cursor:

                # Select the App IDs for cleaned policies.
                cursor.execute(sql_statements.select_classified_policy_app_ids)

                # Fetch all app urls.
                result_rows = cursor.fetchall()

        # Initialize an app ID list.
        app_list = []

        # Initialize a row counter.
        row_count = 0

        self.logger.info("Extracting Previously Cleaned Policy App IDs.")

        # For each row in the result rows.
        for row in result_rows:

            # Increment the row counter.
            row_count += 1

            # Append the Policy's App ID ID to the Policy list
            app_list.append(row['app_id'])

            # For the first ten rows log the url information.
            if row_count <= 10:
                self.logger.info("Row #%d  App ID = %s",
                                 row_count, row['app_id'])

        app_list = set(app_list)

        self.logger.info("Row count = %d,  number of rows in already cleaned App ID list = %d", row_count, len(app_list))

        return app_list


