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
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
#drive_service = discovery.build('drive', 'v3', http=http)

def down(x,y):
    p = subprocess.Popen(['sudo','tcpdump', '-i', 'enp0s3', '-vvv' ,'-s 600',
                 '-w', x.replace('.pcap','')+'_drivedown_capture.pcap'], stdout=subprocess.PIPE)
    store = file.Storage('tokenwrite.json')
    creds = store.get()
    drive_service = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    file_id = y
    request = drive_service.files().get_media(fileId=file_id)
    #fh = io.BytesIO()
    
    fh = io.FileIO(x, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
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
            down(item['name'],item['id'])



if __name__ == '__main__':
    main()
    
  
    

