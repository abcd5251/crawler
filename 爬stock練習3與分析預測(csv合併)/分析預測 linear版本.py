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
data=pd.read_csv("result.csv")

data=data[["成交股數","成交金額","開盤價","最高價","最低價","收盤價","漲跌價差","成交筆數"]]
predict="收盤價"
x=np.array(data.drop([predict],1))
y=np.array(data[predict])
x_train, x_test, y_train, y_test=sklearn.model_selection.train_test_split(x,y,test_size=0.1)
linear=linear_model.LinearRegression()

linear.fit(x_train,y_train)
acc=linear.score(x_test,y_test)
print(acc)

print('Coefficient:\n',linear.coef_)#coefficient 為係數
print('Intercept:\n',linear.intercept_)#intercept 為截距

predictions=linear.predict(x_test)
for x in range(len(predictions)):
    print(predictions[x],x_test[x],y_test[x]) #prediction 為預測的值 x_test為實際的值不包含測試值  y為預測的值





    




