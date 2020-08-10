# -*- coding: utf-8 -*-
"""Divisive.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dEGaZPawuFoGNMk4wUe6iMLq2Ql9Lst2

**IMPORT DATASET**
"""

!wget 'http://genome.crg.es/datasets/ggalhsapgenes2005/hg16.311.putative.aa.fa'

!pip install biopython
!pip install dna_features_viewer
!ls

"""### **Parsing FASTA file into a dataframe**"""

from Bio.SeqIO.FastaIO import SimpleFastaParser
from numpy import *
import pandas as pd
# dataset = df.Dataframe[]
with open('hg16.311.putative.aa.fa') as file: 
    title = []
    length = []
    sequences = []
    for name, dna_sequence in SimpleFastaParser(file):
        title.append(name.split(None, 1)[0])
        sequences.append(dna_sequence)
        length.append(len(dna_sequence))

df = pd.DataFrame({'ID':title, 'sequence':sequences,'length':length})
df.head(5)

!pip install plotly

"""**Upload Matrix**"""

from google.colab import files
files.upload()

import pandas as pd
from numpy import *
similarity_df=pd.read_csv('matrix_np1.csv', sep=',',header=None)
similarity_np = loadtxt('matrix_np1.csv', delimiter=',')
z = similarity_np
data = arange(shape(z)[0])
data = data.reshape(len(data), 1)

from sklearn.preprocessing import normalize
#matrix = arange(0,27,3).reshape(3,3).astype(float64)
for i in range(len(z)):
  z[i,i] = 1
z = 1/z
for i in range(len(z)):
  z[i,i] = 0
z

"""## DIVISIVE CLUSTERING"""

def distEclud(vecA, vecB):
  return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):
  n = shape(dataSet)[1]
  centroids = mat(zeros((k,n)))
  for j in range(n):
    centroids[:,j] = [dataSet[x,0] for x in random.randint(len(dataSet),size=(k,1)).tolist()] 
  return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m,2)))
  centroids = createCent(dataSet, k).astype(int)
  clusterChanged = True
  while clusterChanged:
    clusterChanged = False
    for i in range(m):
      minDist = inf; minIndex = -1
      for j in range(k):
        distJI = z[centroids[j,0]][dataSet[i]]
       # distJI = z1[centroids[j,0]][dataSet[i]]
        if distJI < minDist:
          minDist = distJI; minIndex = j
      if clusterAssment[i,0] != minIndex: clusterChanged = True
      clusterAssment[i,:] = minIndex,minDist
       
    for cent in range(k):
      ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
      ptsInClust = ptsInClust.reshape(len(ptsInClust))
      minDist = inf; minIndex = -1
      for pt in ptsInClust:
        distPt = sum([ z[pt][x] for x in ptsInClust])
        if distPt < minDist:
          minDist = distPt
          minIndex = pt
      centroids[cent,:] = minIndex
            
  return centroids, clusterAssment

ce,ass = kMeans(data,2)
ce

def divisive(dataSet, k, count, distMeas=distEclud):
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m,2)))
  minDist = inf; minIndex = -1
  for pt in range(len(data)):
    distPt = sum([ z[pt][x] for x in range(len(data)) ])
    if distPt < minDist:
      minDist = distPt
      minIndex = pt
  centroid0 = minIndex
  centList =[centroid0]
  for j in range(m):
    clusterAssment[j,1] = z[centroid0][j]
    
  while (len(centList) < k):
    lowestSSE = inf
    for i in range(len(centList)):
      ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
      if(len(ptsInCurrCluster) < 1):
        continue
      centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2 , distMeas)
      sseSplit = sum(splitClustAss[:,1])
      sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
      #print("sseSplit, and notSplit: ",sseSplit,sseNotSplit)
      if (sseSplit + sseNotSplit) < lowestSSE:
        bestCentToSplit = i
        bestNewCents = centroidMat
        bestClustAss = splitClustAss.copy()
        lowestSSE = sseSplit + sseNotSplit
    
    temp1 = nonzero(bestClustAss[:,0].A == 1)[0]
    temp2 = nonzero(bestClustAss[:,0].A == 0)[0]
  
    X[count] = array([bestCentToSplit, len(centList), lowestSSE, len(temp1)+len(temp2)])
    count = count + 1
    
    bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)
    bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
    #print ('the bestCentToSplit is: ',bestCentToSplit)
    #print ('the len of bestClustAss is: ', len(bestClustAss), '\n')
    
    centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]
    centList.append(bestNewCents[1,:].tolist()[0])
    clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss
  return mat(centList), clusterAssment

X = zeros((len(data),4))
count = 0
centList, clusterAssment = divisive(data, 310, count)
#centList



from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt

#dendrogram(linkage(squareform(z)))
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    linkage(squareform(z)),
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.savefig("Div.png")