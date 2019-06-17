from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os, io


SCOPES = ['https://www.googleapis.com/auth/drive']
store = file.Storage('credentials.json')

def main():

	
	# Setup the Drive v3 API
	#store = file.Storage('credentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)

	DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

	'''
	# Upload a file
	fileMetadata = {'name': 'test'}
	media = MediaFileUpload('test.txt',
							mimetype='text/plain')
	file = DRIVE.files().create(body=fileMetadata,
								media_body=media,
								fields='id').execute()

	
	# Call the Drive v3 API
	results = DRIVE.files().list(
		pageSize=10, fields="nextPageToken, files(id, name)").execute()
	items = results.get('files', [])
	if not items:
		print("No files found.")
	else:
		print("Files:")
		for item in items:
			print('{0}, ({1})'.format(item['name'], item['id']))
	'''

	file_id = '1aEWrzxmM9U5ZrYHyDCl-cnefCOFcDX5i'
	filepath = 'test.txt'
	request = DRIVE.files().get_media(fileId=file_id)
	fh = io.BytesIO()
	downloader = MediaIoBaseDownload(fh, request)
	done = False
	while done is False:
		status, done = downloader.next_chunk()
		print("Download %d%%." % int(status.progress() * 100))
	with io.open(filepath, 'wb') as f:
		fh.seek(0)
		f.write(fh.read())

main()