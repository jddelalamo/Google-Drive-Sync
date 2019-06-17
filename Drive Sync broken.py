# from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os, io
from sys import platform
import itertools
import drivefile as df
import mimeDict

# Establish local directory to sync with Google Drive
if platform == 'win32':
	LOCAL_TARGET_DIR = 'E:\\School Work'
	SLASH = '\\'
	EXC_SET = {}
elif platform == 'darwin':
	LOCAL_TARGET_DIR = '/Users/jd/Desktop/Google-Drive-Sync/testing/recursive test'#'/Users/jd/Documents/Sharpening Business'
	SLASH = '/'
	EXC_SET = {'numbers', 'pages', 'key'}

# File ID of Google Drive folder to be synced
GOOGLE_DRIVE_FOLDER_ID = '1ytKCXTe82aLoIB-fS-PGx_3fVCA8wvf4'

# For testing
RECURSIVE_TEST_FOLDER_ID = '1_Yn8jD-J19paY3ja8DZh8n2KEcrcbin_'
DRIVE_TEST_DEST_FOLDER = '1UijN5aO_NoCIZEx7w3qxETdNv1gwfwy3'
DUMP_HERE = '142nFxTXs3O507kBH9fSRG0aUrpXtnpay'

# Authorize access and setup the Drive v3 API
SCOPES = ['https://www.googleapis.com/auth/drive']

store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	creds = tools.run_flow(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))



def main():


	driveFiles, driveFolders = buildDriveFiles(DUMP_HERE)
	localFiles, localFolders = localFileSearch(LOCAL_TARGET_DIR)

	# Process for uploading

	# Extracts filepaths from DriveFile objects and creates a list
	driveFilePaths = []
	driveFolderPaths = []
	for file, folder in itertools.zip_longest(driveFiles, driveFolders):
		if file != None:
			driveFilePaths.append(file.get_filePath())
		if folder != None:
			driveFolderPaths.append(folder.get_filePath())
		
	driveFilePaths = tuple(driveFilePaths)
	driveFolderPaths = tuple(driveFolderPaths)



	# Compares local folders and Drive folders to determine which local
	# folders need to be created so that files can be uploaded into them

	# Uses a for loop and lists instead of sets because filepaths must be
	# kept in correct order
	filesToUpload = []
	foldersToCreate = []
	for file, folder in itertools.zip_longest(localFiles, localFolders):
		# Checking for None necessary because of zip_longest()
		if file not in driveFilePaths and file != None:
			filesToUpload.append(file)
		if folder not in driveFolderPaths and folder != None:
			foldersToCreate.append(folder)

	print(foldersToCreate)

	

	# Iterates over paths to create, creates drive folders, then
	# creates objects for those new folders in case another folder
	# needs to be created in it
	for path in foldersToCreate:
		parentPath = path[:path.rfind(SLASH)]
		folderName = path[path.rfind(SLASH)+1:]
		# If clause checks if any folders to create are among the parent
		# directory.  If they are, the path is removed and the drive folder
		# is created using the global for the google drive folder id
		if parentPath == LOCAL_TARGET_DIR:
			createDriveFolder(folderName, DUMP_HERE)
			parentFolderId = DUMP_HERE
		else:
			for folder in driveFolders:
				if parentPath == folder.get_filePath():
					parentFolderId = folder.get_file_id()
					createDriveFolder(folderName, parentFolderId)
					break
				

		results = searchChildrenByParent(parentFolderId)
		# Only way to search for it is by name--don't know any other attributes
		for i in results:
			if i['name'] == folderName:
				driveFolders.append(df.DriveFile(i['id'], i['name'], i['parents'][0],
									i['modifiedTime'], i['mimeType'], path))


		for file in filesToUpload:
			parentPath = path[:path.rfind(SLASH)]
			fileName = path[path.rfind(SLASH)+1:]





# Does not replace a file with the same path, 
# instead creates another file with same name--
# must handle that on application side
# Look into setting parent_id=None
def uploadFile(filename, filepath, mType, parent_id):
	fileMetadata = {'name': filename, 'parents':[parent_id]}
	media = MediaFileUpload(filepath,
							mimetype=mType)
	file = DRIVE.files().create(body=fileMetadata,
								media_body=media,
								fields='id').execute()


def createDriveFolder(name, parent_id=None):
	# This if statement allows creation of folder in main drive if
	# parent_id is not specified, because the API requires parent_id
	# to be sent in a list
	if parent_id != None:
		parent_id = [parent_id]
	file_metadata = {'name': name,
				 	'mimeType': 'application/vnd.google-apps.folder',
				 	'parents': parent_id}
	DRIVE.files().create(body=file_metadata, fields='id').execute()


# Probably don't need this
def getFileModDate(file_id):
	metadata = DRIVE.files().get(fileId=file_id, fields='modifiedTime').execute()

	return metadata['modifiedTime']


# Automatically replaces file in destination
def downloadFile(file_id, filepath):
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


# test to see if i can avoid .DS_Store files from this function
def searchChildrenByParent(parent_id):
	results = DRIVE.files().list(
		q="'{}' in parents and trashed=false".format(parent_id),
		pageSize=1000, fields='nextPageToken, files(id, name, modifiedTime, mimeType, parents)').execute()
	items = results.get('files', [])

	return items

def getFileParentId(file_id):
	results = DRIVE.files().get(fileId=file_id, fields='parents').execute()

	return results['parents'][0]

# Calls searchChildrenByParent on the file id passed in.
# Then recursively looks through Google Drive file structure
# and adds DriveFile objects to lists based on if the item is a file or folder
# Look into turning this into a generator
def buildDriveFiles(file_id, fileList=[], folderList=[], filePath=LOCAL_TARGET_DIR):
	contents = searchChildrenByParent(file_id)

	# Can probably refactor this loop to handle .DS_Store files more elegantly
	for item in contents:
		newPath = filePath+SLASH+item['name']

		# Parent folder is returned as a list from API
		item['parents'] = item['parents'][0]

		if item['mimeType'][-6:] != 'folder' and item['name'] != '.DS_Store':
			fileList.append(df.DriveFile(item['id'], item['name'], item['parents'],
										 item['modifiedTime'], item['mimeType'], newPath))
		elif item['name'] == '.DS_Store':
			pass
		else:
			folderList.append(df.DriveFile(item['id'], item['name'], item['parents'],
										   item['modifiedTime'], item['mimeType'], newPath))
			buildDriveFiles(item['id'], fileList, folderList, newPath)

	return fileList, folderList


def localFileSearch(path, fileList=[], folderList=[]):
	contents = os.listdir(path)

	# Main processing of file tree
	for item in contents:
	# 	if os.path.isdir(os.path.join(path, item)) and item[item.rfind('.')+1:] not in EXC_SET:
	# 		folderList.append(os.path.join(path, item))
	# 		localFileSearch(os.path.join(path, item), fileList, folderList)
	# 	elif not os.path.isdir(os.path.join(path, item)) and item != '.DS_Store':
	# 		fileList.append(os.path.join(path, item))


		if not os.path.isdir(os.path.join(path, item)) and item != '.DS_Store':
			fileList.append(os.path.join(path, item))
		elif item == '.DS_Store':
			pass
		else:
			folderList.append(os.path.join(path, item))
			localFileSearch(os.path.join(path, item), fileList, folderList)
	# Can maybe turn this into a tuple
	return fileList, folderList



if __name__ == '__main__':
	main()


