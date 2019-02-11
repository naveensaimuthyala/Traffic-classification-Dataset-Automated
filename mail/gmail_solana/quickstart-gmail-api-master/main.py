from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
import auth

def get_labels():
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

SCOPES = 'https://mail.google.com/'
authInst = auth.auth(SCOPES)
credentials = authInst.get_credentials()
service = build('gmail', 'v1', http=credentials.authorize(Http()))

import send_email
sendInst = send_email.send_email(service)
#message = sendInst.create_message_with_attachment('nmuthyala005@gmail.com', 'nmuthyala005@gmail.com', 'test gmail api', 'hi there!, test email', 'Capture.PNG')
message = sendInst.create_message('nmuthyala005@gmail.com', 'nmuthyala005@gmail.com', 'test gmail api', 'hi there!')
sendInst.send_message('me', message)
