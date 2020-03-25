# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 16:17:20 2020

@author: 朱瑋民
"""
import time
import pandas as pd
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys#鍵盤的操作
from selenium.webdriver.common.action_chains import ActionChains#滑鼠的操作
from bs4 import BeautifulSoup
from bokeh.plotting import figure, output_file, show
from bokeh.plotting import ColumnDataSource
from bokeh.models import CategoricalColorMapper
from bokeh.models import HoverTool
from bokeh.models.widgets import Dropdown, Tabs, Panel
from bokeh.layouts import column

URL = "https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html"
driver = None
def start_driver():
    global driver
    print("啟動 WebDriver...")
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(5)
    
def close_driver():
    global driver
    driver.quit()
    print("關閉 WebDriver...")
    
def get_page(url):
    global driver
    print("取得網頁...")
    driver.get(url)
    time.sleep(2)
def visualize(mm):
    df = pd.read_csv(mm+".csv", encoding="utf8")
    prices=df["收盤價"]
    average=sum(prices)/len(prices)
    decides=[]
    for price in prices:
        if price>=average:
           decides.append("較高")
        else:
           decides.append("較低")
    df.insert(9,'decide',decides)
    tech_stocks = ["較高","較低"]
    dates=df["日期"]
    numbers=[]
    for date in dates:
        if date[7]!=0:
            temping=int(date[7:9]) #轉int 要在list指派過去的時候轉
            
        elif date[7]==0:
            temping=int(date[8:9]) #轉int 要在list指派過去的時候轉        
        numbers.append(temping)#temping 不能在這邊轉 或是往前指派轉  會出錯猜可能是因為那是list
        
   
    df.insert(10,'number',numbers)    
    
    c_map = CategoricalColorMapper(
           factors=tech_stocks, 
           palette=["red","blue"])
    
    data = ColumnDataSource(data={
        "date": df["日期"],
        "open": df["開盤價"],
        "high": df["最高價"],
        "low": df["最低價"],
        "minus": df["漲跌價差"],
        "leave": df["收盤價"],
        "deal": df["成交股數"],
        "decide": df["decide"],
        "number": df["number"]
        })
    
    hover_tool = HoverTool(tooltips = [
             ("日期", "@date"),
             ("收盤價", "@leave"),
             ("開盤價", "@open"),
             ("最高價", "@high"),
             ("最低價", "@low"),
             ("漲跌價差", "@minus")
             ])
  
    p = figure(title=mm+"的日期與收盤價", 
           plot_height=500, plot_width=800, 
           x_range=(min(df['number']), max(df['number'])),
           y_range=(min(df['收盤價']), max(df['收盤價'])))
    p.add_tools(hover_tool)
    p.circle(x="number", y="leave", source=data,size=15,
          color={"field": "decide","transform": c_map},legend="decide")
    p.line(x="number", y="leave",source=data,color="black")
    p.xaxis.axis_label = "109年3月日期"
    p.yaxis.axis_label = "109年3月收盤價"
    return p
  
  
def search_stocks(kk):
    global driver   
    search=driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "stock-code-autocomplete", " " ))]')
    enter=driver.find_elements_by_xpath('//*[@id="main-form"]/div/div/form/a[2]')
    search[0].send_keys(kk)
    enter[0].send_keys(Keys.ENTER)
    time.sleep(5)
    soup=BeautifulSoup(driver.page_source,"lxml")
    table=soup.select_one("#report-table")
    df=pd.read_html(str(table))
    df[0].to_csv(kk+".csv",encoding='utf-8-sig')
    search[0].clear()
    
if __name__ == "__main__":
    start_driver()
    get_page(URL)
    keys=["0056","0050","2884","2891"]
    pictures=[]
    for key in keys:
        search_stocks(key)
    output_file("total.html")
    for i in range(4):
        temp=visualize(keys[i])
        tab = Panel(child=column(temp),title=keys[i])
        pictures.append(tab)
    tabs = Tabs(tabs=[pictures[0],pictures[1],pictures[2],pictures[3]])
    show(tabs)
    close_driver()
    
   
    
        
    
    
    
    
    
    
    
    
    
    
