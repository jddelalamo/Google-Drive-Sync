from apiclient.http import MediaIoBaseDownload
from sys import argv
import os, io
import drivefile as df
import upload_process
import download_process
from config import *


def main():

	driveFiles, driveFolders = buildDriveFiles(DRIVE_TEST_DEST_FOLDER)
	localFiles, localFolders = localFileSearch(LOCAL_TARGET_DIR)

	if argv[1] == 'up':
		upload_process.start(driveFiles, driveFolders, localFiles, localFolders)
	elif argv[1] == 'down':
		download_process.start(driveFiles, driveFolders, localFiles, localFolders)



# Probably don't need this
def getFileInfo(file_id):
	results = DRIVE.files().get(fileId=file_id, fields='id, name, modifiedTime, mimeType, parents').execute()

	return results


def getFileParentId(file_id):
	results = DRIVE.files().get(fileId=file_id, fields='parents').execute()

	return results['parents'][0]


# test to see if i can avoid .DS_Store files from this function
def searchChildrenByParent(parent_id):
	results = DRIVE.files().list(
		q="'{}' in parents and trashed=false".format(parent_id),
		pageSize=1000, fields='nextPageToken, files(id, name, modifiedTime, mimeType, parents)').execute()
	items = results.get('files', [])

	return items


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
		if os.path.isdir(os.path.join(path, item)) and item[item.rfind('.')+1:] not in EXCEPT_SET:
			folderList.append(os.path.join(path, item))
			localFileSearch(os.path.join(path, item), fileList, folderList)
		elif not os.path.isdir(os.path.join(path, item)) and item != '.DS_Store':
			fileList.append(os.path.join(path, item))

	# Can maybe turn this into a tuple
	return fileList, folderList



if __name__ == '__main__':
	main()


