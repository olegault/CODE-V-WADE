import json
import random
import sql_statements
import utilities
from database import Database
from datetime import datetime
from time import sleep
import data_processing as dp
from cnn import CNN


class Segment:
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
                        cursor.execute(sql_statements.large_segment_insert,
                                    (self.policy_id
                                        , int('First Party Collection/Use' in segment['main'])
                                        , int('Third Party Sharing/Collection' in segment['main'])
                                        , int('User Access, Edit and Deletion' in segment['main'])
                                        , int('Data Retention' in segment['main'])
                                        , int('Data Security' in segment['main'])
                                        , int('International and Specific Audiences' in segment['main'])
                                        , int('Do Not Track' in segment['main'])
                                        , int('Policy Change' in segment['main'])
                                        , int('User Choice/Control' in segment['main'])
                                        , int('Introductory/Generic' in segment['main'])
                                        , int('Practice not covered' in segment['main'])
                                        , int('Privacy contact information' in segment['main'])
                                        , int('Does' in segment['Does or Does Not'])
                                        , int('Does Not' in segment['Does or Does Not'])
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
                                        , int('Stated Period' in segment['Retention Period'])
                                        , int('Limited' in segment['Retention Period'])
                                        , int('Indefinitely' in segment['Retention Period'])
                                        , int('Unspecified' in segment['Retention Period'])
                                        , int('Advertising' in segment['Retention Purpose'])
                                        , int('Analytics/Research' in segment['Retention Purpose'])
                                        , int('Legal requirement' in segment['Retention Purpose'])
                                        , int('Marketing' in segment['Retention Purpose'])
                                        , int('Perform service' in segment['Retention Purpose'])
                                        , int('Service operation and security' in segment['Retention Purpose'])
                                        , int('Unspecified' in segment['Retention Purpose'])
                                        , int('General notice in privacy policy' in segment['Notification Type'])
                                        , int('General notice on website' in segment['Notification Type'])
                                        , int('No notification' in segment['Notification Type'])
                                        , int('Personal notice' in segment['Notification Type'])
                                        , int('Unspecified' in segment['Notification Type'])
                                        , int('Generic' in segment['Security Measure'])
                                        , int('Data access limitation' in segment['Security Measure'])
                                        , int('Privacy review/audit' in segment['Security Measure'])
                                        , int('Privacy training' in segment['Security Measure'])
                                        , int('Privacy/Security program' in segment['Security Measure'])
                                        , int('Secure data storage' in segment['Security Measure'])
                                        , int('Secure data transfer' in segment['Security Measure'])
                                        , int('Secure user authentication' in segment['Security Measure'])
                                        , int('Unspecified' in segment['Security Measure'])
                                        , int('Children' in segment['Audience Type'])
                                        , int('Californians' in segment['Audience Type'])
                                        , int('Citizens from other countries' in segment['Audience Type'])
                                        , int('Europeans' in segment['Audience Type'])
                                        , int('User with account' in segment['User Type'])
                                        , int('User without account' in segment['User Type'])
                                        , int('Unspecified' in segment['User Type'])
                                        , int('Profile data' in segment['Access Scope'])
                                        , int('Transactional data' in segment['Access Scope'])
                                        , int('User account data' in segment['Access Scope'])
                                        , int('Other data about user' in segment['Access Scope'])
                                        , int('Unspecified' in segment['Access Scope'])
                                        , int('Deactivate account' in segment['Access Type'])
                                        , int('Delete account (full)' in segment['Access Type'])
                                        , int('Delete account (partial)' in segment['Access Type'])
                                        , int('Edit information' in segment['Access Type'])
                                        , int('View' in segment['Access Type'])
                                        , int('None' in segment['Access Type'])
                                        , int('Unspecified' in segment['Access Type'])
                                        , int('Collect from user on other websites' in segment['Action First-Party'])
                                        , int('Collect in mobile app' in segment['Action First-Party'])
                                        , int('Collect on mobile website' in segment['Action First-Party'])
                                        , int('Collect on website' in segment['Action First-Party'])
                                        , int('Receive from other parts of company/affiliates' in segment['Action First-Party'])
                                        , int('Receive from other service/third-party (named)' in segment['Action First-Party'])
                                        , int('Receive from other service/third-party (unnamed)' in segment['Action First-Party'])
                                        , int('Track user on other websites' in segment['Action First-Party'])
                                        , int('Unspecified' in segment['Action First-Party'])
                                        , int('Collect on first party website/app' in segment['Action Third-Party'])
                                        , int('Receive/Shared with' in segment['Action Third-Party'])
                                        , int('See' in segment['Action Third-Party'])
                                        , int('Track on first party website/app' in segment['Action Third-Party'])
                                        , int('Unspecified' in segment['Action Third-Party'])
                                        , int('Named third party' in segment['Third Party Entity'])
                                        , int('Other part of company/affiliate' in segment['Third Party Entity'])
                                        , int('Other users' in segment['Third Party Entity'])
                                        , int('Public' in segment['Third Party Entity'])
                                        , int('Unnamed third party' in segment['Third Party Entity'])
                                        , int('Unspecified' in segment['Third Party Entity'])
                                        , int('Collection' in segment['Choice Scope'])
                                        , int('First party collection' in segment['Choice Scope'])
                                        , int('First party use' in segment['Choice Scope'])
                                        , int('Third party sharing/collection' in segment['Choice Scope'])
                                        , int('Third party use' in segment['Choice Scope'])
                                        , int('Both' in segment['Choice Scope'])
                                        , int('Use' in segment['Choice Scope'])
                                        , int('Unspecified' in segment['Choice Scope'])
                                        , int('Browser/device privacy controls' in segment['Choice Type'])
                                        , int('Dont use service/feature' in segment['Choice Type'])
                                        , int('First-party privacy controls' in segment['Choice Type'])
                                        , int('Opt-in' in segment['Choice Type'])
                                        , int('Opt-out link' in segment['Choice Type'])
                                        , int('Opt-out via contacting company' in segment['Choice Type'])
                                        , int('Third-party privacy controls' in segment['Choice Type'])
                                        , int('Unspecified' in segment['Choice Type'])
                                        , int('None' in segment['User Choice'])
                                        , int('Opt-in' in segment['User Choice'])
                                        , int('Opt-out' in segment['User Choice'])
                                        , int('User participation' in segment['User Choice'])
                                        , int('Unspecified' in segment['User Choice'])
                                        , int('In case of merger or acquisition' in segment['Change Type'])
                                        , int('Non-privacy relevant change' in segment['Change Type'])
                                        , int('Privacy relevant change' in segment['Change Type'])
                                        , int('Unspecified' in segment['Change Type'])
                                        , int('Explicit' in segment['Collection Mode'])
                                        , int('Implicit' in segment['Collection Mode'])
                                        , int('Unspecified' in segment['Collection Mode'])
                                        , int('Not metioned' in segment['Do Not Track Policy'])
                                        , int('Honored' in segment['Do Not Track Policy'])
                                        , int('Not honored' in segment['Do Not Track Policy'])
                                        , int('Mentioned, but unclear if honored' in segment['Do Not Track Policy'])
                                        , int('Other' in segment['Do Not Track Policy'])
                                    ))
                    except Exception as attr_predict_exception:
                                    self.logger.info(f'Failed to process policy ID = {self.policy_id}, segment ID {self.segment_id}', exc_info=attr_predict_exception)
                                    raise 'An exception occurred: {}'.format(attr_predict_exception)

                # Commit to save changes.
                database_connection.commit()
        
        self.logger.debug(f"Added Segment with Policy ID {self.policy_id} to the database.")
                


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
            # Vectorize segment
            segments_tensor = dp.process_policy_of_interest(self.dictionary , self.policy_text)
            # segment_tensor = dp.process_policy_of_interest(self.dictionary, [self.segment_text,])
        except BaseException as segment_tensor_exception:
            raise Exception(f"Exception while creating segment tensor. Error Message: {segment_tensor_exception}")

        self.logger.debug(f'Making Category Predictions: {str(self.policy_logger_dict)}')

        # Make predictions using the CNN model
        main_predictions = self.models['Main']['model'].predict_proba(segments_tensor)

        # Filter predictions to include labels with >50% probability
        main_predictions = main_predictions > 0.5

        result = []

        # Append result for each segment to the result list
        for result_row in range(len(self.policy_text)):

            # Extract main label predictions for current segment.
            main_predictions = main_predictions[result_row, :]

            # Initialize main label classification to empty.
            main_labels = []

            # Parse main label classifications and add to the main_labels list.
            for label in range(12):
                if main_predictions[label] == True:
                    main_labels.append(self.models['Main']['labels'][label])

            if (len(main_labels) == 0):
                continue

            segment_tensor = dp.process_policy_of_interest(self.dictionary, [self.policy_text[result_row],])
            
            # Instantiate result dictionary for current segment
            current_segment = {
                'main': main_labels,
                'Does or Does Not': [],
                'Identifiability': [],
                'Personal Information Type': [],
                'Purpose': [],
                'Retention Period': [],
                'Retention Purpose': [],
                'Notification Type': [],
                'Security Measure': [],
                'Audience Type': [],
                'User Type': [],
                'Access Scope': [],
                'Access Type': [],
                'Action First-Party': [],
                'Action Third-Party': [],
                'Third Party Entity': [],
                'Choice Scope': [],
                'Choice Type': [],
                'User Choice': [],
                'Change Type': [],
                'Collection Mode': [],
                'Do Not Track Policy': []
            }

            # Keep track of attributes as they get predicted, prevent redoing predictions
            predicted_attributes = []

            # If any attribute needs to be classified, proceed individually.
            if ('First Party Collection/Use' in main_labels):

                for attribute in ['Does or Does Not', 'Collection Mode', 'Action First-Party', 'Identifiability', 'Personal Information Type', 'Purpose', 'User Type', 'Choice Type', 'Choice Scope']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)
            
            if ('Third Party Sharing/Collection' in main_labels):

                for attribute in ['Third Party Entity', 'Does or Does Not', 'Action Third-Party', 'Identifiability', 'Personal Information Type', 'Purpose', 'User Type', 'Choice Type', 'Choice Scope']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)
            
            if ('User Access, Edit and Deletion' in main_labels):

                for attribute in ['Access Type', 'Access Scope', 'User Type']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)

            if ('Data Retention' in main_labels):

                for attribute in ['Retention Period', 'Retention Purpose', 'Personal Information Type']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)

            if ('Data Security' in main_labels):

                for attribute in ['Security Measure']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)
            
            if ('International and Specific Audiences' in main_labels):

                for attribute in ['Audience Type']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)
            
            if ('Do Not Track' in main_labels):

                for attribute in ['Do Not Track Policy']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)
            
            if ('Policy Change' in main_labels):

                for attribute in ['Change Type', 'Notification Type', 'User Choice']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)
            
            if ('User Choice/Control' in main_labels):

                for attribute in ['Choice Type', 'Choice Scope', 'Personal Information Type', 'Purpose', 'User Type']:

                    if attribute in predicted_attributes:
                        continue
                    
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

                    predicted_attributes.append(attribute)
            
            # Append the results of the current segment to the results for the policy.
            result.append(current_segment)
        


        self.logger.debug(f"Classified segment for Policy ID {self.policy_id} Adding to the database now.")
        
        # Add policy classification results to the database.
        self.add_results_to_database(result)




