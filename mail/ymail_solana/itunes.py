from selenium import webdriver

browser = webdriver.Firefox()
browser.get('https://itunesconnect.apple.com/WebObjects/iTunesConnect.woa')

# Add this line
browser.switch_to.frame('authFrame')

login_form = browser.find_element_by_id('muthyalanaveensai@gmail.com')
