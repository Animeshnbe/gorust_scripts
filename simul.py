# generate a random list of integers of length 100

import numpy as np
import random

# create a boolean array of length 10 with a total of 2 true values in random indices

predator_pos = np.random.choice(10, 5, replace=False)
trees = [False if i not in predator_pos else True for i in range(10)]
# print(trees)

gene_pos = np.random.choice(100, 50, replace=False)
bots = [1 if i not in gene_pos else 2 for i in range(100)]
# 1 = altruist, 2 = coward

generations = 100
# for gen in range(generations):
#     n = len(bots) # decided at the start of iteration
#     print("N = ",n)
#     for i in range(n):
#         tree_is_predator = trees[np.random.randint(0,9)]
#         if tree_is_predator:
#             print(i)
#             if bots[i]==1:
#                 if i<n-1: # another bot is present
#                     if bots[i+1]==1:
#                         # remove the ith element of bots
#                         del bots[i]
#                         i-=1
#                     else:
#                         del bots[i+1]
#                     n-=1
#             else:
#                 # remove the first element from bots
#                 if i<n-1:
#                     del bots[i+1]
#                     n-=1
#         elif random.randint(0,1)==0:
#             bots.append(bots[i]) # may reproduce with 50% chance
#     # count the percent of bots with value=1 and those with value=2
#     altruists = sum([1 if b==1 else 0 for b in bots])
#     cowards = sum([1 if b==2 else 0 for b in bots])
#     print(f'Generation: {gen}, Len = {len(bots)}, Altruists = {altruists/len(bots)}, Cowards = {cowards/len(bots)}')

x = [1,2,3,4,5,6,7,8,9,10]
n = len(x)
for i in range(n):
    print(i,x[i])
    if i==2:
        del x[i+1]
        n-=1
