from __future__ import print_function

import os.path
import base64
from email.message import EmailMessage
from mysite.settings import BASE_DIR

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_play_scraper import app

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.labels']
CVWEMAIL = 'codevwade@gmail.com'
LABELID = 'Label_7613322265140830793'
creds = None

def get_creds():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    global creds
    creds_fp = os.path.join(BASE_DIR, 'appstoreresults/credentials.json')
    token_fp = os.path.join(BASE_DIR, 'appstoreresults/token.json')
    print(token_fp)
    if os.path.exists(token_fp):
        creds = Credentials.from_authorized_user_file(token_fp, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print('No token')
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_fp, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_fp, 'w') as token:
            token.write(creds.to_json())

def create_notification(url):
    message = EmailMessage()

    package = url.split('id=')[1].split('&')[0]

    result = app(
        package,
        lang='en', # defaults to 'en'
        country='us' # defaults to 'us'
    )
    app_name = result['title']

    message.set_content(f"A user has generated a request to analyze \"{app_name}\". \n{url}")

    
    message['To'] = CVWEMAIL
    message['From'] = CVWEMAIL
    message['Subject'] = f"{app_name} - Request for Packet Analysis"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
        .decode()

    create_message = {
        'raw': encoded_message
    }
    return create_message

def gmail_send_message(create_message):
    """Create and send an email message
    Print the returned  message id
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()

    try:
        
        service = build('gmail', 'v1', credentials=creds)
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        # print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message

def gmail_add_label(message_id):
    service = build('gmail', 'v1', credentials=creds)
    label_body = {'addLabelIds': [LABELID]}
    service.users().messages().modify(userId='me', id=message_id, body=label_body ).execute()


def send_notification(url):
    try:
        get_creds()
    #     msg = create_notification(url)
    #     msg_id = gmail_send_message(msg)['id']
    #     if msg_id:
    #         print('Sent email notification successfully')
    #     else:
    #         print("Could not send email notification")

    except BaseException as e:
        print(f"{type(e).__name__}: Could not send email notification")
        print(e)
    
    # try:
    #     gmail_add_label(msg_id)
    #     return True
    
    # except BaseException as e:
    #     print('Could not add Label')
    #     return False

if __name__ == '__main__':
    url = 'https://play.google.com/store/apps/details?id=com.clue.android&hl=en_US&gl=US'
    send_notification(url)