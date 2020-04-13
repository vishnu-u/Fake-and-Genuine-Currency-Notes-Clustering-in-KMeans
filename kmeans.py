#Currency Genuinity Analysis using KMeans in Python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
#from yellowbrick.cluster import KElbowVisualizer

#reading database and removing NULL values if any
data=pd.read_csv("banknotes.csv")
data.dropna()

#Extracting values
x=data['V1']
y=data['V2']


print("X_max : ",x.max())
print("X_min : ",x.min())
print("Y_max : ",y.max())
print("Y_min : ",y.min())

#performing normaliztion
mean_x=x.mean()
mean_y=y.mean()
max_x=x.max()
max_y=y.max()
min_x=x.min()
min_y=y.min()

for i in range(0,x.size):
    x[i] = (x[i] - mean_x) / (max_x - min_x)

for i in range(0,y.size):
    y[i] = (y[i] - mean_y) / (max_y - min_y)

#Performing Clustering
res=KMeans(n_clusters=2,max_iter=243).fit(np.column_stack((x,y)))

#Separating values belonging to Cluster 0 and Cluster 1
#Helps visualization easier by using different colour for different clusters
xval_0=[]
yval_0=[]
xval_1=[]
yval_1=[]

for i in range(0,x.size):
    if(res.labels_[i] == 0):
        xval_0.append(x[i])
        yval_0.append(y[i])
    else:
        xval_1.append(x[i])
        yval_1.append(y[i])


#Plotting the values and cluster centres
plt.scatter(xval_0,yval_0,c="red")
plt.scatter(xval_1,yval_1,c="green")
plt.scatter(res.cluster_centers_[:,0],res.cluster_centers_[:,1],c="black")
plt.xlabel("V1")
plt.ylabel("V2")
plt.show()
