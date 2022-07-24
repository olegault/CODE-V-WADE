import utilities
from configuration import Configuration
from database import Database
from urllib.parse import unquote
import pickle
import torch
from cnn import CNN
import data_processing as dp

class Model:
    """Class used to obtain trained models from a file path."""

    def __init__(self, logger):
        """Method to initialize the model list class."""

        # Setup the logger
        self.logger = logger

        # Get the configuration from teh configuration file
        self.configuration = Configuration().get_configuration()

        # Path to the folder with saved pretrained models
        self.model_path = self.configuration["models"]["path"]

        # Path to the word2idx dictionary
        self.dictionary_path = self.configuration["models"]["dictionaryPath"]

    def get_main_model(self):
        params_main_model_file = open(f'{self.model_path}/cnn_300_200_[100]_12_[3]_zeros_60-20-20_polisis_params.pkl', 'rb')
        params_main_model = pickle.load(params_main_model_file)
        main_model = CNN(**params_main_model)
        main_model.load_state_dict(torch.load(f'{self.model_path}/cnn_300_200_[100]_12_[3]_zeros_60-20-20_polisis_state.pt'))
        main_model.eval()
        return main_model
    
    def load_model(self, attribute, num_levels, train_percent=60, val_percent=20, test_percent=20):
        params_attribute_model_file = open(f'{self.model_path}/cnn_300_200_[100]_{num_levels}_[3]_{attribute}_zeros_{train_percent}-{val_percent}-{test_percent}_polisis_params.pkl', 'rb')
        params_attribute_model = pickle.load(params_attribute_model_file)
        attribute_model = CNN(**params_attribute_model)
        attribute_model.load_state_dict(torch.load(f'{self.model_path}/cnn_300_200_[100]_{num_levels}_[3]_{attribute}_zeros_{train_percent}-{val_percent}-{test_percent}_polisis_state.pt'))
        attribute_model.eval()
        return attribute_model
    
    def get_all_models(self):
        models = {}

        # Main Model
        main_model = self.get_main_model()
        main_labels = dp.attr_value_labels('Majority')
        models['Main'] = {
            'model': main_model,
            'labels': main_labels
        }

        self.logger.info("Fetched Main Model")

        # Retention Period
        retention_period_model = self.load_model('Retention Period', 4)
        retention_period_labels = dp.attr_value_labels('Retention Period')
        models['Retention Period'] = {
            'model': retention_period_model,
            'labels': retention_period_labels
        }

        # Retention Purpose
        retention_purpose_model = self.load_model('Retention Purpose', 7)
        retention_purpose_labels = dp.attr_value_labels('Retention Purpose')
        models['Retention Purpose'] = {
            'model': retention_purpose_model,
            'labels': retention_purpose_labels
        }

        # Notification Type
        notification_type_model = self.load_model('Notification Type', 5)
        notification_type_labels = dp.attr_value_labels('Notification Type')
        models['Notification Type'] = {
            'model': notification_type_model,
            'labels': notification_type_labels
        }

        # Security Measure
        security_measure_model = self.load_model('Security Measure', 9)
        security_measure_labels = dp.attr_value_labels('Security Measure')
        models['Security Measure'] = {
            'model': security_measure_model,
            'labels': security_measure_labels
        }

        # Audience Type
        audience_type_model = self.load_model('Audience Type', 4)
        audience_type_labels = dp.attr_value_labels('Audience Type')
        models['Audience Type'] = {
            'model': audience_type_model,
            'labels': audience_type_labels
        }

        # User Type
        user_type_model = self.load_model('User Type', 3)
        user_type_labels = dp.attr_value_labels('User Type')
        models['User Type'] = {
            'model': user_type_model,
            'labels': user_type_labels
        }

        # Access Scope
        access_scope_model = self.load_model('Access Scope', 5)
        access_scope_labels = dp.attr_value_labels('Access Scope')
        models['Access Scope'] = {
            'model': access_scope_model,
            'labels': access_scope_labels
        }

        # Does or Does Not
        does_or_does_not_model = self.load_model('Does or Does Not', 2)
        does_or_does_not_labels = dp.attr_value_labels('Does or Does Not')
        models['Does or Does Not'] = {
            'model': does_or_does_not_model,
            'labels': does_or_does_not_labels
        }

        # Access Type
        access_type_model = self.load_model('Access Type', 7)
        access_type_labels = dp.attr_value_labels('Access Type')
        models['Access Type'] = {
            'model': access_type_model,
            'labels': access_type_labels
        }

        # Action First-Party
        action_first_party_model = self.load_model('Action First-Party', 9)
        action_first_party_labels = dp.attr_value_labels('Action First-Party')
        models['Action First-Party'] = {
            'model': action_first_party_model,
            'labels': action_first_party_labels
        }

        # Action Third-Party
        action_third_party_model = self.load_model('Action Third-Party', 5)
        action_third_party_labels = dp.attr_value_labels('Action Third-Party')
        models['Action Third-Party'] = {
            'model': action_third_party_model,
            'labels': action_third_party_labels
        }

        # Third Party Entity
        third_party_entity_model = self.load_model('Third Party Entity', 6)
        third_party_entity_labels = dp.attr_value_labels('Third Party Entity')
        models['Third Party Entity'] = {
            'model': third_party_entity_model,
            'labels': third_party_entity_labels
        }

        # Choice Scope
        choice_scope_model = self.load_model('Choice Scope', 8)
        choice_scope_labels = dp.attr_value_labels('Choice Scope')
        models['Choice Scope'] = {
            'model': choice_scope_model,
            'labels': choice_scope_labels
        }

        # Choice Type
        choice_type_model = self.load_model('Choice Type', 8)
        choice_type_labels = dp.attr_value_labels('Choice Type')
        models['Choice Type'] = {
            'model': choice_type_model,
            'labels': choice_type_labels
        }

        # User Choice
        user_choice_model = self.load_model('User Choice', 5)
        user_choice_labels = dp.attr_value_labels('User Choice')
        models['User Choice'] = {
            'model': user_choice_model,
            'labels': user_choice_labels
        }

        # Change Type
        change_type_model = self.load_model('Change Type', 4)
        change_type_labels = dp.attr_value_labels('Change Type')
        models['Change Type'] = {
            'model': change_type_model,
            'labels': change_type_labels
        }

        # Collection Mode
        collection_mode_model = self.load_model('Collection Mode', 3)
        collection_mode_labels = dp.attr_value_labels('Collection Mode')
        models['Collection Mode'] = {
            'model': collection_mode_model,
            'labels': collection_mode_labels
        }

        # Identifiability
        identifiability_model = self.load_model('Identifiability', 3)
        identifiability_labels = dp.attr_value_labels('Identifiability')
        models['Identifiability'] = {
            'model': identifiability_model,
            'labels': identifiability_labels
        }

        # Personal Information Type
        # personal_information_type_model = self.load_model('Personal Information Type', num_levels=15, train_percent=80, val_percent=10, test_percent=10)
        params_personal_information_type_file = open(f'{self.model_path}/cnn_300_200_[100]_15_[3]_Personal Information Type_zeros_80-10-10_polisis_SGD_params.pkl', 'rb')
        params_personal_information_type_model = pickle.load(params_personal_information_type_file)
        personal_information_type_model = CNN(**params_personal_information_type_model)
        personal_information_type_model.load_state_dict(torch.load(f'{self.model_path}/cnn_300_200_[100]_15_[3]_Personal Information Type_zeros_80-10-10_polisis_SGD_state.pt'))
        personal_information_type_model.eval()
        
        personal_information_type_labels = dp.attr_value_labels('Personal Information Type')
        models['Personal Information Type'] = {
            'model': personal_information_type_model,
            'labels': personal_information_type_labels
        }

        # Purpose
        purpose_model = self.load_model('Purpose', 10)
        purpose_labels = dp.attr_value_labels('Purpose')
        models['Purpose'] = {
            'model': purpose_model,
            'labels': purpose_labels
        }

        # Do Not Track Policy
        do_not_track_policy_model = self.load_model('Do Not Track Policy', 5)
        do_not_track_policy_labels = dp.attr_value_labels('Do Not Track Policy')
        models['Do Not Track Policy'] = {
            'model': do_not_track_policy_model,
            'labels': do_not_track_policy_labels
        }

        self.logger.info("Fetched Attribute Models")

        return models
    
    def get_dictionary(self):
        with open(self.dictionary_path, "rb") as dictionary_file:
            dictionary = pickle.load(dictionary_file)
        self.logger.info("Extracted word2idx Dictionary")
        return dictionary