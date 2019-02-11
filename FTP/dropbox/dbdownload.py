import dropbox
import os
import subprocess
access_token = 'QFVQ-RFAREAAAAAAAAAALpdFyWgFa8RsOrp4ZQ5KkUk-YV8Dk9juOngKtRyn7ZD7'
dbx = dropbox.Dropbox(access_token)
response = dbx.files_list_folder("/inputs")
print(list(response.entries))
for file in response.entries:
	
    print(file.name)
    x=file.name
    p = subprocess.Popen(['sudo','tcpdump', '-i', 'enp0s3', '-vvv' , '-s 350',
                 '-w', x+'_db.pcap'], stdout=subprocess.PIPE)

    with open('db'+x, "wb") as f:
	metadata, res = dbx.files_download(path="/inputs/"+x)
    	f.write(res.content)


    print('downloaded :',x)
    cmd = "sudo killall  tcpdump"
    os.system(cmd)

