from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()   
driver.get("https://web.telegram.org/#/im?p=@solananetworks_bot")

time.sleep(30)

phone_number = driver.find_element_by_name("phone_number")
phone_number.send_keys("6139819267")

time.sleep(100)

msg = driver.find_element_by_xpath("//div[@contenteditable='true']")
x=['a','b','c','d','d','e','f','g','h','i','j','k','l','m','n']
for i in x:
	
	msg.send_keys(i) #message to be sent
	msg.send_keys(Keys.ENTER)
	time.sleep(5)

