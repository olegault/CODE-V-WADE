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

        # Instantiate the app table ID.
        self.app_id = app_id

        # Instantiate the policy URL.
        self.policy_url = policy_url

        # Instantiate the policy plain text.
        self.policy_text = policy_text

        # Instantiate the policy's simple HTML version.
        self.policy_html = policy_html

        # Load existing dictionary
        self.dictionary = dictionary
        
        # Policy Dict for Logger
        self.policy_logger_dict = {
            'id': self.policy_id,
            'app_id': self.app_id,
            'policy_url': self.policy_url
        }

    def classify_attribute(self, segment_text, attribute_model, attribute_labels, threshold = 0.95):

        # Ordered Dict to List 
        attribute_labels = list(attribute_labels)
        
        # Vectorize policy segments
        segments_tensor = dp.process_policy_of_interest(self.dictionary , [segment_text])

        # Make predictions using the CNN model
        predictions = attribute_model(segments_tensor)
        
        # Filter predictions to include labels with >95% probability
        y_pred = predictions > threshold
        
#         print("YPred:")
#         print(y_pred)
        
        # Extract just the prediction row as a list.
        predicted_values = y_pred[0, :]
        
#         print("Predicted_Values:")
#         print(predicted_values)
        
        # Instantiate a result list.
        result_labels = []
        
        try: 
            # Parse each label and record True labels.
            for label in range(len(attribute_labels)):
                if predicted_values[label] == True:
                        result_labels.append(attribute_labels[label])
        except Exception as attr_predict_exception:
            self.logger.info(f'Failed to process policy ID = {self.policy_id},\n y_pred = {y_pred}.\n predicted_values = {predicted_values}.\n attr_labels = {attribute_labels}', exc_info=attr_predict_exception)
            raise 'An exception occurred: {}'.format(attr_predict_exception)
            

        # Return a list of labels that were identified for the attribute in the current segments.
        return result_labels

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
                    
                    segment_text = segment['segment_text']
                    main_labels = segment['main_labels']
                    
                    # Insert a row in the segment table.
                    cursor.execute(sql_statements.segment_insert,
                                (self.app_id, self.policy_id, segment_text))

                    # Use the segment row id as the foreign key to the classified labels.
                    segment_id = cursor.lastrowid

                    # Add each category label to the database.
                    for label in main_labels:
                        cursor.execute(sql_statements.catetgory_labels_insert, (segment_id, label))
                    
                    # If any attribute labels were classified for the segment.
                    if ('attribute_labels' in segment):

                        # Initialize the list of attribute labels
                        attribute_labels = segment['attribute_labels']

                        # Parse each label.
                        for attribute in attribute_labels:

                            # Add each attribute label to the attribute label table of the database.
                            cursor.execute(sql_statements.attribute_labels_insert, (segment_id, attribute))
                            
                            try:
                                # Attribute table Name to insert into the right db table
                                attribute_table_name = utilities.label_to_variable(attribute)
                            except Exception as attr_predict_exception:
                                self.logger.info(f'Failed to process policy ID = {self.policy_id},\n attribute_table_name = {attribute_table_name}.\n attribute = {attribute}.\n attr_labels = {attribute_labels}', exc_info=attr_predict_exception)
                                raise 'An exception occurred: {}'.format(attr_predict_exception)

                            # SQL statement to inser value into the attribute table
                            sql_statement = sql_statements.attribute_variable_table_insert.format(table_name=f"{attribute_table_name}_label")

                            # Fetch all classifications for the current attribute label.
                            attribute_results = segment[attribute]

                            # Parse through each result for the given attribute.
                            for label in attribute_results:
                                
                                try:
                                    # Add each label to the corresponding table
                                    cursor.execute(sql_statement, (segment_id, label))
                                except Exception as attr_predict_exception:
                                    self.logger.info(f'Failed to process policy ID = {self.policy_id},\n attribute_table_name = {attribute_table_name}.\n attribute = {attribute}.\n attr_labels = {attribute_labels}', exc_info=attr_predict_exception)
                                    raise 'An exception occurred: {}'.format(attr_predict_exception)


                # Commit to save changes.
                database_connection.commit()
        
        self.logger.debug(f"Added Policy with Policy ID {self.policy_id} to the database.")
                


    def process_policy(self):
        
        primary_labels = ('First Party Collection/Use', 'Third Party Sharing/Collection', 'User Access, Edit and Deletion', 'Data Retention',
          'Data Security', 'International and Specific Audiences', 'Do Not Track', 'Policy Change', 'User Choice/Control',
          'Introductory/Generic', 'Practice not covered', 'Privacy contact information') 
        
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
                    main_labels.append(primary_labels[label])

            # Proceed if current segment includes any main labels.
            if(len(main_labels) > 0):

                # Instantiate result dictionary for current segment
                current_segment = {
                    'segment_text': segment_text,
                    'main_labels': main_labels
                }

                # Extract corresponding attributes to be extracted for each main label.
                for label in main_labels:
                    attribute_labels.extend(utilities.main_label_to_attribute(label))
                
                # Remove duplicate attributes.
                attribute_labels = set(attribute_labels)

                # If any attribute needs to be classified, proceed individually.
                if (len(attribute_labels) > 0):

                    # Add attribute labels to the current segment result dict.
                    current_segment['attribute_labels'] = attribute_labels

                    for attribute in attribute_labels:
                        
                        self.logger.debug(f'Making Attribute {attribute} Predictions: {str(self.policy_logger_dict)}')

                        # Instantiate attribute model.
                        attribute_model = self.models[attribute]['model']

                        # Instantiate attribute labels dict as a list.
                        attribute_labels_dict = self.models[attribute]['labels']

                        # Call classification function and extract predicted labels as a list.
                        predicted_labels = self.classify_attribute(segment_text, attribute_model, attribute_labels_dict, threshold = 0.95)
                        
                        # If any labels have been classified, add them to the dict.
                        current_segment[attribute]= predicted_labels
                    
                # Append the results of the current segment to the results for the policy.
                result.append(current_segment)
        
        self.logger.debug(f"Classified policy with Policy ID {self.policy_id}. Adding to the database now.")
        
        # Add policy classification results to the database.
        self.add_results_to_database(result)


    

