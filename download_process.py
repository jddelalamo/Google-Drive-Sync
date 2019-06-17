from apiclient.http import MediaIoBaseDownload
import os
from config import *


def start(driveFiles, driveFolders, localFiles, localFolders):
	for folder in driveFolders:
		if folder.get_filePath() not in localFolders:
			print("Creating folder {}".format(folder.get_filePath()))
			os.makedirs(folder.get_filePath())

	for file in driveFiles:
		if file.get_filePath() not in localFiles:
			print("Downloading file {}".format(file.get_fileName()), end=': ')
			downloadFile(file.get_file_id(), file.get_filePath())



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