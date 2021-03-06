# -*- coding: utf-8 -*-
"""K-Means.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-ZkCvIxGgQTCIqDAaogynncujXKVoY7h

# Importing Dataset

Also installing BioPython for faster parsing of fasta files
"""

!wget 'http://genome.crg.es/datasets/ggalhsapgenes2005/hg16.311.putative.aa.fa'

!pip install biopython

!pip install dna_features_viewer

!ls

"""# Parsing FASTA file into a dataframe"""

from Bio.SeqIO.FastaIO import SimpleFastaParser
import numpy as np
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

"""# Needleman-Wunsch Algorithm for Similarity matrix"""

def score(seq1,seq2):
  gap = 2
  substitution = 1
  match = 0
  len1 = len(seq1)
  len2 = len(seq2)
#   print(seq1)
#   print(seq2)
#   print(opt)
  i=0
  j=0
  opt = np.zeros(shape=(len1+1,len2+1))
  for i in range (1,len1+1):
    opt[i][0] = opt[i-1][0] + gap
    i=i+1
#     print("i")
  for j in range (1,len2+1):
    opt[0][j] = opt[0][j-1] + gap
    j=j+1
#     print("j")
  
  for i in range(1,len1+1):
    for j in range(1,len2+1):
      add_score = match if seq1[i-1] == seq2[j-1] else substitution 
      score_diag = opt[i-1][j-1] +  add_score
      score_left = opt[i][j-1] + gap
      score_up = opt[i-1][j] + gap
      opt[i][j] = min(score_diag, score_left, score_up)
      j=j+1
    i=i+1
  
#   print(opt)
  similarity = opt[i-1][j-1]
  del opt
  return similarity

df_len = len(df.index)
matrix = pd.DataFrame(np.zeros(df_len*df_len).reshape(df_len,df_len))
matrix1 = np.zeros(shape=(df_len,df_len))

print(df_len)
# df.iloc[1,2]

from IPython.display import clear_output

for i in range(0,df_len):
  for j in range(0,df_len):
    similarity = score(df.iloc[i,2],df.iloc[j,2])
    matrix[j][i] = similarity
    matrix1[i][j] = similarity
    print(str(i) + " " + str(j) + " " + str(similarity))
    j = j+1
  i = i+1
  clear_output()

print(matrix1)
matrix.to_csv('matrix_pd1.csv')
from google.colab import files

np.savetxt("matrix_np1.csv", matrix1, delimiter=",")
# files.download('matrix_pd1.csv')
files.download('matrix_np1.csv')

"""## Code for generating **dotplot**"""

def delta(x,y):
  if x == y:
    return 0
  return 1

def M(seq1,seq2,i,j,k):
  return sum(delta(x,y) for x,y in zip(seq1[i:i+k],seq2[j:j+k]))
  
def makeMatrix(seq1,seq2,k):
  n = len(seq1)
  m = len(seq2)
  return [[M(seq1,seq2,i,j,k) for j in range(m-k+1)] for i in range(n-k+1)]

def plotMatrix(M,t, seq1, seq2, nonblank = chr(0x25A0), blank = ' '):
    print(' |' + seq2)
    print('-'*(2 + len(seq2)))
    for label,row in zip(seq1,M):
        line = ''.join(nonblank if s < t else blank for s in row)
        print(label + '|' + line)
        
def dotplot(seq1,seq2,k = 1,t = 1):
    M = makeMatrix(seq1,seq2,k)
    plotMatrix(M, t, seq1,seq2) #experiment with character choice

seqx = df.iloc[0,0]
seqy = df.iloc[1,0]
dotplot(seqx,seqy)
# print(seqx)
print(seqy)

"""# Code - K-Means

## Upload the similarity matrix
"""

from google.colab import files
files.upload()

"""## Import the file as an array
## Import required libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import math
import warnings
warnings.filterwarnings("ignore")

"""## Import Similarity matrix

Setup the dataset
"""

similarity_df=pd.read_csv('matrix_np1.csv', sep=',',header=None)
similarity_np = np.loadtxt('matrix_np1.csv', delimiter=',')
z = similarity_np
data = np.zeros((311*311,2),dtype='int')
print(data.shape)
k = 0
for i in range(0,311):
  for j in range(0,311):
    data[k][0] = int(i)
    data[k][1] = int(j)
    k = k+1
    j = j+1
  i = i+1

print(k)

"""## Clustering"""

