
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRET = 'client_secret.json'

def main():

	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				CLIENT_SECRET, SCOPES)
			creds = flow.run_local_server()
		#save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	# Call the Drive v3 API
	service = build('drive', 'v3', credentials=creds)

	results = service.files().list(
		pageSize=10, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])

	if not items:
		print('No files found.')
	else:
		print('Files:')
		for item in items:
			print(u'{0} ({1})'.format(item['name'], item['id']))
main()