#!/usr/bin/env python
# coding: utf-8

# # Attribute Classifiers

# In[4]:


#Imports needed from pytorch
import torch
from torch.utils.data import Dataset
from collections import OrderedDict
from torch import nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.optim import SGD,Adam

#Some built-in imports
import matplotlib.pyplot as plt
import numpy as np
import pickle
from os.path import join, isfile
from os import listdir


# SKLearn and Skorch
from sklearn.datasets import make_classification
from skorch import NeuralNet, NeuralNetClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import f1_score, make_scorer
from sklearn.metrics import classification_report
from skorch.callbacks import EarlyStopping

#Imports from the repository
from data_processing import get_weights_matrix, get_tokens
import data_processing as dp
from privacy_policies_dataset import PrivacyPoliciesDataset as PPD

import nltk
nltk.download('punkt')


# # 1. Declare Attribute to Train

# In[5]:


current_attribute = 'Does or Does Not'
current_num_levels = 2


# # 2. Pretrained Embeddings

# In[6]:


def get_dicts(input_path, output_path, dims = 300, read = False):
    """
    
    This functions returns two dictionaries that process the fasttext folder and gets the pretrained 
    embedding vectors.
    
    Args:
        input_path: string, path to the pretrained embeddings
        output_path: string, path to save dictionaries extracted from the pretrained embeddings
        dims: integer, embeddings dimensionality to use. (Default = 300)
        read: boolean, variable that allows us to decide wether to read from pre-processed files or not.
    Returns:
        word2vector: dictionary, the keys are the words and the values are the embeddings associated with that word.
        word2idx: dictionary, the keys are the words and the values are the indexes associated with that word.
    
    """
    
    def append_from_file(words, word2idx, vectors, idx, input_path):
        
        with open(input_path, encoding="utf8") as fast_text_file:

            for line in fast_text_file:

                split_line = line.split()

                word = split_line[0]

                words.append(word)

                word2idx[word] = idx

                vector = np.array(split_line[1:]).astype(float)

                vectors.append(vector)
                
                idx += 1
                
        return words, word2idx, vectors, idx
    

    word2vector_path = "word2vector_" + str(dims) + ".pkl"

    word2vector_path = join(output_path, word2vector_path)

    word2idx_path = "word2idx_" + str(dims) + ".pkl"

    word2idx_path = join(output_path, word2idx_path)
    
    if isfile(word2vector_path) and isfile(word2idx_path) and read:
        
        print("Loading from file {}".format(word2vector_path))

        with open(word2vector_path,"rb") as word2vector_file:
        
            word2vector = pickle.load(word2vector_file)
            
        print("Loading from file {}".format(word2idx_path))

        with open(word2idx_path,"rb") as word2idx_file:
        
            word2idx = pickle.load(word2idx_file)
            
    else:
        
        print("Processing dataset ...")

        words = [None]

        word2idx = {None: 0}

        idx = 1

        vectors = [np.zeros(dims)]
        
        words, word2idx, vectors, idx = append_from_file(words, word2idx, vectors, idx, input_path)     
                           
        word2vector = {w: vectors[word2idx[w]] for w in words}
        
        with open(word2vector_path,"wb") as word2vector_file:
        
            pickle.dump(word2vector, word2vector_file)
        
        with open(word2idx_path,"wb") as word2idx_file:
        
            pickle.dump(word2idx, word2idx_file)

    return word2vector, word2idx


# In[7]:


pretrained_embeddings = './embeddings/pretrained_embeddings_300.vec'
word2vector, word2idx = get_dicts(pretrained_embeddings, f"./embeddings/", 300, read = True)
weights_matrix = get_weights_matrix(300, f"./embeddings/", oov_random = False, dictionary = word2idx, word2vector = word2vector, read = True)


# # Train and Test Datasets

# In[10]:


labels_file = open(f"labels/labels_{current_attribute}.pkl","rb")

labels = pickle.load(labels_file)

labels_file.close()

target_names = []
label_indices = []

