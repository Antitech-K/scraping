from importlib.resources import contents
from multiprocessing import Value
import csv
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import codecs
import time


opt=Options()
opt.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")
opt.add_argument("--disable-blink-features=AutomationControlled")

"""
driver = webdriver.Chrome("chromedriver", chrome_options=opt)
driver.get("https://aliexpress.ru/wholesale?SearchText=%D0%9A%D1%83%D1%80%D1%82%D0%BA%D0%B0+%D0%BC%D1%83%D0%B6%D1%81%D0%BA%D0%B0%D1%8F&maxPrice=1000") 

time.sleep(2)
n = 1
for i in range(200):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print('scroling=', n)
    n +=1
    time.sleep(1)

file_object = codecs.open("ali_test.html", "w", "utf-8")
html = driver.page_source
file_object.write(html)
file_object.close()
"""
file_r=codecs.open('ali_test.html', "r", "utf-8")
hnya= file_r.read()
file_r.close()
soup=BS(hnya, "html")
all_product_href = soup.find_all('a', href=True)
url_general="https://aliexpress.ru"
url_item = []


for item in all_product_href:
    if item.get("href").find("item") != -1:
        item_href=url_general + item.get("href")
        url_item.append(item_href)

resault =[]
for u in url_item:
    driver = webdriver.Chrome("chromedriver", chrome_options=opt)
    driver.get(u)
    time.sleep(0.8)
    try:
        button_capcha1= driver.find_element(By.ID, "nc_1_n1z")
        ActionChains(driver).click_and_hold (on_element = button_capcha1).perform()
        time.sleep(0.5)
        ActionChains(driver).move_to_element_with_offset (button_capcha1, 258, 5).perform()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "baxia-dialog-close").click()
    except:
        None
    html_items = driver.page_source
    borsch= BS(html_items, "html")
    price = borsch.find(class_='snow-price_SnowPrice__mainS__ugww0l')
    develiry =borsch.find_all(class_= "snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography__sizeTextM__1shggo")
    number_buy = borsch.find(class_="snow-ali-kit_Typography__base__1shggo snow-ali-kit_Typography__base__1shggo SnowProductDescription_ExtraInfo__text__193uk")
    review = borsch.find(class_="snow-ali-kit_Typography__link__1shggo snow-ali-kit_Typography-Primary__link__1xop0e snow-ali-kit_Typography__underline__1shggo SnowProductDescription_ExtraInfo__text__193uk")
    resault.append(u)
    try:
        resault.append(price.text)
        resault.append (number_buy.text)
        resault.append (review.text)
        for find_text in develiry[:4]:
            resault.append (find_text.text)
    except:
        None
    time.sleep(1)
    print(resault)
    file= open('resault.csv', 'a')
    write=csv.writer(file, dialect='excel')
    write.writerow(resault)
    file.close()
    resault.clear()
