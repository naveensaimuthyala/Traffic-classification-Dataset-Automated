import base64
import httplib2
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client import tools

from email import encoders

#needed for attachment
import smtplib  
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'credentials.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
  credentials = tools.run_flow(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)



#-------------------------------------------------------------------------------------------------------------------------------------


# create a message to send
## Get creds, prepare message and send it
def create_message_and_send(sender, to, subject,  message_text_plain, message_text_html, attached_file):
    credentials = get_credentials()

    # Create an httplib2.Http object to handle our HTTP requests, and authorize it using credentials.authorize()
    http = httplib2.Http()

    # http is the authorized httplib2.Http() 
    http = credentials.authorize(http)        #or: http = credentials.authorize(httplib2.Http())

    service = discovery.build('gmail', 'v1', http=http)

    ## without attachment
    # message_without_attachment = create_message_without_attachment(sender, to, subject, message_text_html, message_text_plain)
    # send_Message_without_attachement(service, "me", message_without_attachment, message_text_plain)


    ## with attachment
    message_with_attachment = create_Message_with_attachment(sender, to, subject, message_text_plain, message_text_html, attached_file)
    send_Message_with_attachement(service, "me", message_with_attachment, message_text_plain,attached_file)

# def create_message_without_attachment (sender, to, subject, message_text_html, message_text_plain):
    # #Create message container
    # message = MIMEMultipart('alternative') # needed for both plain & HTML (the MIME type is multipart/alternative)
    # message['Subject'] = subject
    # message['From'] = sender
    # message['To'] = to

    # #Create the body of the message (a plain-text and an HTML version)
    # message.attach(MIMEText(message_text_plain, 'plain'))
    # message.attach(MIMEText(message_text_html, 'html'))

    # raw_message_no_attachment = base64.urlsafe_b64encode(message.as_bytes())
    # raw_message_no_attachment = raw_message_no_attachment.decode()
    # body  = {'raw': raw_message_no_attachment}
    # return body



def create_Message_with_attachment(sender, to, subject, message_text_plain, message_text_html, attached_file):
    """Create a message for an email.

    message_text: The text of the email message.
    attached_file: The path to the file to be attached.

    Returns:
    An object containing a base64url encoded email object.
    """

    ##An email is composed of 3 part :
        #part 1: create the message container using a dictionary { to, from, subject }
        #part 2: attach the message_text with .attach() (could be plain and/or html)
        #part 3(optional): an attachment added with .attach() 

    ## Part 1
    message = MIMEMultipart() #when alternative: no attach, but only plain_text
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    ## Part 2   (the message_text)
    # The order count: the first (html) will be use for email, the second will be attached (unless you comment it)
    message.attach(MIMEText(message_text_html, 'html'))
    message.attach(MIMEText(message_text_plain, 'plain'))

    ## Part 3 (attachement) 
    # # to attach a text file you containing "test" you would do:
    # # message.attach(MIMEText("test", 'plain'))

    #-----About MimeTypes:
    # It tells gmail which application it should use to read the attachement (it acts like an extension for windows).
    # If you dont provide it, you just wont be able to read the attachement (eg. a text) within gmail. You'll have to download it to read it (windows will know how to read it with it's extension). 

    #-----3.1 get MimeType of attachment
        #option 1: if you want to attach the same file just specify it’s mime types

        #option 2: if you want to attach any file use mimetypes.guess_type(attached_file) 

    my_mimetype, encoding = mimetypes.guess_type(attached_file)

    # If the extension is not recognized it will return: (None, None)
    # If it's an .mp3, it will return: (audio/mp3, None) (None is for the encoding)
    #for unrecognized extension it set my_mimetypes to  'application/octet-stream' (so it won't return None again). 
    if my_mimetype is None or encoding is not None:
        my_mimetype = 'application/octet-stream' 


    main_type, sub_type = my_mimetype.split('/', 1)# split only at the first '/'
    # if my_mimetype is audio/mp3: main_type=audio sub_type=mp3

    #-----3.2  creating the attachement
        #you don't really "attach" the file but you attach a variable that contains the "binary content" of the file you want to attach

        #option 1: use MIMEBase for all my_mimetype (cf below)  - this is the easiest one to understand
        #option 2: use the specific MIME (ex for .mp3 = MIMEAudio)   - it's a shorcut version of MIMEBase

    #this part is used to tell how the file should be read and stored (r, or rb, etc.)
    if main_type == 'text':
        print("text")
        temp = open(attached_file, 'r')  # 'rb' will send this error: 'bytes' object has no attribute 'encode'
        attachement = MIMEText(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'image':
        print("image")
        temp = open(attached_file, 'rb')
        attachement = MIMEImage(temp.read(), _subtype=sub_type)
        temp.close()

    elif main_type == 'audio':
        print("audio")
        temp = open(attached_file, 'rb')
        attachement = MIMEAudio(temp.read(), _subtype=sub_type)
        temp.close()            

    elif main_type == 'application' and sub_type == 'pdf':   
        temp = open(attached_file, 'rb')
        attachement = MIMEApplication(temp.read(), _subtype=sub_type)
        temp.close()

    else:                              
        attachement = MIMEBase(main_type, sub_type)
        temp = open(attached_file, 'rb')
        attachement.set_payload(temp.read())
        temp.close()

    #-----3.3 encode the attachment, add a header and attach it to the message
    encoders.encode_base64(attachement)  #https://docs.python.org/3/library/email-examples.html
    filename = os.path.basename(attached_file)
    attachement.add_header('Content-Disposition', 'attachment', filename=filename) # name preview in email
    message.attach(attachement) 


    ## Part 4 encode the message (the message should be in bytes)
    message_as_bytes = message.as_bytes() # the message should converted from string to bytes.
    message_as_base64 = base64.urlsafe_b64encode(message_as_bytes) #encode in base64 (printable letters coding)
    raw = message_as_base64.decode()  # need to JSON serializable (no idea what does it means)
    return {'raw': raw} 



# def send_Message_without_attachement(service, user_id, body, message_text_plain):
    # try:
        # message_sent = (service.users().messages().send(userId=user_id, body=body).execute())
        # message_id = message_sent['id']
        # # print(attached_file)
        # print (f'Message sent (without attachment) \n\n Message Id: {message_id}\n\n Message:\n\n {message_text_plain}')
        # # return body
    # except errors.HttpError as error:
        # print (f'An error occurred: {error}')




def send_Message_with_attachement(service, user_id, message_with_attachment, message_text_plain, attached_file):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """
    try:
        message_sent = (service.users().messages().send(userId=user_id, body=message_with_attachment).execute())
        message_id = message_sent['id']
        # print(attached_file)

        # return message_sent
    except errors.HttpError as error:
        print (f'An error occurred: {error}')


def main():
    to = "muthyalanaveensai@gmail.com"
    sender = "nmuthyala005@gmail.com"
    subject = "subject test1"
    message_text_html  = r'Hi<br/>Html <b>hello</b>'
    message_text_plain = "Hi\nPlain Email"
    attached_file = r'stck.py'
    create_message_and_send(sender, to, subject, message_text_plain)


if __name__ == '__main__':
    main()
