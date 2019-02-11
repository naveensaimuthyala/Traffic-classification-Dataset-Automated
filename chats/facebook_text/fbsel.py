
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()   
driver.get("https://www.facebook.com/")  ##Tells the driver to go to facebook.com
driver.find_element_by_css_selector("#email").send_keys("muthyalanaveensai")
driver.find_element_by_css_selector("#pass").send_keys("6139819267")


login_box = driver.find_element_by_id('loginbutton') 
login_box.click() 

driver.get("https://www.facebook.com/messages/t/2037591349694082")  ##facebook link of your friend



msg = driver.find_element_by_xpath('//div[@role="combobox"]')
x=['a','b','c','d','d','e','f','g','h','i','j','k','l','m','n']
for i in x:
	
	msg.send_keys(i) #message to be sent
	msg.send_keys(Keys.ENTER)
	time.sleep(3)

