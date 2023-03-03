#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Imports needed from pytorch
import torch
from torch.utils.data import Dataset
from collections import OrderedDict
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.optim import SGD,Adam

# SKLearn and Skorch
from sklearn.datasets import make_classification
from skorch import NeuralNet, NeuralNetClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score, make_scorer


#Some built-in imports
import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
import time
from os.path import join, isfile
from os import listdir
from math import ceil

#Imports from the repository
from data_processing import get_weight_matrix, get_tokens
import data_processing as dp
from privacy_policies_dataset import PrivacyPoliciesDataset as PPD

import nltk
nltk.download('punkt')


# # Define the CNN

# In[3]:


class CNN(nn.Module):


    """
    
    Convolutional Neural Model used for training the models. The total number of kernels that will be used in this
    CNN is Co * len(Ks). 
    
    Args:
        weights_matrix: numpy.ndarray, the shape of this n-dimensional array must be (words, dims) were words is
        the number of words in the vocabulary and dims is the dimensionality of the word embeddings.
        Co (number of filters): integer, stands for channels out and it is the number of kernels of the same size that will be used.
        Hu: integer, stands for number of hidden units in the hidden layer.
        C: integer, number of units in the last layer (number of classes)
        Ks: list, list of integers specifying the size of the kernels to be used. 
     
    """
    
    def __init__(self, embeddings, vocab_size, emb_dim, Co, Hu, C, Ks, dropout, name = 'generic'):
        
        super(CNN, self).__init__()
              
        self.num_embeddings = vocab_size
        
        self.embeddings_dim = emb_dim

        self.padding_index = 0
        
        self.cnn_name = 'cnn_' + str(emb_dim) + '_' + str(Co) + '_' + str(Hu) + '_' + str(C) + '_' + str(Ks) + '_' + name

        self.Co = Co
        
        self.Hu = Hu
        
        self.C = C
        
        self.Ks = Ks
        
        self.embedding = nn.Embedding(self.num_embeddings, self.embeddings_dim, self.padding_index)
        self.embedding = self.embedding.from_pretrained(torch.tensor(embeddings).float(), freeze=True)

        self.convolutions = nn.ModuleList([nn.Conv2d(1,self.Co,(k, self.embeddings_dim)) for k in self.Ks])
        
        # activation function for hidden layers =  Rectified Linear Unit
        self.relu = nn.ReLU()
        
        self.drop_out = nn.Dropout(p=dropout)
        
        self.linear1 = nn.Linear(self.Co * len(self.Ks), self.Hu[0])
        
        self.linear2 = nn.Linear(self.Hu[-1], self.C)
        
        # activation function of output layer
        self.sigmoid = nn.Sigmoid()
        
        self.double()
    
    def forward(self,x):
        
        #size(N,1,length) to size(N,1,length,dims)
        
        x = self.embedding(x)
        
        #size(N,1,length,dims) to size(N,1,length)
        
        x = [self.relu(conv(x)).squeeze(3) for conv in self.convolutions]
        
        #size(N,1,length) to (N, Co * len(Ks))
        
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]
        
        x = torch.cat(x,1)
        
        x = self.linear1(x)
        
        x = self.relu(x)
        
        x = self.linear2(x)

        x = self.sigmoid(x)
        
        return x
    


# In[4]:


def collate_data(batch):

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


# # Prepare the Dataset

# In[5]:


current_attribute = 'Personal Information Type'
current_num_levels = 15


# In[6]:


dictionary_path = "/data/word2idx_fast_text_300.pkl"
def get_dictionary():
        with open(dictionary_path, "rb") as dictionary_file:
            dictionary = pickle.load(dictionary_file)
        return dictionary
dictionary = get_dictionary()

word2vector_fast_text_path = "/data/word2vector_fast_text_300.pkl"
def get_word2vector_fast_text():
        with open(word2vector_fast_text_path, "rb") as dictionary_file:
            dictionary = pickle.load(dictionary_file)
        return dictionary
word2vector_fast_text = get_word2vector_fast_text()

weights_matrix_path = "/data/weights_matrix_300.pkl"
def get_weights_matrix():
        with open(weights_matrix_path, "rb") as dictionary_file:
            dictionary = pickle.load(dictionary_file)
        return dictionary
weights_matrix = get_weights_matrix()


# In[7]:


labels_file = open(f"labels_{current_attribute}.pkl","rb")

labels = pickle.load(labels_file)

labels_file.close()

target_names = []
label_indices = []

for label, index in labels.items():
    target_names.append(label)
    label_indices.append(index)
    print(str(index) + '. ' + label)


# In[8]:


dp.aggregate_data_attribute_level(current_attribute, current_num_levels, read = False)
sentence_matrices_all, labels_matrices_all = dp.process_dataset_attribute_level(labels, dictionary, current_attribute, read = False)
dataset = PPD(sentence_matrices_all, labels_matrices_all, labels)
test_dataset, train_dataset = dataset.split_dataset_randomly(0.2)


# In[9]:


train_dataset.labels_stats()
print("-" * 35 * 3)
test_dataset.labels_stats()
print("-" * 35 * 3)


# In[18]:


def my_custom_f1(y_true, y_pred):
    y_pred = y_pred > 0.5
    return f1_score(y_true, y_pred, average='macro', zero_division='warn')

score = make_scorer(my_custom_f1, needs_proba=True)


# In[16]:

net = NeuralNet(
    CNN,
    module__embeddings = weights_matrix,
    module__vocab_size = weights_matrix.shape[0],
    module__emb_dim = weights_matrix.shape[1],
    module__Co = 200,
    module__Hu = [100],
    module__C = current_num_levels,
    module__Ks = [3],
    module__name = f'{current_attribute}_zeros_60-20-20_polisis',
    module__dropout = 0.5,
    max_epochs = 50,
    lr = 0.01,
    optimizer = SGD,
    optimizer__weight_decay = 0,
    optimizer__momentum=0.9,
    criterion = nn.BCELoss(),
    batch_size=40,
    # Shuffle training data on each epoch
    iterator_train__shuffle=True,
    iterator_train__collate_fn=collate_data,
    iterator_valid__collate_fn=collate_data,
    device='cuda',
    verbose=0
)



params = {
    'lr': [0.0001],
    'max_epochs': [10000],
}

gs = GridSearchCV(net, params, refit=True, scoring=score, verbose=3)


gs.fit(train_dataset.segments_array, train_dataset.labels_tensor)
print(gs.best_score_, gs.best_params_)
