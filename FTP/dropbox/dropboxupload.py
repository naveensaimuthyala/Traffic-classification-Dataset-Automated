import dropbox
import os
import subprocess
dbx = dropbox.Dropbox('QFVQ-RFAREAAAAAAAAAALpdFyWgFa8RsOrp4ZQ5KkUk-YV8Dk9juOngKtRyn7ZD7')
dbx.users_get_current_account()
files = [f for f in os.listdir(os.path.join('inputs/')) if os.path.isfile(os.path.join('inputs/', f))]
print(files)
for x in files:   

    with open('inputs/'+x, "rb") as f:
	file_size = os.path.getsize('inputs/'+x)
	print(file_size)
        print(f)
	CHUNK_SIZE = 4 * 1024 * 1024
		
	p = subprocess.Popen(['sudo','tcpdump', '-i', 'enp0s3', '-vvv' , '-s 250',
                 '-w', x+'_db.pcap'], stdout=subprocess.PIPE)



	if file_size <= CHUNK_SIZE:

    		print(dbx.files_upload(f.read(),'/'+'inputs/'+x,mute=True))

	else:

    		upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
   		cursor = dropbox.files.UploadSessionCursor(session_id=upload_session_start_result.session_id,offset=f.tell())
   		commit = dropbox.files.CommitInfo(path='/'+'inputs/'+x)

    		while f.tell() < file_size:

       	 		if ((file_size - f.tell()) <= CHUNK_SIZE):
           			 print(dbx.files_upload_session_finish(f.read(CHUNK_SIZE),cursor,commit))
       			
			else:
				
        			dbx.files_upload_session_append(f.read(CHUNK_SIZE),cursor.session_id,
                                            cursor.offset)

            			cursor.offset = f.tell()
		
	print('uploaded','inputs/'+x)



        #dbx.files_upload(f.read(),'/'+'inputs/'+x,mute=True)
	cmd = "sudo killall  tcpdump"
	os.system(cmd)


	
    
