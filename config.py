from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os, io
from sys import platform

# Establish local directory to sync with Google Drive
if platform == 'win32':
	LOCAL_TARGET_DIR = 'E:\\School Work'
	SLASH = '\\'
elif platform == 'darwin':
	LOCAL_TARGET_DIR = '/Users/jd/Desktop/Google-Drive-Sync/test destination'
	SLASH = '/'

EXCEPT_SET = {'numbers', 'pages', 'key'}
# File ID of Google Drive folder to be synced
GOOGLE_DRIVE_FOLDER_ID = '1ytKCXTe82aLoIB-fS-PGx_3fVCA8wvf4'

# For testing
RECURSIVE_TEST_FOLDER_ID = '1_Yn8jD-J19paY3ja8DZh8n2KEcrcbin_'
DRIVE_TEST_DEST_FOLDER = '1UijN5aO_NoCIZEx7w3qxETdNv1gwfwy3'
SHARPENING_BUSINESS = '142nFxTXs3O507kBH9fSRG0aUrpXtnpay'

# Authorize access and setup the Drive v3 API
SCOPES = ['https://www.googleapis.com/auth/drive']

store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	creds = tools.run_flow(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))