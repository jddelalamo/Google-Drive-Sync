import time
import os


class DriveFile:

	def __init__(self, file_id, fileName, parent_id, RFCdateModified, mimeType, filePath):
		self.__file_id = file_id
		self.__fileName = fileName
		self.__parent_id = parent_id
		self.__RFCdateModified = RFCdateModified
		self.__mimeType = mimeType
		self.__filePath = filePath

	def get_file_id(self):
		return self.__file_id

	def get_fileName(self):
		return self.__fileName

	def get_parent_id(self):
		return self.__parent_id

	def get_RFCdateModified(self):
		return self.__RFCdateModified

	def get_mimeType(self):
		return self.__mimeType

	def get_filePath(self):
		return self.__filePath

	# Converts RFC time to tuple time so drive file last-modified dates
	# can be compared with local file last-modified dates
	def get_driveDateModified(self):
		start = self.__RFCdateModified.split('-')

		year = int(start[0])
		month = int(start[1])
		day = int(start[2].split('T')[0])

		rest = start[2].split('T')[1].split(':')
		
		hour = int(rest[0])
		minute = int(rest[1])
		second = int(rest[2][0:2])

		return (year, month, day, hour, minute, second)

	# Gets local last-modified date based on the constructed filepath
	# for purposes of comparison
	def get_localDateModified(self):
		dirtyTime = time.localtime(os.path.getmtime(self.get_filePath()))
		year = dirtyTime[0]
		month = dirtyTime[1]
		day = dirtyTime[2]
		hour = dirtyTime[3]
		minute = dirtyTime[4]
		second = dirtyTime[5]

		return (year, month, day, hour, minute, second)
