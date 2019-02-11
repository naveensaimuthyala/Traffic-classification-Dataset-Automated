

#file_id = '18lCUKdGqjQfZMdxR9X5xgRP27t5ReL9w'

 
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import io
from apiclient.http import MediaIoBaseDownload

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CREDENTIAL_DIR = './credentials'
CREDENTIAL_FILENAME = 'drive-python-quickstart.json'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Drive File Export Example'
SCOPES = 'https://www.googleapis.com/auth/drive.readonly'

FILE_ID = '18lCUKdGqjQfZMdxR9X5xgRP27t5ReL9w'
EXCEL = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
EXPORTED_FILE_NAME = 'exported_file.xlsx'

def get_credentials():
    credential_dir = CREDENTIAL_DIR
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, CREDENTIAL_FILENAME)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    request = service.files().export_media(fileId=FILE_ID, mimeType=EXCEL)
    fh = io.FileIO(EXPORTED_FILE_NAME, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print('Download %d%%.' % int(status.progress() * 100))


if __name__ == '__main__':
    main()   
