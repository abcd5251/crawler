# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 00:20:45 2020

@author: 朱瑋民
"""
import pandas as pd
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import Sequential
import sklearn
from sklearn import linear_model
import numpy as np
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

data=pd.read_csv("result.csv")

data=data[["成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]]
predict="收盤價"
x=np.array(data.drop([predict],1))
y=np.array(data[predict])

best=0 
x_train, x_test, y_train, y_test=sklearn.model_selection.train_test_split(x,y,test_size=0.1)#因為每次都會有不同的training data
#90% 10% 但裡面取的是隨機的
for _ in range(30):
    x_train, x_test, y_train, y_test=sklearn.model_selection.train_test_split(x,y,test_size=0.1)
    linear=linear_model.LinearRegression()
    
    linear.fit(x_train,y_train)
    acc=linear.score(x_test,y_test)
    print(acc)

    if acc>best:
        best=acc
        
        with open("stock.pickle","wb") as f:
            pickle.dump(linear,f)    #這段可以不用  當有Pickle的時候 只是用來存入pickle 
#且可以用多次迴圈找出最佳  每次for 去跑的值會不同

pickle_in=open("stock.pickle","rb")
linear=pickle.load(pickle_in)

print('Coefficient:\n',linear.coef_)#coefficient 為係數
print('Intercept:\n',linear.intercept_)#intercept 為截距

predictions=linear.predict(x_test)
for x in range(len(predictions)):
    print(predictions[x],x_test[x],y_test[x]) #prediction 為預測的值 x_test為實際的值不包含測試值  y為預測的值
#y都為要預測的東西
p='開盤價'

style.use("ggplot")
pyplot.scatter(data[p],data["收盤價"])
pyplot.xlabel(p)
pyplot.ylabel("result")
pyplot.show()



    




