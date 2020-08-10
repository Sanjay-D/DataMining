#!/usr/bin/env python
# coding: utf-8

# In[311]:


import pandas as pd
import numpy as np
import math
import scipy 
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage


# In[320]:


simMatrix = np.genfromtxt('matrix_np1.csv',delimiter = ',')
simMatrix = np.delete(simMatrix,120,0)
simMatrix = np.delete(simMatrix,120,1)
Lmatrix = np.zeros([simMatrix.shape[0],5])
simMatrix[simMatrix == 0] = math.inf
Lmatrix[Lmatrix == 0] = math.inf


# In[321]:


def get_points(a,b):
    count_a = 1
    count_b = 1
    for row in Lmatrix:
        if(row[0] == a):
            count_a = row[3]
        elif(row[0] == b):
            count_b = row[3]
#     print(count_a)
#     print(count_b)
    return count_a + count_b

def get_id(a):
    a_id = a
    for row in Lmatrix:
        if(a_id == row[0] or a_id == row[1]):
            a_id = row[4]
        if(row[0] == math.inf):
            break
    return a_id

def get_row(a,b):
    r1 = simMatrix[a]
    r2 = simMatrix[b]
    sum1 = 0
    sum2 = 0
    for i in r1:
        if(i != math.inf):
            sum1 += i
    for i in r2:
        if(i != math.inf):
            sum2 += i
    return r1 if sum1 < sum2 else r2


# In[322]:


#combine everyting
for i in range(simMatrix.shape[0]):
#     print(i)
    #find closest pairs of clusters from matrix
    min_dist = np.min(simMatrix)
    minim = np.where(simMatrix == min_dist)
    x,y = minim
    #single linkage to find minimum of entries of both rows and merge clusters
    row1 = simMatrix[x[0]]
    row2 = simMatrix[y[0]]
#     row3 = get_row(x[0],y[0])
    row3 = np.where(row1 > row2,row2,row1)  #for max change to '>'
    simMatrix[:,x[0]] = row3
    simMatrix[x[0]] = row3
    simMatrix[y[0]] = math.inf
    simMatrix[:,y[0]] = math.inf
    simMatrix[x[0]][y[0]] = math.inf
    simMatrix[x[0]][x[0]] = math.inf
    #update Linkage matrix
#     points = get_points(x[0],y[0])
    Lmatrix[i][3] = get_points(x[0],y[0])
    Lmatrix[i][0] = get_id(x[0])
    Lmatrix[i][1] = get_id(y[0])
    Lmatrix[i][4] = simMatrix.shape[0] + i
    Lmatrix[i][2] = min_dist
#     print(Lmatrix[i][3])


# In[323]:


final_l = Lmatrix[:-1,:-1]


# In[324]:


plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    final_l,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()
plt.savefig('AHC1.jpg')


# In[ ]:




