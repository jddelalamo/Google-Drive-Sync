from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import pickle
import os.path

SCOPES = "https://www.googleapis.com/auth/drive"
CLIENT_SECRET = 'client_secret.json'

def main():

	store = file.Storage('storage.json')
	creds = store.get()


	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
		creds = tools.run_flow(flow, store)


	DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
'''
	files = DRIVE.files().list().execute().get('items,', [])

	for f in files:
		print(f['title'], f['mimeType'])
'''
main()