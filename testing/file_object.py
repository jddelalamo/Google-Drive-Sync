class File:

	def __init__(self, file_id, fileName, parentFolder, dateModified, mimeType, filePath):
		self.__file_id = file_id
		self.__fileName = fileName
		self.__parentFolder = parentFolder
		self.__dateModified = dateModified
		self.__mimeType = mimeType
		self.__filePath = filePath

	def get_file_id(self):
		return self.__file_id

	def get_fileName(self):
		return self.__fileName

	def get_parentFolder(self):
		return self.__parentFolder

	def get_dateModified(self):
		return self.__dateModified

	def get_mimeType(self):
		return self.__mimeType

	def get_filePath(self):
		return self.__filePath
	