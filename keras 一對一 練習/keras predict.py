# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:56:07 2020

@author: 朱瑋民
"""
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, LSTM, TimeDistributed, RepeatVector
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt

def readdata():
    train=pd.read_csv("result.csv")
    return train

def addfeature(train):
    date=train["日期"] #轉換 
    for i in range(len(date)):
        date.iloc[i]=date.iloc[i].replace(date.iloc[i][0:3],str(int(date.iloc[i][0:3] ) + 1911 ))# 轉換 成西元 iloc基於行索引和列索引（index，columns） 都是從 0 開始
    train["日期"]=pd.to_datetime(train["日期"],yearfirst=True, errors='coerce')
    train["month"]=train["日期"].dt.month
    train["day"]=train["日期"].dt.day
    train["weeknumber"] = train["日期"].dt.dayofweek
    return train

def normalize(train):
  train = train.drop(["日期"], axis=1)#axis=1表示對縱軸操作
  train_norm = train.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))
  return train_norm


def buildTrain(train, pastDay=30, futureDay=5):
  X_train, Y_train = [], []
  for i in range(train.shape[0]-futureDay-pastDay):
    X_train.append(np.array(train.iloc[i:i+pastDay]))#iloc用數字來算
    Y_train.append(np.array(train.iloc[i+pastDay:i+pastDay+futureDay]["收盤價"]))
  return np.array(X_train), np.array(Y_train)#一次train 30 天加預測五天

def shuffle(X,Y):
  np.random.seed(10)
  randomList = np.arange(X.shape[0])#使用shape[0]讀取矩陣第一维度的長度
  np.random.shuffle(randomList)#亂洗順序  橫著打亂
  return X[randomList], Y[randomList]#將資料打散  讓他們不是照時間排序
def splitData(X,Y,rate):
   X_train = X[int(X.shape[0]*rate):] #從int(X.shape[0]*rate)開始跑 不指定結束
   #取一些做validation data  
   Y_train = Y[int(Y.shape[0]*rate):]#Validation Data則是用來挑選以及修改model的
   X_val = X[:int(X.shape[0]*rate)]#一個好的model他的表現再Training Data以及Validation Data上應該要差不多，
   #如果他在Testing Data的表現很好，但是在Validation Data的表現很糟，此時就是處於Overfitting的狀態，但是如果他在Testing Data的表現就很糟，那麼就是Underfitting了。
   Y_val = Y[:int(Y.shape[0]*rate)]
   return X_train, Y_train, X_val, Y_val

def build_one_to_one_model(shape):
     model = Sequential()
     model.add(LSTM(100, input_length=shape[1], input_dim=shape[2],return_sequences=True))
     # output shape: (1, 1)
     
     model.add(TimeDistributed(Dense(1)))    # or use model.add(Dense(1))
     model.compile(loss="mean_squared_error", optimizer="adam",metrics=["accuracy"])
     model.summary()# loss val_loss validation data 的loss   train test validation  train 跟test 拿來訓練  validation 拿來驗證  loss全部都要減少
     return model


if __name__ == '__main__':
    train=readdata()
    train_feature=addfeature(train)
    train_normalize=normalize(train_feature)
    
    x_train,y_train=buildTrain(train_normalize,1,1)
    
    x_train,y_train=shuffle(x_train,y_train)
    
    X_train, Y_train, X_val, Y_val= splitData(x_train,y_train,0.1)
    #np.newaxis轉變矩陣形狀
    Y_train=Y_train[:,np.newaxis]
    Y_val=Y_val[:,np.newaxis]
   
    print(Y_train)
    model=build_one_to_one_model(x_train.shape)
    callback=EarlyStopping(monitor="loss",patience=10, verbose=1, mode="auto")
    model.fit(X_train, Y_train, epochs=1000, batch_size=128, validation_data=(X_val, Y_val), callbacks=[callback])

    
    
    
    
    