for label, index in labels.items():
    target_names.append(label)
    label_indices.append(index)
    print(str(index) + '. ' + label)


# In[12]:


dp.aggregate_data_attribute_level(current_attribute, current_num_levels, read = True)


# In[14]:


sentence_matrices_all, labels_matrices_all = dp.process_dataset_attribute_level(labels, word2idx, current_attribute, read = True)


# We now create an PPD which stands for PrivacyPoliciesDataset containing the training and testing dataset. We will need to split the data in two to get the test training data and the data that will be used for training and validation. The function split_dataset_randomly is spliting the dataset 90/10 by default. It uses a consistent random seed as 10.

# In[15]:


dataset = PPD(sentence_matrices_all, labels_matrices_all, labels)

test_dataset, train_dataset = dataset.split_dataset_randomly(ratio = 0.2)

test_dataset.pickle_dataset(f"datasets/test_dataset_{current_attribute}.pkl")

train_dataset.pickle_dataset(f"datasets/train_dataset_{current_attribute}.pkl")


# In[16]:


train_dataset.labels_stats()
print("-" * 35 * 3)
test_dataset.labels_stats()
print("-" * 35 * 3)


# # CNN

# In[17]:


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
    


# In[18]:


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


# In[21]:

def my_custom_f1_presence(y_true, y_pred):
    y_pred = y_pred > 0.5
    return f1_score(y_true, y_pred, average='macro', zero_division='warn')

def my_custom_f1_absence(y_true, y_pred):
    y_pred = y_pred <= 0.5
    return f1_score(y_true < 1, y_pred, average='macro', zero_division='warn')


score_presence = make_scorer(my_custom_f1_presence, needs_proba=True)
score_absence = make_scorer(my_custom_f1_absence, needs_proba=True)


# In[22]:


net = NeuralNet(
    CNN,
    module__embeddings = weights_matrix,
    module__vocab_size = weights_matrix.shape[0],
    module__emb_dim = weights_matrix.shape[1],
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
    iterator_train__collate_fn=collate_data,
    iterator_valid__collate_fn=collate_data,
    # Turn off verbose
    verbose = 0,
    device='cuda',
)


# In[23]:


params = {
    'lr': [0.001],
    'max_epochs': [100]
}

gs = RandomizedSearchCV(net, params, refit='presence', scoring=score_presence)
gs.fit(train_dataset.segments_array, train_dataset.labels_tensor)
print(gs.best_score_, gs.best_params_)


# In[ ]:


gs.best_estimator_.save_params(f_params=f'trained_models/{current_attribute}/model.pkl',f_optimizer=f'trained_models/{current_attribute}/optimizer.pkl', f_history=f'trained_models/{current_attribute}/history.json')


# In[15]:


# net.save_params(f_params=f'trained_models/{current_attribute}/model.pkl',f_optimizer=f'trained_models/{current_attribute}/optimizer.pkl', f_history=f'trained_models/{current_attribute}/history.json')


# # Evaluate Trained Model

# In[12]:


# Load Trained Model
net = NeuralNet(
    CNN,
    module__embeddings = weights_matrix,
    module__vocab_size = weights_matrix.shape[0],
    module__emb_dim = weights_matrix.shape[1],
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
    iterator_train__collate_fn=collate_data,
    iterator_valid__collate_fn=collate_data,
    # Turn off verbose
    verbose = 0,
    device='cuda',
).initialize()
net.load_params(f_params=f'trained_models/{current_attribute}/model.pkl',f_optimizer=f'trained_models/{current_attribute}/optimizer.pkl', f_history=f'trained_models/{current_attribute}/history.json')


# In[13]:


y_proba = net.predict_proba(test_dataset)


# In[14]:


# Presence
print(classification_report(test_dataset.labels_tensor > 0, y_proba > 0.5, labels=label_indices, target_names=target_names, zero_division='warn'))


# In[15]:


# Absence
print(classification_report(test_dataset.labels_tensor < 1, y_proba <= 0.5, labels=label_indices, target_names=target_names, zero_division='warn'))

