import subprocess
import time
import sys
import pandas as pd
import random
from random import shuffle
#https://support.mozilla.org/en-US/questions/1182594

df=pd.read_csv("list_spotify.csv")
duration_list = df.duration.tolist()
#print(duration_list)
url_list=df.url.tolist()
#print(url_list)

          


if __name__ == "__main__":
	Start_Time_Experiment = time.time() 

	waiting_list=[]
	for i in range(len(duration_list)):
		wait_time=round(duration_list[i],2)
		
		#wait_time=round(random.choice(duration_list),2)
		#print('wait_time is see here',wait_time)
		waiting_list.append(wait_time)

	print (len(waiting_list))
	print(waiting_list)
	f_out=open("report_%s.csv"%time.strftime('%Y-%m-%d-%H', time.localtime(time.time())),'w')
	f_out.write(",".join(['start','end','wait','url','browser\n']))

	for sleep in waiting_list:
		print('sleep in loop :',sleep)
		#shuffle(url_list)
		#print ("Url list shuffled : ",url_list)
		for url in url_list:  
			to_run = ['firefox' ,'-new-tab', url]
			s=time.time()
			proc = subprocess.Popen(to_run)
			print ("Access url %s and wait %s seconds" % (url,sleep))
			time.sleep(sleep)
			proc = subprocess.Popen(['wmctrl','-c' ,'Mozilla Firefox'])
			f_out.write(",".join([str(s),str(time.time()),str(sleep),url,'firefox\n']))
			time.sleep(15)
			proc = subprocess.Popen(["killall" ,"firefox"])
			proc = subprocess.Popen(["bash","reset_firefox_setting.sh"])
			End_Time_Experiment = time.time()
			if End_Time_Experiment - Start_Time_Experiment > 25000:
				print ("Start : ", Start_Time_Experiment)
				print ("End : ", End_Time_Experiment)
				print ("AVG wait time in this run ", sum(waiting_list)/len(waiting_list))
				exit(0)

	f_out.close()

