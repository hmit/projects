from __future__ import print_function

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


import pickle
import os.path
import re
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    msgsApi = service.users().messages()
    def fetchAttachment(fname, emailId, attachId):
        b64bytes = msgsApi.attachments().get(userId='me', messageId=emailId, id=attachId).execute()['data']
        with open(fname, 'wb') as f:
            f.write(base64.urlsafe_b64decode(b64bytes))
        print(f'Stored pdf email attachment for {emailId} at {fname}')

    def getAttachments(emailId):
        email = msgsApi.get(userId='me', id=emailId, format='full').execute()
        acct4 = os.environ["ACCT4"]
        match = re.search(f'number xxxxxxx{acct4} on ([a-zA-Z]* 20[12][0-9]).*', email['snippet'])
        stmtDate = match.group(1) if match else 'Unknown'
        print(f'Processing email statement for {stmtDate}')
        for p in email['payload']['parts']:
            ctype = list(filter(lambda h: h['name'] == 'Content-Type', p['headers']))[0]['value']
            if 'application/pdf' not in ctype:
                continue
            match = re.search('name="([^"]*)"', ctype)
            fname = match.group(1) if match else stmtDate.replace(' ', '_')
            fetchAttachment(fname, emailId, p['body']['attachmentId'])

    msgs = msgsApi.list(userId='me', q='from:Global.E-Statement-IN@sc.com subject: estatement', maxResults=100).execute()
    for m in msgs['messages']:
        emailId = m['id']
        getAttachments(emailId)

if __name__ == '__main__':
    main()
