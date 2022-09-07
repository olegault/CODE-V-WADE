#Imports needed from pytorch
import torch
from torch.utils.data import Dataset
from collections import OrderedDict
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.optim import SGD,Adam

# SKLearn and Skorch
from skorch import NeuralNet

import utilities
from configuration import Configuration
from database import Database
from urllib.parse import unquote
import pickle
import torch
from cnn import CNN
import data_processing as dp
import privacy_policies_dataset as PPD

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
        
        # Path to the weights matrix
        self.weights_matrix_path = self.configuration["models"]["weightsMatrixPath"]
        
        with open(self.weights_matrix_path, "rb") as weights_matrix_file:
            self.weights_matrix = pickle.load(weights_matrix_file)
    
    def collate_data(self, batch):

        def stack_segments(segments, clearance = 2):

            import numpy as np

            segments_len = map(len, segments)
            max_len = max(segments_len)

            segments_list = []

            output_len = max_len + clearance * 2

            for i, segment in enumerate(segments):

                segment_array = np.array(segment)

                zeros_to_prepend = int((output_len - len(segment_array))/2)

                zeros_to_append = output_len - len(segment_array) - zeros_to_prepend

                resized_array = np.append(np.zeros(zeros_to_prepend), segment_array)

                resized_array = np.append(resized_array, np.zeros(zeros_to_append))

                segments_list.append(torch.tensor(resized_array, dtype = torch.int64, device=torch.device("cuda")))

                segments_tensor = torch.stack(segments_list).unsqueeze(1)

            return segments_tensor                         

        segments = [item[0] for item in batch]

        labels = [item[1] for item in batch]

        segments_tensor = stack_segments(segments)

        labels_tensor = torch.stack(labels)

        return [segments_tensor, labels_tensor]
    
    def load_model(self, current_attribute, current_num_levels):
        # Load Trained Model
        net = NeuralNet(
            CNN,
            module__embeddings = self.weights_matrix,
            module__vocab_size = self.weights_matrix.shape[0],
            module__emb_dim = self.weights_matrix.shape[1],
            module__Co = 200,
            module__Hu = [100],
            module__C = current_num_levels,
            module__Ks = [3],
            module__name = f'{current_attribute}_zeros_60-20-(no-val)_polisis',
            module__dropout = 0.5,
            max_epochs = 300,
            lr = 0.01,
            optimizer = SGD,
            optimizer__weight_decay = 0,
            optimizer__momentum=0.9,
            criterion = nn.BCELoss(),
            batch_size=40,
            # Turn the validation split off once we have the metadata values set
            train_split = None,
            # Shuffle training data on each epoch
            iterator_train__shuffle=True,
            iterator_train__collate_fn=self.collate_data,
            iterator_valid__collate_fn=self.collate_data,
            # Turn off verbose
            verbose = 0,
            device='cuda',
        ).initialize()
        net.load_params(f_params=f'{self.model_path}/{current_attribute}/model.pkl',f_optimizer=f'{self.model_path}/{current_attribute}/optimizer.pkl', f_history=f'{self.model_path}/{current_attribute}/history.json')
        return net
    
    def get_all_models(self):
        models = {}

        # Main Model
        main_model = self.load_model('Majority', 12)
        main_labels = list(dp.attr_value_labels('Majority'))
        models['Main'] = {
            'model': main_model,
            'labels': main_labels
        }

        self.logger.info("Fetched Main Model")
        
        # Does or Does Not
        does_not_model = self.load_model('Does or Does Not', 2)
        does_not_labels = list(dp.attr_value_labels('Does or Does Not'))
        models['Does or Does Not'] = {
            'model': does_not_model,
            'labels': does_not_labels
        }

        # Identifiability
        identifiability_model = self.load_model('Identifiability', 3)
        identifiability_labels = list(dp.attr_value_labels('Identifiability'))
        models['Identifiability'] = {
            'model': identifiability_model,
            'labels': identifiability_labels
        }

        # Personal Information Type
        personal_information_type_model = self.load_model('Personal Information Type', 15)
        personal_information_type_labels = list(dp.attr_value_labels('Personal Information Type'))
        models['Personal Information Type'] = {
            'model': personal_information_type_model,
            'labels': personal_information_type_labels
        }

        # Purpose
        purpose_model = self.load_model('Purpose', 10)
        purpose_labels = list(dp.attr_value_labels('Purpose'))
        models['Purpose'] = {
            'model': purpose_model,
            'labels': purpose_labels
        }

        self.logger.info("Fetched Attribute Models")

        return models
    
    def get_additional_models(self):
        models = {}
        
        # Retention Period
        retention_period_model = self.load_model('Retention Period', 4)
        retention_period_labels = list(dp.attr_value_labels('Retention Period'))
        models['Retention Period'] = {
            'model': retention_period_model,
            'labels': retention_period_labels
        }
        
        # Retention Purpose
        retention_purpose_model = self.load_model('Retention Purpose', 7)
        retention_purpose_labels = list(dp.attr_value_labels('Retention Purpose'))
        models['Retention Purpose'] = {
            'model': retention_purpose_model,
            'labels': retention_purpose_labels
        }
        
        # Notification Type
        notification_type_model = self.load_model('Notification Type', 5)
        notification_type_labels = list(dp.attr_value_labels('Notification Type'))
        models['Notification Type'] = {
            'model': notification_type_model,
            'labels': notification_type_labels
        }
        
        # Security Measure
        security_measure_model = self.load_model('Security Measure', 9)
        security_measure_labels = list(dp.attr_value_labels('Security Measure'))
        models['Security Measure'] = {
            'model': security_measure_model,
            'labels': security_measure_labels
        }
        
        # Audience Type
        audience_type_model = self.load_model('Audience Type', 4)
        audience_type_labels = list(dp.attr_value_labels('Audience Type'))
        models['Audience Type'] = {
            'model': audience_type_model,
            'labels': audience_type_labels
        }
        
        # User Type
        user_type_model = self.load_model('User Type', 4)
        user_type_labels = list(dp.attr_value_labels('User Type'))
        models['User Type'] = {
            'model': user_type_model,
            'labels': user_type_labels
        }
        
        # Access Scope
        access_scope_model = self.load_model('Access Scope', 5)
        access_scope_labels = list(dp.attr_value_labels('Access Scope'))
        models['Access Scope'] = {
            'model': access_scope_model,
            'labels': access_scope_labels
        }
        
        # Access Type
        access_type_model = self.load_model('Access Type', 7)
        access_type_labels = list(dp.attr_value_labels('Access Type'))
        models['Access Type'] = {
            'model': access_type_model,
            'labels': access_type_labels
        }
        
        # Action First-Party
        action_first_party_model = self.load_model('Action First-Party', 9)
        action_first_party_labels = list(dp.attr_value_labels('Action First-Party'))
        models['Action First-Party'] = {
            'model': action_first_party_model,
            'labels': action_first_party_labels
        }
        
        # Action Third-Party
        action_third_party_model = self.load_model('Action Third-Party', 5)
        action_third_party_labels = list(dp.attr_value_labels('Action Third-Party'))
        models['Action Third-Party'] = {
            'model': action_third_party_model,
            'labels': action_third_party_labels
        }
        
        # Third Party Entity
        third_party_entity_model = self.load_model('Third Party Entity', 6)
        third_party_entity_labels = list(dp.attr_value_labels('Third Party Entity'))
        models['Third Party Entity'] = {
            'model': third_party_entity_model,
            'labels': third_party_entity_labels
        }
        
        # Choice Scope
        choice_scope_entity_model = self.load_model('Choice Scope', 8)
        choice_scope_labels = list(dp.attr_value_labels('Choice Scope'))
        models['Choice Scope'] = {
            'model': choice_scope_model,
            'labels': choice_scope_labels
        }
        
        # Choice Type
        choice_type_entity_model = self.load_model('Choice Type', 8)
        choice_type_labels = list(dp.attr_value_labels('Choice Type'))
        models['Choice Type'] = {
            'model': choice_type_model,
            'labels': choice_type_labels
        }
        
        # User Choice
        user_choice_model = self.load_model('User Choice', 5)
        user_choice_labels = list(dp.attr_value_labels('User Choice'))
        models['User Choice'] = {
            'model': user_choice_model,
            'labels': user_choice_labels
        }
        
        # Change Type
        change_type_model = self.load_model('Change Type', 4)
        change_type_labels = list(dp.attr_value_labels('Change Type'))
        models['Change Type'] = {
            'model': change_type_model,
            'labels': change_type_labels
        }
        
        # Collection Mode
        collection_mode_model = self.load_model('Collection Mode', 3)
        collection_mode_labels = list(dp.attr_value_labels('Collection Mode'))
        models['Collection Mode'] = {
            'model': collection_mode_model,
            'labels': collection_mode_labels
        }
    
    def get_dictionary(self):
        with open(self.dictionary_path, "rb") as dictionary_file:
            dictionary = pickle.load(dictionary_file)
        self.logger.info("Extracted word2idx Dictionary")
        return dictionary