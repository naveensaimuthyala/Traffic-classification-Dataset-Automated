from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

class auth:
    def __init__(self, SCOPE):
        self.SCOPE = SCOPE

    def get_credentials(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        cwd_dir = os.getcwd()
        credential_dir = os.path.join(cwd_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'python-gmail-api-tutorial.json')
                                       
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', self.SCOPE)
            creds = tools.run_flow(flow, store)
        return creds
