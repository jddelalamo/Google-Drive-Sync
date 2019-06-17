from apiclient.http import MediaFileUpload
import os, io
from sys import platform
import itertools
import drivefile as df
import mimeDict
from config import *



def start(driveFiles, driveFolders, localFiles, localFolders):

	# Extracts filepaths from DriveFile objects and creates a list
	driveFilePaths = []
	driveFolderPaths = []
	for file, folder in itertools.zip_longest(driveFiles, driveFolders):
		if file != None:
			driveFilePaths.append(file.get_filePath())
		if folder != None:
			driveFolderPaths.append(folder.get_filePath())
		
	driveFilePaths, driveFolderPaths = tuple(driveFilePaths), tuple(driveFolderPaths)


	# Compares local folders and Drive folders to determine which local
	# folders need to be created so that files can be uploaded into them

	# Uses a for loop and lists instead of set comparisonbecause filepaths 
	# must be kept in correct order
	filesToUpload = []
	foldersToCreate = []
	for file, folder in itertools.zip_longest(localFiles, localFolders):
		# Checking for None necessary because of zip_longest()
		if file not in driveFilePaths and file != None:
			filesToUpload.append(file)
		if folder not in driveFolderPaths and folder != None:
			foldersToCreate.append(folder)

	
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
			parentFolderId = DRIVE_TEST_DEST_FOLDER
			print("creating folder {}".format(path))
			createDriveFolder(folderName, parentFolderId)
		else:
			for folder in driveFolders:
				if parentPath == folder.get_filePath():
					parentFolderId = folder.get_file_id()
					print("creating folder {}".format(path))
					createDriveFolder(folderName, parentFolderId)
					break
				

		results = searchChildrenByParent(parentFolderId)
		# Only way to search for it is by name--don't know any other attributes
		for i in results:
			if i['name'] == folderName:
				driveFolders.append(df.DriveFile(i['id'], i['name'], i['parents'][0],
									i['modifiedTime'], i['mimeType'], path))
	
	# Uploads files
	for path in filesToUpload:
		parentPath = path[:path.rfind(SLASH)]
		fileName = path[path.rfind(SLASH)+1:]
		try:
			fileExt = fileName[fileName.rfind('.'):]
		except KeyError as err:
			print("File extension probably missing from mimeDict.py.")
			print("Add it and try again.")
			print("Error message: {}".format(err))
		fileExt = fileExt.lower()

		if parentPath == LOCAL_TARGET_DIR:
			parentFolderId = DRIVE_TEST_DEST_FOLDER
			print("uploading file {}".format(path))
			try: 
				uploadFile(fileName, path, mimeDict.mimeDict[fileExt], parentFolderId)
			except Exception as err:
				print(err)
		else:
			for folder in driveFolders:
				if parentPath == folder.get_filePath():
					parentFolderId = folder.get_file_id()
					print("uploading file {}".format(path))
					try:
						uploadFile(fileName, path, mimeDict.mimeDict[fileExt], parentFolderId)
					except Exception as err:
						print(err)


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


# test to see if i can avoid .DS_Store files from this function
def searchChildrenByParent(parent_id):
	results = DRIVE.files().list(
		q="'{}' in parents and trashed=false".format(parent_id),
		pageSize=1000, fields='nextPageToken, files(id, name, modifiedTime, mimeType, parents)').execute()
	items = results.get('files', [])

	return items


