# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 11:09:17 2020

@author: 朱瑋民
"""
import time
import pandas as pd
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys#鍵盤的操作
from selenium.webdriver.common.action_chains import ActionChains#滑鼠的操作
# 目標URL網址
URL = "https://tw.hotels.com/"
# 搜尋條件
KEY = "台北巿台灣" 
CHECKIN = "2020-03-27" 
CHECKOUT = "2020-03-29"

driver = None

def start_driver():
    global driver
    print("啟動 WebDriver...")
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(7)

def close_driver():
    global driver
    driver.quit()
    print("關閉 WebDriver...")
    
def get_page(url):
    global driver
    print("取得網頁...")
    driver.get(url)
    time.sleep(2)

def search_hotels(searchKey, checkInDate, checkOutDate):
    global driver
    # 找出表單的HTML元素
    searchEle = driver.find_elements_by_xpath('//*[(@id = "qf-0q-destination")]')
    checkInEle = driver.find_elements_by_xpath('//*[(@id = "qf-0q-localised-check-in")]')
    checkOutEle = driver.find_elements_by_xpath('//*[(@id = "qf-0q-localised-check-out")]')
    search = driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cta-strong", " " ))]')
    close=driver.find_elements_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "widget-overlay-close", " " ))]')
    if searchEle and checkInEle and checkOutEle and search:#有找到這三個    
        actions = ActionChains(driver)     # 關閉彈出框  並指派action為使用的
      
        actions.perform()       
        searchEle[0].send_keys(searchKey)  # 輸入搜尋條件
        searchEle[0].send_keys(Keys.TAB)        
        checkInEle[0].clear()
        checkInEle[0].send_keys(checkInDate)
        checkOutEle[0].clear()
        checkOutEle[0].send_keys(checkOutDate)
        time.sleep(5)
        checkOutEle[0].send_keys(Keys.ENTER)  # 送出搜尋  送出搜尋一次就好  不然會出錯
       
        time.sleep(10)  
        menu = driver.find_elements_by_xpath('//*[@id="enhanced-sort"]/li[5]/a')
        if menu:
            actions = ActionChains(driver)    # 選排序選單
            actions.move_to_element(menu[0]) #移動至排序選單
            
            actions.perform()
            # 找出價格從低至商排序
            price=driver.find_elements_by_xpath('//*[@id="sort-submenu-price"]/li[2]/a')
            #不知道位置  按右鍵  檢查
            if price:
                price[0].click()
                time.sleep(10)
                return True  
    return False
                                
def grab_hotels():
    global driver                
    # 使用lxml剖析HTML文件
    for i in range(1,10):
        if(i<5):
            number=2300*i
        else:
            number=1800*i
        driver.execute_script('window.scrollTo(0,'+str(number)+');')
        time.sleep(6)
        driver.execute_script('window.scrollTo(0,0);')
        time.sleep(6)#讓網頁可以繼續往下跑
    
    tree = html.fromstring(driver.page_source)#要解析後才可以找xpath
    hotels = tree.xpath('//*[@id="listings"]/ol')#位置不對不能用
    found_hotels = []
    i=1 
    for i in range(60): 
        hotelName1=""
        price1=""
        rating1=""
        address1=""
        hotelName = tree.xpath('//*[@id="listings"]/ol/li['+str(i)+']/article/section/div/h3/a')
        price = tree.xpath('//*[@id="listings"]/ol/li['+str(i)+']/article/section/aside/div[1]/a/strong')
        if price:
            price1 = price[0].text_content().replace(",","").strip()
            item = [hotelName1, price1, rating1, address1]
        else:
            price = tree.xpath('//*[@id="listings"]/ol/li['+str(i)+']/article/section/aside/div[1]/a/ins')
            if price:
                price1 = price[0].text_content().replace(",","").strip()
                item = [hotelName1, price1, rating1, address1]
        rating =tree.xpath('//*[@id="listings"]/ol/li['+str(i)+']/article/section/div/div/div[1]/span')
        if rating:
            rating1 = rating[0].text_content()
            item = [hotelName1, price1, rating1, address1]
        address = tree.xpath('//*[@id="listings"]/ol/li['+str(i)+']/article/section/div/address/span')
        if address:
            address1 = address[0].text_content().split(",")
            item = [hotelName1, price1, rating1, address1]
        if hotelName:
            hotelName1 = hotelName[0].text_content()
            item = [hotelName1, price1, rating1, address1]
            found_hotels.append(item)
        i+=1
       
    
    return found_hotels    

def parse_hotels(url, searchKey, checkInDate, checkOutDate):
    start_driver()
    get_page(url)
    # 是否成功執行旅館搜尋
    if search_hotels(searchKey, checkInDate, checkOutDate): #如果return true   
        hotels = grab_hotels()
        close_driver()
        return hotels
    else:
        print("搜尋旅館錯誤...")
        return []

def save_to_csv(items, file):
    found_hotels = ["旅館名稱","價格","星級","地址"]
    test=pd.DataFrame(columns=found_hotels,data=items)
    test.to_html("hotels.html")#如果test.head()則只會有前五筆
    test.to_csv(file,encoding='utf-8-sig')
 
        
if __name__ == '__main__':    
    hotels = parse_hotels(URL, KEY, CHECKIN, CHECKOUT)
    print(hotels)
    for hotel in hotels:
        print(hotel)
    save_to_csv(hotels, "hotels.csv")