class K_means:
  def __init__(self,k=3,tolerance=0.000,max_iterations = 800):
    z = (similarity_np)
    self.k = k
    self.tol = tolerance
    self.iter = max_iterations
  

  def get_dist(self,x,y):
    return z[int(x)][int(y)]
  
  def fit(self,data):
    data = data[0:311,1]
    self.centroids = {}
    print("Initial Points")
    for i in range(self.k):
#       self.centroids[i] = data[random.randint(0,311)]
      self.centroids[i] = data[i*int(300/self.k)]
      print(self.centroids[i])
      
      
    for i in range(self.iter):
      self.classes = {}
      for j in range(self.k):
        self.classes[j] = []
        
      for feature in data:
        distances = [self.get_dist(feature,self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        self.classes[classification].append(feature)
        
      previous_centroids = dict(self.centroids)
      for classification in self.classes:
        min_dist = math.inf
        median = 0
        for x in self.classes[classification]:
          dist = 0
          for y in self.classes[classification]:
            dist += self.get_dist(x,y)
          if dist < min_dist:
            min_dist = dist
            median = x
        self.centroids[classification] = median

      opt= True
      for c in self.centroids:
        orig_centroid = previous_centroids[c]
        cur_centroid = self.centroids[c]
        check_dist = self.get_dist(cur_centroid,orig_centroid)/10000
#         print(check_dist)
        if check_dist > self.tol:
          opt = False
          
      if opt:
        break
#       print(i)

k = 4
amino_acid = K_means(k)
amino_acid.fit(data)
print("Number of Clusters: " + str(k))
print("Centroids")
print(amino_acid.centroids)
print("Clusters")
for classification in amino_acid.classes:
  print(amino_acid.classes[classification])

"""# Results

## k = 2

Number of Clusters: 2

Centroids  {154,  96}

Cluster 1

> [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 13, 14, 21, 22, 23, 24, 27, 31, 33, 36, 37, 38, 39, 40, 41, 44, 45, 46, 48, 49, 50, 51, 53, 55, 56, 57, 58, 59, 60, 63, 64, 66, 67, 68, 69, 70, 73, 74, 76, 78, 80, 81, 82, 84, 85, 86, 87, 88, 89, 90, 91, 92, 95, 97, 99, 100, 102, 103, 104, 105, 106, 107, 109, 110, 113, 114, 115, 118, 119, 120, 121, 123, 124, 125, 127, 128, 129, 130, 131, 134, 136, 137, 140, 141, 142, 143, 144, 147, 149, 151, 152, 154, 155, 157, 158, 159, 160, 162, 164, 165, 166, 167, 168, 169, 170, 172, 175, 176, 177, 178, 180, 181, 183, 185, 186, 187, 191, 193, 195, 197, 199, 200, 202, 203, 207, 208, 210, 211, 212, 213, 215, 216, 217, 220, 221, 225, 226, 227, 229, 231, 232, 233, 234, 237, 239, 242, 243, 247, 250, 251, 255, 256, 258, 259, 260, 262, 264, 265, 266, 269, 270, 272, 273, 274, 276, 277, 278, 279, 280, 281, 283, 285, 286, 288, 289, 290, 292, 294, 295, 296, 298, 299, 300, 301, 302, 304, 305, 308, 309, 310]

Cluster 2

> [8, 11, 12, 15, 16, 17, 18, 19, 20, 25, 26, 28, 29, 30, 32, 34, 35, 42, 43, 47, 52, 54, 61, 62, 65, 71, 72, 75, 77, 79, 83, 93, 94, 96, 98, 101, 108, 111, 112, 116, 117, 122, 126, 132, 133, 135, 138, 139, 145, 146, 148, 150, 153, 156, 161, 163, 171, 173, 174, 179, 182, 184, 188, 189, 190, 192, 194, 196, 198, 201, 204, 205, 206, 209, 214, 218, 219, 222, 223, 224, 228, 230, 235, 236, 238, 240, 241, 244, 245, 246, 248, 249, 252, 253, 254, 257, 261, 263, 267, 268, 271, 275, 282, 284, 287, 291, 293, 297, 303, 306, 307]


## k = 3

Number of Clusters: 3

Initial Points: 168 170 227

Centroids  {63, 150,  82}

Cluster 1

> [3, 6, 7, 9, 23, 27, 31, 39, 44, 46, 53, 55, 56, 58, 63, 64, 66, 67, 73, 74, 76, 86, 88, 92, 100, 103, 105, 106, 110, 121, 123, 124, 127, 129, 134, 140, 143, 144, 154, 157, 159, 160, 162, 165, 166, 167, 168, 170, 178, 180, 183, 185, 186, 191, 193, 202, 208, 210, 212, 217, 225, 226, 232, 233, 234, 239, 243, 256, 258, 260, 264, 266, 269, 272, 278, 280, 281, 283, 285, 290, 304, 305, 308, 310]

Cluster 2

> [0, 1, 2, 4, 5, 10, 13, 14, 16, 18, 21, 22, 24, 25, 26, 29, 30, 33, 36, 37, 38, 40, 41, 43, 45, 48, 49, 50, 51, 57, 59, 60, 65, 68, 69, 70, 72, 78, 80, 81, 82, 84, 85, 87, 89, 90, 91, 95, 97, 99, 102, 104, 107, 109, 111, 113, 114, 115, 118, 119, 120, 125, 126, 128, 130, 131, 132, 136, 137, 141, 142, 145, 146, 147, 148, 149, 151, 152, 155, 156, 158, 164, 169, 172, 175, 176, 177, 179, 181, 182, 187, 195, 196, 197, 199, 200, 203, 204, 205, 207, 209, 211, 213, 215, 216, 218, 220, 221, 227, 229, 231, 235, 237, 241, 242, 245, 247, 249, 250, 251, 252, 255, 259, 261, 262, 265, 268, 270, 273, 274, 276, 277, 279, 286, 288, 289, 292, 294, 295, 296, 298, 299, 300, 301, 302, 306, 309]

Cluster 3

> [8, 11, 12, 15, 17, 19, 20, 28, 32, 34, 35, 42, 47, 52, 54, 61, 62, 71, 75, 77, 79, 83, 93, 94, 96, 98, 101, 108, 112, 116, 117, 122, 133, 135, 138, 139, 150, 153, 161, 163, 171, 173, 174, 184, 188, 189, 190, 192, 194, 198, 201, 206, 214, 219, 222, 223, 224, 228, 230, 236, 238, 240, 244, 246, 248, 253, 254, 257, 263, 267, 271, 275, 282, 284, 287, 291, 293, 297, 303, 307]


## k = 4

Initial Points 0 75 150 225

Number of Clusters: 4

Centroids {104, 263, 96, 266}

Clusters
> [0, 5, 10, 13, 14, 16, 22, 24, 26, 29, 30, 33, 36, 37, 38, 40, 41, 43, 45, 48, 49, 50, 51, 57, 59, 60, 65, 68, 69, 72, 78, 82, 84, 85, 87, 89, 90, 91, 95, 97, 99, 102, 104, 107, 109, 111, 113, 114, 115, 118, 119, 120, 125, 128, 130, 131, 132, 136, 137, 141, 142, 145, 147, 149, 152, 155, 169, 175, 176, 177, 179, 181, 182, 187, 195, 197, 200, 203, 204, 207, 213, 216, 218, 221, 227, 231, 237, 241, 242, 247, 250, 251, 252, 255, 261, 262, 265, 268, 270, 273, 274, 276, 277, 279, 286, 289, 292, 294, 295, 296, 298, 299, 300, 301, 302, 306, 309]

>[8, 15, 28, 32, 61, 83, 93, 101, 117, 122, 133, 135, 138, 153, 163, 192, 214, 219, 222, 223, 224, 238, 240, 257, 263, 284, 297, 303]

> [11, 12, 17, 18, 19, 20, 25, 34, 35, 42, 47, 52, 54, 62, 71, 75, 77, 79, 94, 96, 98, 108, 112, 116, 126, 139, 146, 148, 150, 156, 161, 171, 173, 174, 184, 188, 189, 190, 194, 196, 198, 201, 205, 206, 209, 228, 230, 235, 236, 244, 245, 246, 248, 249, 253, 254, 267, 271, 275, 282, 287, 291, 293, 307]

> [1, 2, 3, 4, 6, 7, 9, 21, 23, 27, 31, 39, 44, 46, 53, 55, 56, 58, 63, 64, 66, 67, 70, 73, 74, 76, 80, 81, 86, 88, 92, 100, 103, 105, 106, 110, 121, 123, 124, 127, 129, 134, 140, 143, 144, 151, 154, 157, 158, 159, 160, 162, 164, 165, 166, 167, 168, 170, 172, 178, 180, 183, 185, 186, 191, 193, 199, 202, 208, 210, 211, 212, 215, 217, 220, 225, 226, 229, 232, 233, 234, 239, 243, 256, 258, 259, 260, 264, 266, 269, 272, 278, 280, 281, 283, 285, 288, 290, 304, 305, 308, 310]
"""