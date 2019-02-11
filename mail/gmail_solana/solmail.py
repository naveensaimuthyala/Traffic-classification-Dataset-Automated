from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import httplib2
from email.mime.text import MIMEText

from oauth2client.file import Storage
from oauth2client import tools

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://mail.google.com/']
http = httplib2.Http()
def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    #results = service.users().labels().list(userId='me').execute()
   # labels = results.get('labels', [])

   # if not labels:
       # print('No labels found.')
    #else:
      #  print('Labels:')
        #for label in labels:
         #   print(label['name'])

    index=0
    limit=5
    # Call the Gmail API to fetch INBOX
    inbox_results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = inbox_results.get('messages', [])
    if not messages:
        print("No messages found.")
    else:
        print("Message snippets:")
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(msg['snippet'])
            index+=1
            if index == limit:
                break


#Build the Gmail service from discovery
    gmail_service = build('gmail', 'v1', http=http)
    
    message = MIMEText("Hello Ravi,\r\n\r\n It's amazing you can send email using scripts.\r\n\r\n ")
    message['to'] = "nmuthyala005@gmail.com" #replace to email Id
    message['from'] = "nmuthyala005@gmail.com" #replace from email Id
    message['subject'] = "Reporting cool stuff" #replace the subject
    body = {'raw': base64.b64encode(message.as_string())}

# send it
    try:

       	message = (gmail_service.users().messages().send(userId="me", body=body).execute())
     	print('Message Id: %s' % message['id'])
      	print(message)
    except Exception as error:
	print('An error occurred: %s' % error)



if __name__ == '__main__':
    main()
