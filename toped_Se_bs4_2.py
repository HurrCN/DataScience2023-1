'''
PROJECT DATA SCRAPPING
# by Muhammad Hurricane
# Last updated Jan 7 2023
'''''
########## PRE PROCESSING ##########

# Command to erase the terminal prompt
import os
os.system('cls')
import time
# To do scrapping
from selenium import webdriver  # browser driver like Chrome, Edge etc.
from selenium.webdriver.support.ui import WebDriverWait     # to wait until the page is opened
from bs4 import BeautifulSoup   # to find class name
# To make dataframe with pandas and export it to Excel
import pandas as pd
# To ensure the page has been opened
from selenium.webdriver.support import expected_conditions as EC
# To get address by using class (use it for icons, not text)
from selenium.webdriver.common.by import By

########## Scrap Trial ##########
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path="/Users/HurrCN/Documents/GitHub/TokopediaDataScience2023/chromedriver", options=options)
driver.set_window_size(1200, 1000)

url = 'https://www.tokopedia.com/search?navsource=&ob=3&origin_filter=sort_price&pmin=3300000&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&st=product&q=acer%20swift'
driver.get(url)

data = []
maxPage = 10
# The first for loop is to count how many pages do we need
for i in range(1,maxPage):
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#zeus-root")))
    time.sleep(4)
    print(f'\nViewing Page {i} of {maxPage}')
    # Scroll the page vertically 250 px by every step, do it 16 times with 0.5 secs delay
    for j in range(15):
        driver.execute_script("window.scrollBy(0,250)")
        time.sleep(0.5)
    
    # Take every address or class from HTML file behind any web page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # find the class
    for item in soup.findAll('div', class_='css-974ipl'):
        productName = item.find('div', class_='prd_link-product-name css-svipq6').text
        productPrice = item.find('div', class_='prd_link-product-price css-1ksb19c').text
        shopName = item.find('span', class_='prd_link-shop-name css-1kdc32b flip').text
        shopLoc = item.find('span', class_='prd_link-shop-loc css-1kdc32b flip').text
        # Frame the data with column arrangement as mentioned
        data.append(
            (shopName, shopLoc, productName, productPrice)
        )
    for j in range(3):
        driver.execute_script("window.scrollBy(250,0)")
        time.sleep(0.5)
    if i < maxPage : 
        time.sleep(5)
        nextPage = driver.find_element(By.CSS_SELECTOR, 'button[aria-label^="Laman berikutnya"]')
        nextPage.click()
        time.sleep(3)
    if i >= maxPage :
        time.sleep(5)
        
time.sleep(3)
df = pd.DataFrame(data, columns=['Store', 'Location', 'Product', 'Price'])
print(df)

with pd.ExcelWriter(r'C:\Users\Muhammad Hurricane\Documents\Programming\DataAnalyst\Project1_TokopediaDataScience2023\result\tokpedscrap.xlsx') as writer:
    df.to_excel(writer, sheet_name = 'Data Utama', index=False)

df.to_csv(r'C:\Users\Muhammad Hurricane\Documents\Programming\DataAnalyst\Project1_TokopediaDataScience2023\result\tokpedscrap.csv')

print('Data has been saved.')

time.sleep(10)
driver.quit()
