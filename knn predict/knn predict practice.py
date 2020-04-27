# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 13:03:03 2020

@author: 朱瑋民
"""
import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

data=pd.read_csv("car.csv")

le=preprocessing.LabelEncoder() #數據處理  針對字串
#字串無法套入數學模型進行運算，在此先對其進行Label encoding編碼  產生數字(多個相同字串分類)
#當我們對其進行Label encoding後，模型會認為他們之間存在著0<1<2 數字為自動產生
buying=le.fit_transform(list(data["buying"]))
maint=le.fit_transform(list(data["maint"]))
door=le.fit_transform(list(data["door"]))
persons=le.fit_transform(list(data["persons"]))
lug_boot=le.fit_transform(list(data["lug_boot"]))
safety=le.fit_transform(list(data["safety"]))
cls=le.fit_transform(list(data["class"]))

print(buying)

predict="class"
x=list(zip(buying,maint,door,persons,lug_boot,safety))   #各式各樣的features

y=list(cls)    # label 要測的

x_train,x_test,y_train,y_test=sklearn.model_selection.train_test_split(x,y,test_size=0.1) 
#每次取得的都不一樣  0.1的範圍

model=KNeighborsClassifier(n_neighbors=9)#9個群體  假設欲預測點是 i
                                            #找出離 i最近的 k 筆資料多數是哪一類，預測 i 的類型
model.fit(x_train,y_train) #fit the model using x as training data  y as target values
acc=model.score(x_test,y_test) #正確率

predicted=model.predict(x_test)

names=["unacc","acc","good","vgood"]
for x in range(len(x_test)):
    print("Predicted:",names[predicted[x]],"Data:",x_test[x],"Actual:",names[y_test[x]])
    n=model.kneighbors([x_test[x]],9,True) # 9個neighbor 的群體  
    print("N: ",n) #第一個array為distance between all these points
                        #後面的array為different neighbor 有9個
