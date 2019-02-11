from __future__ import print_function
import os

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import mimetypes
mimetypes.add_type('application/vnd.android.package-archive', '.pcap')

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v2', http=creds.authorize(Http()))
FILES = [f for f in os.listdir(os.path.join('inputs/')) if os.path.isfile(os.path.join('inputs/', f))]
print(FILES)
#FILES = (
    #('3.type conversions.mp4', True),
  #  ('hello.txt', True),
#)

for filename in FILES:
    metadata = {'title': filename}
    res = DRIVE.files().insert(convert=True, body=metadata,
            media_body=filename, fields='mimeType,exportLinks').execute()
    print(res)
    if res:
        print('Uploaded "%s" (%s)' % (filename, res['mimeType']))

if res:
    MIMETYPE = 'application/pdf'
    res, data = DRIVE._http.request(res['exportLinks'][MIMETYPE])
    if data:
        fn = '%s.pdf' % os.path.splitext(filename)[0]
        with open(fn, 'wb') as fh:
            fh.write(data)
        print('Downloaded "%s" (%s)' % (fn, MIMETYPE))

