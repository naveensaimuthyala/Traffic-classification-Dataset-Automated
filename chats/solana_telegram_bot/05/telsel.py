from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import subprocess
import time
import sys
import pandas as pd
import random
from random import shuffle

#driver = webdriver.Firefox()   
url="https://web.telegram.org/#/im?p=@solananetworks_bot"
#driver.get("https://web.telegram.org/#/im?p=@solananetworks_bot")
to_run = ['firefox' ,'-new-tab', url]
s=time.time()
proc = subprocess.Popen(to_run)
time.sleep(100)
proc = subprocess.Popen(['wmctrl','-c' ,'Mozilla Firefox'])
f_out.write(",".join([str(s),str(time.time()),str(sleep),url,'firefox\n']))
time.sleep(15)
proc = subprocess.Popen(["killall" ,"firefox"])
proc = subprocess.Popen(["bash","reset_firefox_setting.sh"])

