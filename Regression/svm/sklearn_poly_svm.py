# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 01:52:24 2017

@author: Megamindo_0
"""
__author__ = 'Peeyush Yadav'

import csv
import numpy as np
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold

def load_dataset(xy,x,y):
    
    with open('chessboard.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if row[0] != 'A':
                xy.append([float(row[0]),float(row[1]),int(row[2])])
                x.append([float(row[0]),float(row[1])])
                y.append(int(row[2]))
    
   
#    print ("x = ",x)
#    print ("y = ",y)
#    print ()

def plot_dataset(xy,x,y):
    A0 = [row[0] for row in xy if row[2] == 0]
    A1 = [row[0] for row in xy if row[2] == 1]
    B0 = [row[1] for row in xy if row[2] == 0]
    B1 = [row[1] for row in xy if row[2] == 1]
    plot0 = plt.scatter(A0,B0, marker='+', color = 'red')
    plot1 = plt.scatter(A1,B1, marker = 'o', color = 'green')
    plt.legend((plot0, plot1), ('label 0', 'label 1'), scatterpoints = 1)
    plt.title("Scatter Plot")
    plt.xlabel('A')
    plt.ylabel('B')
    plt.show()  

    
class Support_Vector_Machine :
    
    def __init__(self,dataset):
        self.dataset = dataset
        self.X_train = []
        self.Y_train = []
        self.X_test = []
        self.Y_test = []
        self.stratified_sampling(dataset)
        
    def stratified_sampling(self,xy):
        self.Y = [row[2] for row in xy]
        self.X = [(row[0],row[1]) for row in xy]
        self.skf = StratifiedKFold(n_splits= 5)
        
    def poly_svm(self):
        errorPenalty = [10**-2, 1, 5]
        degree = [3,4,5]
        self.bestScoreErrorPenalty = 1
        self.bestScoreDegree = 0
        bestScore = 0
        for c in errorPenalty:
            for d in degree :
                score = 0
                for train_ind, test_ind in self.skf.split(self.X,self.Y):
                    self.X_train = [self.X[ind] for ind in train_ind]
                    self.Y_train = [self.Y[ind] for ind in train_ind]
                    self.X_test = [self.X[ind] for ind in test_ind]
                    self.Y_test = [self.Y[ind] for ind in test_ind]
                    clf = svm.SVC(kernel = 'poly', C = c, degree = d).fit(self.X_train,self.Y_train)
                    score = score + clf.score(self.X_test, self.Y_test )
                if score > bestScore :
                    bestScore = score
                    self.bestScoreErrorPenalty = c
                    self.bestScoreDegree = d
                print ("Mean score for C(",c,"),d(",d,"):",(score/float(5))*100,"%")
                 
    def plot_svm(self):
        c = self.bestScoreErrorPenalty
        d = self.bestScoreDegree
        A0 = [row[0] for row in self.dataset if row[2] == 0]
        A1 = [row[0] for row in self.dataset if row[2] == 1]
        B0 = [row[1] for row in self.dataset if row[2] == 0]
        B1 = [row[1] for row in self.dataset if row[2] == 1]
        Xplot = []
        Yplot = []   
        Xplot, Yplot = np.meshgrid(np.arange(-0.2, 4.4, 0.2),np.arange(-0.2, 4.4, 0.2))
        clf = svm.SVC(kernel = 'poly', C = c, degree = d).fit(self.X,self.Y)
        predicted = clf.predict(np.c_[Xplot.ravel(), Yplot.ravel()])
        predicted = predicted.reshape(Xplot.shape)             
        plot0 = plt.scatter(A0,B0, marker='+', color = 'red')
        plot1 = plt.scatter(A1,B1, marker = 'o', color = 'green')
        plt.legend((plot0, plot1), ('label 0', 'label 1'), scatterpoints = 1)
        plt.xlabel('A')
        plt.ylabel('B')
        plt.title("Polynomial kernel")
        plt.contourf(Xplot, Yplot, predicted, alpha=0.5)
        plt.show()

        
if __name__ == "__main__":
    dataset=[]
    dataset_x = []
    dataset_y = []
    load_dataset(dataset,dataset_x,dataset_y)
    plot_dataset(dataset,dataset_x,dataset_y)

    svc = Support_Vector_Machine(dataset)
    svc.poly_svm()
    svc.plot_svm()
   
    