
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import csv
import itertools
from itertools import chain,combinations


# In[185]:


min_support = 0.006
min_confidence = 0.5
transactions = list()
L1 = set()
with open('groceries.csv',newline = '') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        transactions.append(set(row))
        for item in row:
            L1.add(frozenset([item]))


# In[186]:


def pruned_itemset(global_support,itemset,minSupport,transactions):
    set1 = set() #contains pruned set of items
    supcount = dict() #stores support count for those pruned itemsets
    for item in itemset:
        for _ in transactions:
            if(set(item) <= set(_)):
                if(item in supcount.keys()):
                    supcount[item] += 1
                else: supcount[item] = 1
                if(item in global_support.keys()):
                    global_support[item] += 1
                else: global_support[item] = 1
    for item,sup_count in supcount.items():
        if(sup_count / len(transactions) >= minSupport):
            set1.add(item)
    return set1


# In[187]:


def self_join(Lset,k): #Here Lset is L(k-1), and Lset_k is L(k+1)
    join = []
    for set1 in Lset:
        for set2 in Lset:
            a = set1.union(set2)
            if(len(a) == k):
                join.append(a)
    return(set(join))


# In[188]:


def Apriori(minSupport):
    freq_itemsets = dict() #used to generate rules
    all_itemset_support = dict()
    k = 1
    C = pruned_itemset(all_itemset_support,L1,min_support,transactions)
    L = C
    freq_itemsets[k] = L
    k = k + 1
    while(L != set()):
        L = self_join(L,k)
        C = pruned_itemset(all_itemset_support,L,min_support,transactions)
        L = C
        freq_itemsets[k] = L
        k = k + 1    
    return freq_itemsets,all_itemset_support


# In[189]:


a,b = Apriori(min_support)
# print(a)
# print(b)

# In[190]:


def gen_rules(min_confidence,a,b):
    rules = []
    c = list(a[2])
    k = 2
    while(c != list()):
        for each in c:
            temp = list(each)
            u = chain(*[combinations(temp, i + 1) for i in range(len(temp))])
            q = [x for x in u]
            for _ in q:
                p = frozenset(_)
                diff = each.difference(p)
                if(len(diff) > 0):
                    conf = b[each] / b[p]
                    if(conf >= min_confidence):
                        rules.append([p,diff,conf])
        k = k + 1
        c = list(a[k])
    return rules


# In[191]:


c = gen_rules(min_confidence,a,b)


# In[192]:


F = []
q = a[1]
k = 1
while(q != set()):
    for each in q:
        F.append(each)
    k = k + 1
    q = a[k]


# In[140]:


with open('s0.006.csv','a') as file:
    writer = csv.writer(file)
    for _ in F:
        row = [list(_),b[_]]
        print(row)
        writer.writerow(row)


# In[193]:


with open('c0.05.csv','a') as file:
    writer = csv.writer(file)
    for _ in c:
        row = [list(map(list,_[0:-1])),_[-1]]
        writer.writerow(row)


# In[ ]:




