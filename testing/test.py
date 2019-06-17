import os
import pickle
from sys import platform
import time
import timeit
import itertools
import file_object
import mimeDict
from test_import import *




# aList = [1,2,3]
# bList = [4,5,6]

# a, b = tuple(aList), tuple(bList)

# print(type(b))
# print(a)
# print(b)



# print(os.path.isdir('/Users/jd/Documents/Sharpening Business/customer records.numbers'))

# path = '/Users/jd/Documents/Sharpening Business/hey/scam.pdf'
# fileExt = path[path.rfind('.'):]

# print(mimeDict.mimeDict[fileExt])


# pathList = ['a', 'a', 'b', 'c', 'b']
# path = pathList.pop(pathList.index('b'))

# print(path)
# print(pathList)


# a = [1,2,3]
# b = ['a','b','c','d','e']

# for i, j in itertools.zip_longest(a, b):
# 	if i != None:
# 		print(i, j)


# xy = [1,2,3]

# for x in []:
# 	print('hi')


# aSet = {1,2,3}
# bSet = {3,2}

# print(aSet.difference(bSet))


# myList = [1,2,3,4,5]
# for x in myList:
# 	print(x)
# 	if x == 3:
# 		myList.append(6)


# pathName = '/Users/jd/Desktop/Google-Drive-Sync/testing/recursive test/yo/class notes'
# # pathIndex = pathName.rfind('/')

# print(pathName[pathName.rfind('/')+1:])


# print(os.path.exists('/Users/jd/Desktop/Google-Drive-Sync/test destination'))


# slash = '\\'
# print('a'+slash+'c')


# epochTime = os.path.getmtime('/Users/jd/Desktop/Google-Drive-Sync/upload test media/test.txt')
# print(epochTime)
# # formatTime = time.strftime('%Y-%m-%d %H:%M:%S', epochTime)



# # Python Time Tuple format
# timeTuple = (2019, 5, 25, 11, 6, 30, 5, 145, -1)\

# print(time.localtime(epochTime))

# print(epochTime)

# lambda test
# g = lambda x: 3*x + 1


# num = '05'
# a = lambda x: x[0] == '0'
# print(a(num))



# print(time.time())


# Gets time offset
# print(time.altzone/3600)



# os.walk tutorial
# if platform == 'win32':
# 	TARGET_DIR = r'E:\School Work'
# elif platform == 'darwin':
# 	TARGET_DIR = '/Users/jd/Desktop/School Work'
# TARGET_DIR = '/Users/jd/Desktop/School Work'

# for i, (root, subdirs, files) in enumerate(os.walk('/Users/jd')):
# 	if '.cocoapods' in subdirs:
# 		subdirs.remove('.cocoapods')
# 	print('Pass', i)
# 	print('root:', root)
# 	print('subdirs:', subdirs)
# 	print('files:', files)
# 	print()



# testStr = 'application/vnd.google-apps.folder'
# newStr = testStr[-6:]








### Pickling--pickle can be overwritten with same method as creating it new

# testVar = "This is a second test"

# pickleOut = open('test.pickle', 'wb')
# pickle.dump(testVar, pickleOut)
# pickleOut.close()


# pickleIn = open('test.pickle', 'rb')
# testVar = pickle.load(pickleIn)
# pickleIn.close()

# print(testVar)
