
import torch.nn.functional as Fun

import os
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms


device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

# class Network(nn.Module):
#     def __init__(self):
#         super(Network, self).__init__()
#         self.conv = nn.Conv2d(2, 4, 4)
#         self.conv = nn.Conv2d(4, 12, 3)
#         self.fu1 = nn.Linear(10 * 4 * 3, 90) # 5*5 from image dimension
#         self.fu2 = nn.Linear(90, 70)
#         self.fu3 = nn.Linear(60, 12)
    
#     def next(self, A):
#         A = Fun.max_pool2d(Fun.relu(self.conv(A)), (3, 3))
#         A = Fun.max_pool2d(Fun.relu(self.conv2d(A)), 3)
#         A = torch.flatten(A, 2) # flatten all dimensions except the batch dimension
#         A = Fun.relu(self.fu1(A))
#         A = Fun.relu(self.fu2(A))
#         A = self.fu3(A)
#         return A

# net_value = Network()
# print(net_value)