from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
browser = webdriver.Firefox()

browser.get('https://login.yahoo.com')
emailElem = browser.find_element_by_id('login-username')
emailElem.send_keys('muthyalanaveensai@yahoo.com')
emailElem.submit()


passwordElem = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.ID, "login-passwd"))
)
passwordElem.send_keys('naveen.95')
submitBtn=browser.find_element_by_id("login-signin")
submitBtn.click()


mailElem = browser.find_element_by_id('uh-mail-link')
mailElem.click()
#time.sleep(10)
composeElem = browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/div/div[1]/nav/div/div[1]/a')
composeElem.click()

toelem=browser.find_element_by_id('message-to-field')
toelem.send_keys("nmuth032@uottawa.ca")


subelem=browser.find_element_by_xpath("//div[@class='p_R']//input[contains(@data-test-id,'compose-subject')]")
#subelem=browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div[1]/div[3]/div/div/input")
subelem.send_keys("Test_mail")


bdyelem=browser.find_element_by_xpath("//div[@id='editor-container']//div[contains(@role,'textbox')]")

#bdyelem=browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/div/div[1]")
bdyelem.send_keys("Test_mail")


atchelem= browser.find_element_by_xpath("//input[contains(@title,'Attach files')]")

#atchelem= browser.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/span[1]/div/input")
atchelem.send_keys('~/Desktop/SolanaData/Milestone2/ymail_solana/itunes.py')

sendElem = browser.find_element_by_class_name('q_Z2aVTcY')
sendElem.click()




