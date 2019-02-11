from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
import requests
from apiclient import discovery
from socket import socket
import io
import os
import subprocess

SCOPES = ['https://www.googleapis.com/auth/drive']
files = [f for f in os.listdir(os.path.join('inputs/')) if os.path.isfile(os.path.join('inputs/', f))]
print(files)

def up():
    for filename in files:
	p = subprocess.Popen(['sudo','tcpdump', '-i', 'enp0s3', '-vvv' ,'-s 600',
                 '-w', filename.replace('.pcap','')+'_driveup_capture.pcap'], stdout=subprocess.PIPE)
    	store = file.Storage('tokenwrite.json')
    	creds = store.get()
    	drive_service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    
    	the_file_to_upload = 'inputs/'+filename
	print('uploading----  :',the_file_to_upload)
   	metadata = {'name': the_file_to_upload.replace('inputs/','')}
    # Note the chunksize restrictions given in
# https://developers.google.com/api-client-library/python/guide/media_upload
    	media = MediaFileUpload(the_file_to_upload,
                            chunksize= 1024 * 1024,
                            # Not sure whether or not this mimetypes is necessary:
                            #mimetype='text/plain',
                            resumable=True)
    	request = drive_service.files().create(body=metadata, media_body=media)
    	response = None
   	while response is None:
        	status, response = request.next_chunk()
        	if status:
           		print("Uploaded %d%%." % int(status.progress() * 100))
    	print("Upload of {} is complete.".format(the_file_to_upload))
	cmd = "sudo killall  tcpdump"
    	os.system(cmd)



def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('tokenwrite.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            #print(item['id'])
            
            print(u'{0} ({1})'.format(item['name'], item['id']))
            #up(item['name'],item['id'])
           




if __name__ == '__main__':
    main()
    up()
    
  
    
