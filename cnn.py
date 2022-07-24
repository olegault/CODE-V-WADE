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
    