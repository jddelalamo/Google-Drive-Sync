# Not sure these functions are needed now



def createFileStructure(file_id, fileList=[], folderList=[], filePath=LOCAL_TARGET_DIR):
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
			createFileStructure(item['id'], fileList, folderList, newPath)

	return fileList, folderList

# Figure out how time is formatted
def getFileModDate(file_id):
	metadata = DRIVE.files().get(fileId=file_id, fields='modifiedTime').execute()
	return metadata['modifiedTime']

def getFileParent(file_id):
	metadata = DRIVE.files().get(fileId=file_id, fields='parents').execute()
	return metadata['parents']

def getFileName(file_id):
	metadata = DRIVE.files().get(fileId=file_id, fields='name').execute()
	return metadata['name']

def getChanges():
	# response = DRIVE.changes().getStartPageToken().execute()
	# print('Start token: %s' % response.get('startPageToken'))


	# Begin with our last saved start token for this user or the
	# current token from getStartPageToken()
	page_token = 454816
	while page_token is not None:
		response = DRIVE.changes().list(pageToken=page_token, spaces='drive').execute()
		print(response)
		for change in response.get('changes'):
			print('Change found for file: {}'.format(change.get('fileId')))
		if 'newStartPageToken' in response:
			saved_start_page_token = response.get('newStartPageToken')
		page_token = response.get('nextPageToken')

def getParametersToCreateDFObject(parent_id, targetPath):
	results = searchChildrenByParent(parent_id)
	for i in results:
		if i['name'] == targetPath[targetPath.rfind(SLASH)+1:]:
			return i['id'], i['name'], i['parents'][0], i['modifiedTime'], i['mimeType'], targetPath

def getLocalModDate(filePath):
	dirtyTime = time.localtime(os.path.getmtime(filePath))
	year = dirtyTime[0]
	month = dirtyTime[1]
	day = dirtyTime[2]
	hour = dirtyTime[3]
	minute = dirtyTime[4]
	second = dirtyTime[5]

	return (year, month, day, hour, minute, second)

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

def buildDriveFolders(file_id, folderList=[], filePath=LOCAL_TARGET_DIR):
	contents = searchChildrenByParent(file_id)
	# Can probably refactor this loop to handle .DS_Store files more elegantly
	for item in contents:
		print(item['mimeType'])
		newPath = filePath+SLASH+item['name']

		# Parent folder is returned as a list from API
		item['parents'] = item['parents'][0]

		if item['mimeType'][-6:] == 'folder':
			folderList.append(df.DriveFile(item['id'], item['name'], item['parents'],
										   item['modifiedTime'], item['mimeType'], newPath))
			buildDriveFolders(item['id'], folderList, newPath)

	return folderList


# Old upload folder processing ============================================================
filesToUpload = tuple(filesToUpload)
foldersToCreate = tuple(foldersToUpload)

# Checking if any folders to create are among the parent directory
# If they are, the path is popped out of foldersToCreate and the 
# DF Object is created and added to driveFolders
for path in foldersToCreate:
	parentPath = path[:path.rfind(SLASH)]
	tempName = path[path.rfind(SLASH)+1:]

	if parentPath == LOCAL_TARGET_DIR:
		foldersToCreate.remove(path)
		createDriveFolder(tempName, RECURSIVE_TEST_FOLDER_ID)

	results = searchChildrenByParent(RECURSIVE_TEST_FOLDER_ID)

	# Only way to search for it is by name--don't know any other attributes
	for i in results:
		if i['name'] == tempName:
			driveFolders.append(df.DriveFile(i['id'], i['name'], i['parents'][0],
								i['modifiedTime'], i['mimeType'], path))






for path in foldersToCreate:
	for folder in driveFolders:
	# Finds last occurence of slash and splits path at that point
	# to get the directory path one level above
		if path[:path.rfind(SLASH)] == folder.get_filePath():
			# String parsing to create folder name for uploading
			folderName = path[path.rfind(SLASH)+1:]
			createDriveFolder(folderName, folder.get_file_id())

			# Adds newly created Drive Folder to driveFolders list so new
			# folders created in new parent folders are also uploaded
			results = searchChildrenByParent(folder.get_file_id())
				# Only way to search for it is by name--don't know any other attributes
				for i in results:
					if i['name'] == folderName:
						driveFolders.append(df.DriveFile(i['id'], i['name'], i['parents'][0],
											i['modifiedTime'], i['mimeType'], path))

# ===============================================================================================







