import torch
import torch.utils.data as data
import pandas as pd
import numpy as np

class WerewolfDataset(data.Dataset):
  """Werewolf dataset."""

  def __init__(self, name_filelist):
    self.name_dataframe = pd.read_csv(name_filelist)


  def __len__(self):
    return len(self.name_dataframe)

  def __getitem__(self, idx):
    basename = self.name_dataframe.iloc[idx][0]


    x = torch.from_numpy(np.load(basename+".x.npy")).float()
    y = torch.from_numpy(np.load(basename + ".y.npy")).long()
    valid = torch.from_numpy(np.load(basename + ".valid.npy")).float()
    
    ###
    #Careful with the shape, should have shape num_steps
    #We simply create a uniform growing series from 0 to 1
    loss_scale = torch.from_numpy(np.linspace(0.0,1.0,valid.size()[0],dtype='float32'))
    # Add fake last dimension to use expand
    valid = torch.mul(valid, loss_scale).view(valid.size()[0],-1)
    #Valid is expanded, in blocks of J that hold the same value
    valid = valid.expand(-1,x.size()[0]).contiguous().view(-1)


    #Repeat targets across timesteps
    y = y.repeat(x.size()[1])
    
    ###


    return (x,y,valid)
