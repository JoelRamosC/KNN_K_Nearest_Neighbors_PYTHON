# -*- coding: utf-8 -*-

# fonte https://realpython.com/knn-python/

import pandas as pd
import matplotlib.pyplot as plt

url = ("https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data")
abalone = pd.read_csv(url, header=None)

#check
abalone.head()

abalone.columns = [
         "Sex",
         "Length",
         "Diameter",
         "Height",
         "Whole weight",
         "Shucked weight",
         "Viscera weight",
         "Shell weight","Rings",]

abalone = abalone.drop("Sex", axis =1)

abalone["Rings"].hist(bins = 15)
plt.show()

#Scratch
#Search the correlation between the independent variables and goal variables
correlation_matrix = abalone.corr()
correlation_matrix["Rings"]

import numpy as np
a = np.array([2,2])
b = np.array([4,4])
#to obtain the distance between two vector points
np.linalg.norm(a-b) 

X = abalone.drop("Rings", axis = 1)
X = X.values
y = abalone["Rings"]
y = y.values

#new point
new_data_point = np.array([
         0.569552,
         0.446407,
         0.154437,
         1.016849,
         0.439051,
         0.222526,
         0.291208,
     ])

#calculate distances between new point and dataset points
distances = np.linalg.norm(X-new_data_point, axis = 1)

k = 3
#calculete the id or indices of the k nearest points 
nearest_neighbor_ids = distances.argsort()[:k] #indice grammar

nearest_neighbor_rings = y [ nearest_neighbor_ids]

# In regression problems, the target variable is numeric. You combine multiple neighbors into one prediction by taking the average of their values of the target variable. 

prediction = nearest_neighbor_rings.mean()

# # Instead, in the case of classification, you take the mode. The mode is the value that occurs most often.
# # The prediction is the value that occurs most often among the neighbors.
# If there are multiple modes, there are multiple possible solutions. You could select a final winner randomly from the winners. You could also make the final decision based on the distances of the neighbors, in which case the mode of the closest neighbors would be retained.

import scipy.stats
#exemplo of mode (be appear more)
class_neighbors = np.array(["A", "B", "B", "C"])
scipy.stats.mode(class_neighbors)

####### Using Scikit-learn #######

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=12345)

from sklearn.neighbors import KNeighborsRegressor
knn_model = KNeighborsRegressor(n_neighbors = 3)
knn_model.fit(X_train, y_train)

# #Evaluete step
#RMSE = Root mean square error
# 1- Compute the difference between each data point’s actual value and predicted value.
# 3- For each difference, take the square of this difference.
# 3- Sum all the squared differences.
# 4- Take the square root of the summed value.

from sklearn.metrics import mean_squared_error
from math import sqrt
#Evaluating the error with X_train
train_preds = knn_model.predict(X_train)
mse = mean_squared_error(y_train, train_preds)
rmse = sqrt(mse)
rmse #1,65

#Evaluating the error with X_test
test_preds = knn_model.predict(X_test)
mse = mean_squared_error(y_test, test_preds)
rmse = sqrt(mse)
rmse #237 (overfitting during the in step train)

# Plotting the fit of model
import seaborn as sns
#test_pedicted
cmap = sns.cubehelix_palette(as_cmap=True)
f, ax = plt.subplots()
points = ax.scatter(X_test[:, 0], X_test[:, 1], c=test_preds, s=50, cmap=cmap)
f.colorbar(points)
plt.show()

#y_test
cmap = sns.cubehelix_palette(as_cmap=True)
f, ax = plt.subplots()
points = ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, s=50, cmap=cmap)
f.colorbar(points)
plt.show()


# To find the best value for k, you’re going to use a tool called GridSearchCV. This is a tool that is often used for tuning hyperparameters of machine learning models. In your case, it will help by automatically finding the best value of k for your dataset.

# Using GridSearchCV to find a value for k has reduced the problem of overfitting on the training data.

from sklearn.model_selection import GridSearchCV
parameters = {"n_neighbors": range(1, 50)}
gridsearch = GridSearchCV(KNeighborsRegressor(), parameters)
gridsearch.fit(X_train, y_train)

#get the best result
gridsearch.best_params_

#training with the best parameter
train_preds_grid = gridsearch.predict(X_train)#predict whith the best params
train_mse = mean_squared_error(y_train, train_preds_grid)
train_rmse = sqrt(train_mse)
test_preds_grid = gridsearch.predict(X_test) 
test_mse = mean_squared_error(y_test, test_preds_grid)
test_rmse = sqrt(test_mse)
train_rmse
test_rmse

# weighted average instead of a regular average. This means that neighbors that are further away will less strongly influence the prediction.
parameters = {"n_neighbors": range(1, 50),"weights": ["uniform", "distance"],}
gridsearch = GridSearchCV(KNeighborsRegressor(), parameters)
gridsearch.fit(X_train, y_train)
gridsearch.best_params_
test_preds_grid = gridsearch.predict(X_test)
test_mse = mean_squared_error(y_test, test_preds_grid)
test_rmse = sqrt(test_mse)
test_rmse

# As a third step for kNN tuning, you can use bagging. Bagging is an ensemble method, or a method that takes a relatively straightforward machine learning model and fits a large number of those models with slight variations in each fit. Bagging often uses decision trees, but kNN works perfectly as well.

best_k = gridsearch.best_params_["n_neighbors"]
best_weights = gridsearch.best_params_["weights"]
bagged_knn = KNeighborsRegressor(n_neighbors=best_k,weights=best_weights)

from sklearn.ensemble import BaggingRegressor
bagging_model = BaggingRegressor(bagged_knn, n_estimators=100)

test_preds_grid = bagging_model.predict(X_test)
test_mse = mean_squared_error(y_test, test_preds_grid)
test_rmse = sqrt(test_mse)
test_rmse


# In this tutorial you learned how to:

# Understand the mathematical foundations behind the kNN algorithm
# Code the kNN algorithm from scratch in NumPy
# Use the scikit-learn implementation to fit a kNN with a minimal amount of code
# Use GridSearchCV to find the best kNN hyperparameters
# Push kNN to its maximum performance using bagging