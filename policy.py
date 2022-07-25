import json
import random
import sql_statements
import utilities
from database import Database
from datetime import datetime
from time import sleep
import data_processing as dp
from cnn import CNN


class Policy:
    """Class that manages processing an app."""

    def __init__(self, logger, models, dictionary, policy_id, policy_text, policy_html):
        """Method to initialize the App class."""

        # Setup the logger.
        self.logger = logger

        # Load pretrained classifiers.
        self.models = models

        # Instantiate the policy table ID.
        self.policy_id = policy_id

        # Instantiate the policy plain text.
        self.policy_text = policy_text

        # Instantiate the policy's simple HTML version.
        self.policy_html = policy_html

        # Load existing dictionary
        self.dictionary = dictionary
        
        # Policy Dict for Logger
        self.policy_logger_dict = {
            'id': self.policy_id,
        }

    def add_results_to_database(self, result):
        """Function to add policy classification results to the database.

        :param result: list of results for each segment.
        :return:
        """
        
        self.logger.debug(f'Adding Results to Database: {str(self.policy_logger_dict)}')

        # Establish a database connection
        database_connection = Database().get_database_connection()

        # Try with the database connection as a resource.
        with database_connection:
            with database_connection.cursor() as cursor:

                for segment in result:
                    
                    try:
                        # Insert a row in the segment table.
                        cursor.execute(sql_statements.segment_insert,
                                    (self.policy_id 
                                     , segment['segment_text']
                                     , int('First Party Collection/Use' in segment['main'])
                                     , int('Third Party Sharing/Collection' in segment['main'])
                                     , int('Identifiable' in segment['Identifiability'])
                                     , int('Aggregated or anonymized' in segment['Identifiability'])
                                     , int('Unspecified' in segment['Identifiability'])
                                     , int('Additional service/feature' in segment['Purpose'])
                                     , int('Advertising' in segment['Purpose'])
                                     , int('Analytics/Research' in segment['Purpose'])
                                     , int('Basic service/feature' in segment['Purpose'])
                                     , int('Legal requirement' in segment['Purpose'])
                                     , int('Marketing' in segment['Purpose'])
                                     , int('Merger/Acquisition' in segment['Purpose'])
                                     , int('Personalization/Customization' in segment['Purpose'])
                                     , int('Service operation and security' in segment['Purpose'])
                                     , int('Unspecified' in segment['Purpose'])
                                     , int('Computer information' in segment['Personal Information Type'])
                                     , int('Contact' in segment['Personal Information Type'])
                                     , int('Cookies and tracking elements' in segment['Personal Information Type'])
                                     , int('Demographic' in segment['Personal Information Type'])
                                     , int('Financial' in segment['Personal Information Type'])
                                     , int('Generic personal information' in segment['Personal Information Type'])
                                     , int('Health' in segment['Personal Information Type'])
                                     , int('IP address and device IDs' in segment['Personal Information Type'])
                                     , int('Location' in segment['Personal Information Type'])
                                     , int('Personal identifier' in segment['Personal Information Type'])
                                     , int('Social media data' in segment['Personal Information Type'])
                                     , int('Survey data' in segment['Personal Information Type'])
                                     , int('User online activities' in segment['Personal Information Type'])
                                     , int('User profile' in segment['Personal Information Type'])
                                     , int('Unspecified' in segment['Personal Information Type'])
                                    ))
                    except Exception as attr_predict_exception:
                                    self.logger.info(f'Failed to process policy ID = {self.policy_id}', exc_info=attr_predict_exception)
                                    raise 'An exception occurred: {}'.format(attr_predict_exception)

                # Commit to save changes.
                database_connection.commit()
        
        self.logger.debug(f"Added Policy with Policy ID {self.policy_id} to the database.")
                


    def process_policy(self):
        
        self.logger.debug(f'Merging Lists: {str(self.policy_logger_dict)}')
        # Preprocess the Policy Text.
        # Merge lists back to previous paragraph.
        self.policy_text = utilities.merge_lists(self.policy_text)
        
        self.logger.debug(f'Filtering Headings: {str(self.policy_logger_dict)}')
        # Remove header-related text
        self.policy_text = utilities.filter_out_headings(self.policy_text, self.policy_html)
        
        try: 
            self.logger.debug(f'Creating Policy Segments: {str(self.policy_logger_dict)}')
            # Vectorize policy segments
            segments_tensor = dp.process_policy_of_interest(self.dictionary , self.policy_text)
        except BaseException as segment_tensor_exception:
            raise Exception(f"Exception while creating segment tensor. Error Message: {segment_tensor_exception}")

        self.logger.debug(f'Making Category Predictions: {str(self.policy_logger_dict)}')
        # Make predictions using the CNN model
        predictions = self.models['Main']['model'](segments_tensor)

        # Filter predictions to include labels with >50% probability
        y_pred = predictions > 0.5

        result = []

        # Append result for each segment to the result list
        for result_row in range(len(self.policy_text)):
            # Extract segment text.
            segment_text = self.policy_text[result_row]

            # Initialize main label classification to empty.
            main_labels = []

            # Initialize attribute label list to empty.
            attribute_labels = []

            # Extract main label predictions for current segment.
            predictedValues = y_pred[result_row, :]

            # Parse main label classifications and add to the main_labels list.
            for label in range(12):
                if predictedValues[label] == True:
                    main_labels.append(self.models['Main']['labels'][label])

            # Proceed if current segment includes any main labels.
            if(len(main_labels) > 0):

                # Instantiate result dictionary for current segment
                current_segment = {
                    'segment_text': segment_text,
                    'main': main_labels
                }

                # If any attribute needs to be classified, proceed individually.
                if ('First Party Collection/Use' in main_labels or 'Third Party Sharing/Collection' in main_labels):

                    segment_tensor = dp.process_policy_of_interest(dictionary, [segment_text,])

                    for attribute in ['Identifiability', 'Purpose', 'Personal Information Type']:
                        
                        self.logger.debug(f'Making {attribute} Predictions: {str(self.policy_logger_dict)}')

                        # Instantiate attribute model.
                        attribute_model = self.models[attribute]['model']

                        # Instantiate attribute labels dict as a list.
                        attribute_labels = self.models[attribute]['labels']
                        
                        attribute_results = []
                        attribute_predictions = attribute_model.predict_proba(segment_tensor)
                        attribute_predictions = attribute_predictions > 0.5
                        attribute_predictions = attribute_predictions[0, :]
                        for attribute_label_index in range(len(attribute_labels)):
                            if attribute_predictions[attribute_label_index] == True:
                                attribute_results.append(attribute_labels[attribute_label_index])

                        # If any labels have been classified, add them to the dict.
                        current_segment[attribute]= attribute_results
                    
                # Append the results of the current segment to the results for the policy.
                result.append(current_segment)
        
        self.logger.debug(f"Classified policy with Policy ID {self.policy_id}. Adding to the database now.")
        
        # Add policy classification results to the database.
        self.add_results_to_database(result)


    

