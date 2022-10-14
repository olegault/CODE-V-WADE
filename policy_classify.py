#!/usr/bin/python3
import atexit
import concurrent.futures
import requests
import sql_statements
import utilities
from configuration import Configuration
from database import Database
from log import Log
from status_email import StatusEmail
from time import sleep
from time_log import TimeLog, seconds_to_string
from policy_list import PolicyList
import urllib.parse
from nltk.tokenize import sent_tokenize

# Importing values to handle timeout signals. 
import signal
import time
import os

class PolicyClassify:
    """The policy classify class used to process privacy policies."""

    def __init__(self):
        """Method to initialize the PolicyClassify class."""

        # Setup the logger.
        self.logger = Log("privacy_policy_log").logger

        # Chunk status log frequency.
        self.chunk_status_log_frequency = 100

        # Start the elapsed time log.
        self.time_log = TimeLog(self.logger)

        # Register an at exit method to run, when the program exits run the exit method.
        atexit.register(self.onexit)

        self.logger.info("Initializing PolicyClassify.")

        # Get the configuration from the configuration file
        self.configuration = Configuration().get_configuration()

        # Size of the thread pool used for processing privacy policies.
        self.thread_pool_size = self.configuration["program"]["threadPoolSize"]

        # Size of the chunks to split the policy list into for processing.
        self.policy_list_chunk_size = self.configuration["program"]["policyListChunkSize"]

        # Size of the chunks to split the policy list into for processing.
        self.error_policy_list_chunk_size = self.configuration["program"]["errorPolicyListChunkSize"]

        # Sleep time between chunks in seconds.
        self.sleep_time_between_chunk_processing_in_seconds \
            = self.configuration["program"]["sleepTimeBetweenChunkProcessingInSeconds"]

        # The process id for the node currently running the program.
        self.process_id = self.configuration["program"]["processingNodeId"]

        # Initialize an policy error list for processing later.
        self.policies_with_errors_during_processing = []

        # Retrieve Pre-trained models.
        # self.models = Model(self.logger).get_additional_models()

        # Retrieve the Policy list.
        self.policy_list = PolicyList(self.logger).get_policies()

        # Retrieve IDs for previously cleaned policies
        # self.classified_policy_ids = PolicyList(self.logger).get_classified_policy_ids()
        self.classified_policy_ids = []

        # Retrieve dictionary for word embeddings
        # self.dictionary = Model(self.logger).get_dictionary()

        # Statistical variables to keep track of the total number of processed policies, and errors.
        self.total_number_of_empty_policies = 0
        self.empty_policies_list = []
        self.total_number_of_small_policies = 0
        self.small_policies_list = []
        self.total_number_of_policies_classified = 0
        self.total_number_of_small_or_empty_policies = 0
        self.total_number_of_errors = 0
    
    def timeout_handler(self, num, stack):
        """
        Method to raise an exception when policy classification takes too long to return.
        Creating this to avoid the process from getting killed.
        Ref: https://medium.com/@chamilad/timing-out-of-long-running-methods-in-python-818b3582eed6 
        
        
        """
        print("Received SIGALRM")
        raise Exception("FUBAR")

    
    def safe_process_policy(self, policy_id):
        """Method to process a policy within a try block so that processing may continue in case of error.
           Safely call the process policy function.

        :param policy: A dict containing the ID of the policy from the raw_policy database.   
        """
        
        self.logger.debug(f'Starting Processing Policy ID: {str(policy_id)}')
        

        (policy_text, policy_html) = utilities.get_policy_text(policy_id)
        
        if (policy_text == ''):
            self.total_number_of_empty_policies += 1
            self.total_number_of_small_or_empty_policies += 1
            self.empty_policies_list.append(policy_id)
            self.logger.debug(f'Policy Empty: id: {str(policy_id)}')
            return
    
        policy_text = policy_text.splitlines()
            
        # If readabability couldn't divide the policy into segments, it's possible they have just 1 or 2 long segments.
        if (len(policy_text) < 3):

            # Flatten the list
            flattened_list = [item for sublist in policy_text for item in sublist]

            flattened_string = '\n'.join(flattened_list)

            policy_text = sent_tokenize(flattened_string)
                
        # If the policy is small despite sentence tokenization, then skip it.    
        if (len(policy_text) < 3):
                
            if (len(policy_text) == 0):
                self.total_number_of_empty_policies += 1
                self.empty_policies_list.append(policy_id)
            else:
                self.total_number_of_small_policies += 1
                self.small_policies_list.append(policy_id)

            self.logger.debug(f'Policy Too Small: id: {str(policy_id)}')

            # Increment the total number of small found.
            self.total_number_of_small_or_empty_policies += 1

            # Append the policy ID to the policies with errors during processing list.
            self.policies_with_errors_during_processing.append(policy_id)
            
        return


    def process_policy_list_chunk(self, policy_list_chunk):
        """Method to process policy list chunks using a thread pool.
        
        : param policy_list_chunk: A policy list chunk.
        """

        self.logger.info(f'Processing a policy list chunk of size: {len(policy_list_chunk)}')
        
        for policy in policy_list_chunk:
            
            # Initializing Signal to raise an ALARM when the policy processing has taken longer than 2 mins.
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(120)
            
            try:
                self.safe_process_policy(policy)
                
            except Exception as ex:
                if "FUBAR" in ex:
                    self.logger.debug(f'Took too long to process policy. Hence, timeout exception raised. {str(policy)}.', exc_info=ex)
                    
            finally:
                signal.alarm(0)
            
            self.logger.debug(f'Processed policy: {str(policy)}')



    def process_policy_list(self):
        """Method to process the policy list."""
        self.logger.info("Processing a policy list of size: %d", len(self.policy_list))

        # Initiaize a chunk counter.
        chunk_counter = 0

        # Split the policy list into chunks.
        for chunked_list in utilities.split_list_into_chunks(self.policy_list, self.policy_list_chunk_size):
            
            # Process the individual policy list chunks.
            self.process_policy_list_chunk(chunked_list)

            # Increment the chunk counter.
            chunk_counter += 1

            # Log status every certain number of chunks processed.
            if chunk_counter % self.chunk_status_log_frequency == 0:

                # Log the program status information.
                self.logger.info(self.build_status_information_string())

    
    def build_status_information_string(self):
        """Method to build the status information string for logging and emailing status information."""
        
        with open('small-policies.txt', 'w') as fp:
            for item in self.small_policies_list:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')
            
        with open('empty-policies.txt', 'w') as fp:
            for item in self.empty_policies_list:
                # write each item on a new line
                fp.write("%s\n" % item)
            print('Done')

        # Create a log line of 40 equals signs.
        line = "=" * 40

        # Create a new line
        newline = "\n"

        # Build the status string.
        status = newline \
            + "UIC Apple App Small and Empty Policy Detection Status" + newline \
            + line + newline \
            + "Start time: " + self.time_log.start_program_time_string + newline \
            + "Current time: " + seconds_to_string() + newline \
            + "Elapsed time: " + self.time_log.calculate_elapsed_time() + newline \
            + "Number of small or empty policies: " + str(self.total_number_of_small_or_empty_policies) + newline \
            + "Number of small policies: " + str(self.total_number_of_small_policies) + newline \
            + "Number of empty policies: " + str(self.total_number_of_empty_policies) + newline \
            + line

        return status 

    def log_program_completion(self):
        """Method to log status at the end of the program."""
        
        # Log the program status information.
        self.logger.info(self.build_status_information_string())

    def send_program_status_completion_email(self):
        """Method to email status at the end of the program."""

        # Email message subject.
        subject = "UIC Apple App Privacy Policy Classification Status"

        # Email message body.
        body = self.build_status_information_string()

        # Send the program status email.
        StatusEmail().send_email(subject, body)

    def onexit(self):
        """Method that will run on program exit, used for logging and status emails."""
        
        # Write the program results to the log.
        self.log_program_completion()

        # Send an email when the program has completed that will contain the result details of the program run.
        self.send_program_status_completion_email()


    def main(self):
        """The main method for the PolicyClean class. Calls the process_policy_list method."""

        # Process the Policy list.
        self.process_policy_list()


# '__main__' is the name of the scope in which top-level code executes.
# A module’s __name__ is set equal to '__main__' when read from standard input, a script, or from an interactive prompt.
if __name__ == "__main__":
    PolicyClassify().main()