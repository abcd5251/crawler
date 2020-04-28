# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:30:32 2020

@author: 朱瑋民
"""
import sklearn
from sklearn import datasets

from sklearn import svm
from sklearn import metrics 

from sklearn.neighbors import KNeighborsClassifier

cancer=datasets.load_breast_cancer()
#print(cancer)
#print(cancer.feature_names)
#print(cancer.target_names)

x=cancer.data
y=cancer.target  #用內建的dataset 來抓裡面的資料

x_train,x_test,y_train,y_test=sklearn.model_selection.train_test_split(x,y,test_size=0.2)

print(x_train,y_train)

classes=['malignant' 'benign']#目標y_train


clf=svm.SVC(kernel="linear",C=2)#畫線
clf.fit(x_train,y_train)

y_pred=clf.predict(x_test)

acc=metrics.accuracy_score(y_test,y_pred)
print(acc)
