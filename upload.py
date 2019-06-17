

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
			createDriveFolder(folderName, RECURSIVE_TEST_FOLDER_ID)
			parentFolderId = RECURSIVE_TEST_FOLDER_ID
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