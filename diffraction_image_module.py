#!/usr/bin/python2
import os
import re
import numpy as np

from scipy import fftpack, ndimage


#import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import subprocess
import sys
from cryio.cbfimage import CbfImage

import shutil
from scipy import fftpack


class ImageD:

	def __init__(self, newOrRead, *args): #### meworRead: -1 = new, 1 = read ### imgNum if using .cbf image type

############ 

# Format for reading (newOrRead = 1, filePath =  path to file being read, imgNum = number of image if using .cbf format image)

# Format for new ImageD (newOrRead = -1, numpy image array, imgType = image format, imagename, header)

#############
		if newOrRead == 1:

			self.filePath = args[0]
			self.imgName, self.imgType = os.path.splitext(self.filePath) # Find file extension
			imgSplit = self.imgName.split("/")
			self.imgName = imgSplit[len(imgSplit)-1]
			if self.imgType == ".img":
				self.header,self.headerSize, self.xN, self.yN = self.imgHeaderRead()  
				self.array = self.imgImageRead()
			elif self.imgType == ".cbf":
				self.imgNum = args[1]
				self.header = None
				self.cbfReader()
			else:
				print("Please provide image of .img")

		elif newOrRead == -1:

			self.imgType = args[1]
			print("h",args[3])
			self.headerSize = 0
			if self.imgType == '.img':
				self.header = args[3]
			else:
				if args[3]!=None:
					self.cryioImg=args[3]
			self.imgName = args[2]
			self.array = args[0]
			self.xN = args[0].shape[0]
			self.yN = args[0].shape[1]

		else:
			print("Provide -1 for new image 1 for image")
#########################################################################
			
	def typeCheck(self, checkType):
		if self.imgType != checkType:
			print("Requires image type "+ str(checkType)+ " used:" +str(self.imgType))
			os.exit()

################# Image Callable Attributes ##########################

	def getArray(self):
		return self.array

################# .img Related Functions ###########################

	def imgHeaderRead(self):
		self.typeCheck(".img")
		nx = 0
		ny = 0
		headerSize = 0

		file = open(self.filePath, 'rb')
		header = file.read()[:256]
		decode = header
		header_split = decode.decode().split('\n')
		for line in header_split:
			lineSplit = re.split(r'[=, ,\r,      ]',line)

			lineSplit = list(filter(None,lineSplit))
			print(lineSplit)
			#lineSplit = (filter(None,re.decode().split('	|=| ',line))) #split acording to spaces and equal symbol then filter blank entries
			if "NHEADER" in lineSplit: #If "NHEADER" is in line look for next componant in list for value
				headerSize = lineSplit[lineSplit.index("NHEADER")+1] 
			if "NY" in lineSplit:
				ny= lineSplit[lineSplit.index("NY")+1]
			if "NX" in lineSplit:
				nx = lineSplit[lineSplit.index("NX")+1]

		return header,int(headerSize),int(nx),int(ny)

	def imgImageRead(self):
		self.typeCheck(".img")

		dtype = np.dtype(np.int32) # big-endian unsigned integer (16bit)

		file = open(self.filePath, 'rb')
		shape = (self.yN,self.xN)
		headFile = file.read()
		self.header = headFile[:int(self.headerSize)]
		file.seek(0)
		file.seek(int(self.headerSize))
		data = np.fromfile(file, dtype)
		print(self.headerSize)
		#data.reshape(shape)

		return data.reshape(shape)

	def newImgImage(self,path):
		file = open(path+str(self.imgType),'wb')
		if self.header != None:
			file.write(self.header)
		else:
			header = "OD SAPPHIRE  4.0\n"+"COMPRESSION= NO\n"+"NX= "+str(self.xN)+" NY= "+str(self.yN)+" OI=      0 OL=      0\n"+"NHEADER=   "+str(256)+" NG=    512 NS=    768 NK=   1024 NS=    512 NH=   2048"+"NSUPPLEMENT=      0\n"+"TIME=Tue Mar 06 12:40:56 2018 "

			size = sys.getsizeof(header)
			if size <256:
				header = header + os.urandom(256-size)
			elif size > 256:
				header = header[0:256]

			file.write(header)
		np.array(self.array.ravel(), dtype=np.int32).tofile(file)

############## .cbf Related Functions ########################################################

	def cbfReader(self):
		self.typeCheck(".cbf")
		self.cryioImg = CbfImage(self.filePath)
		self.array = self.cryioImg.array
		self.xN = self.cryioImg.binary_header_dict['X-Binary-Size-Second-Dimension']
		self.yN = self.cryioImg.binary_header_dict['X-Binary-Size-Fastest-Dimension']
		
	def cbfGetImage(self):
		self.typeCheck(".cbf")
		series = dectris.albula.DImageSeries()
		series.open(self.filePath)
		img = series[self.imgNum]
		return img

	def showImage(self):
		self.typeCheck(".cbf")
		m = dectris.albula.openMainFrame()
		s = m.openSubFrame()
		s.loadImage(self.cbfReader())

	def array2CbfImage(self, numpyArray):
		self.typeCheck(".cbf")
		return dectris.albula.DImage(numpyArray,dataType = None)

	def newCbfImage(self,path):
		self.typeCheck(".cbf")
		self.cryioImg.array = self.array
		self.cryioImg.save_cbf(path+".cbf")


############# Image Manipulation ####################################

	def saveImage(self,path):
		if self.imgType == ".cbf":
			self.newCbfImage(path)
		if self.imgType == ".img":
			self.newImgImage(path)

	def divideImage(self,divider):
		self.array = np.true_divide(self.array,divider)

	def cutImage(self,cutValMin,cutValMax):
		np.clip(self.array,cutValMin,cutValMax,out= self.array)

	def showImage(self,clim=300):
		import matplotlib.pyplot as plt
		if clim!=None:
			plt.imshow(self.array,clim=(0,clim))
		else:
			plt.imshow(self.array)

		plt.show()

	def sumArea(self,x1,y1,x2,y2):
		return np.sum(self.array[y1:y2,x1:x2])

	def subtractImage(self,image):
		self.array = self.array - image.array

	def medianFilter(self,filterSize):
		self.array = ndimage.median_filter(self.array,filterSize)

def cutImage(img, lineV):
	rect = dectris.albula.DRect(lineV[0],lineV[1],lineV[2]-lineV[0],lineV[3]-lineV[1])
	return img.extract(rect)

############ File Managments ########################################

def clearFolder(path):
	if not os.path.exists(path): #check if background directory exists if not create it
	    os.makedirs(path)
	else: 
		shutil.rmtree(path) #Clear Background file and dir
		os.makedirs(path)

def readDatFile(filePath):
	file = open(filePath,"r")
	file = file.read()
	lines = file.split("\n")
	data = []
	for line in lines:
		item = []
		if(line==""):
			break
		item.append(line.split()[0])
		item.append(line.split()[1])
		data.append(item)
	return data


############# Data Extraction ###################################################

def removeDuplicatesArray2Numpy(IntData):
	numpyInt = np.array(IntData)
	numpInt = np.vstack({tuple(row) for row in numpyInt})
	b = np.ascontiguousarray(numpyInt).view(np.dtype((np.void, numpyInt.dtype.itemsize * numpyInt.shape[1])))
	_, idx = np.unique(b, return_index=True)
	return numpyInt[idx]


def boxSumIntensity(line_m, line_c, line_perp_m, width, x, y,img,dataOrImage):

	#Calc line equation for line perpendicular to line specified originating from x and y
	line_perp_c = y - (line_perp_m*x)
	#y = mx +c -> y = line_perp_m *x + line_perp_c
	x1 = int((x))
	y1 = y
	x2 = int((x1-(np.cos(np.arctan(line_perp_m))*width))) # calculate x2 from angle of perpendicular line to the x -axis arctan(gradient) the cos(angle)*width of box 
	scale = 1 #split pixels 
	IntData = []
	if width>0: #if width is zero then only calculate intensity of pixels crossing lines otherwise calculate box with width 
		count = 0
		for xVal in range(x2*scale,x1*scale): #loop between x2 and x1 pixels calculating Intensity of pixesl that cross the line perpendicular to the line specified and passing through the point x1,y1
			count+=1
			item = []
			x_p = int(xVal/scale) #round scaled x value, x = 1234 scaled becomes 12340 so that the loop can go through 12341, 12342...
			y_p = int(((line_perp_m*(xVal/scale))+line_perp_c)) #calculate y value acording to perpendicular line and xVal 
			item.append(x_p)
			item.append(y_p)
			item.append(img.pixel(x_p,y_p))
			IntData.append(item)
	else:
		item = []
		x_p = int(round(float(x1*scale)/scale))
		y_p = int(round(((line_perp_m*x1*scale)+line_perp_c*scale)/scale))
		item.append(x_p)
		item.append(y_p)
		item.append(img.pixel(x_p,y_p))
		IntData.append(item)

	if(dataOrImage==0):
		numpyInt = removeDuplicatesArray2Numpy(IntData)
	else:
		numpyInt = np.array(IntData)
	Intesity = 0
	intSize = 0
	out = []
	item=[]
	for line in numpyInt:
		Intesity+= line[2]
		item.append(line[2])
		intSize+=1
	if dataOrImage ==0:
		return Intesity/intSize
	else:
		return item


def lineVector(x1,y1,x2,y2,pixel_scaler,width):
	x1 = x1 *pixel_scaler
	y1 = y1 *pixel_scaler
	x2 = x2 *pixel_scaler
	y2 = y2 *pixel_scaler
	line_m = float(float(y2-y1)/float(x2-x1)) #gradient of line defined by x1,y1,x2,y2
	line_perp_m = float(-1/(line_m)) #gradient of line perpendicular to line defined by x1,y1,x2,y2
	line_c = (y2)-(line_m*x2) # intercept of line x1,y1,x2,y2 of form y = mx+c
	return (x1,y1,x2,y2,line_m,line_perp_m,line_c,width) # x1 = 0, y1 = 1, x2 = 2, y2 = 3, m = 4, m_perp = 5, c = 6, width = 7

def sumLengthRange(data, range1, range2):
	summ= 0
	for x in range(len(data)):
		if range1 <= float(data[x][0]) <= range2:
			summ = summ + float(data[x][1])
	return summ


class SeriesD:

##################################################


# Expects Image names to have general format of someimagename_runNumber_imageNumber.ext
# if runNum is 1 then assume run name is not specifed in image name
# args 0 = filepath, 1 = filename, 2 = fileExt 

##################################################

	def __init__(self,newOrRead,filePath, fileName):
		if newOrRead == 1:
			self.filePath = filePath
			self.fileName = fileName
			self.fileExt = self.findFileExt()
			self.seriesNames = self.findAllDirImages()
			self.seriesImages = self.generateImageSeries()
			self.numImages = self.numImages()

		elif newOrRead == -1:
			self.filePath = filePath
			self.fileName = fileName
			self.fileExt = fileExt
			self.seriesNames = []
			self.seriesImages = []
			self.numImages = 0

	def findFileExt(self):
		for file in os.listdir(self.filePath):
			if file.startswith(self.fileName):
				fileName,fileExt = os.path.splitext(file) # Find file extension
				return fileExt

	def cutFilePath(self, filePath):
		cutIndex = 0
		for i in range(len(filePath)-1, 0 , -1):
			if filePath[i] == "/":
				return filePath[0:i+1], filePath[i+1:]

	def sumBox(self,x1,y1,x2,y2,imageMin=None,imageMax=None):

		if imageMin == None:
			imageMin = 0
		if imageMax == None:
			imageMax = self.numImages 

		int_ = []
		for i in range(imageMin,imageMax):
			int_.append(self.seriesImages[i].sumArea(x1,y1,x2,y2))
		return np.array(int_)

	def findAllDirImages(self):
		fileList = []
		for file in os.listdir(self.filePath):
		    if file.startswith(self.fileName):
		    	if file.endswith(self.fileExt):
		        	fileList.append(os.path.join(self.filePath, file))

		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
		return sorted(fileList,key=alphanum_key )

	def generateImageSeries(self):
		imageSeries = []
		for i in range(len(self.seriesNames)):
			imageSeries.append(ImageD(1,self.seriesNames[i],i)) 
		return imageSeries

	def appendImageD(self,fileName,Image):
		self.seriesNames.append(fileName)
		self.seriesImages.append(Image)
		self.numImages = self.numImages+1

	def openImageSeries(self):
		return self.seriesImages

	def numImages(self):
		return len(self.seriesNames)

	def combineSeriesArray(self, range1,range2):
		image_array_combined = self.seriesImages[range1].array
		for i in range(range1+1,range2):
			image_array_combined += self.seriesImages[i].array
		return image_array_combined

	def cutSeries(self,range1,range2,cutValMin,cutValMax):
		for i in range(range1,range2):
			self.seriesImages[i].cutImage(cutValMin,cutValMax)

	def saveImageSeries(self,filePath):
		if self.filePath == filePath:
			a = input("About to overide original Images, do you wish to continue Y/N")
			if a == "N":
				sys.exit()

		for image in self.seriesImages:
			image.saveImage(filePath+image.imgName)

	def subtractImageFromSeries(self, range1,range2, image):
		for i in range(range1,range2):
			self.seriesImages[i].subtractImage(image)
	
	def medianFilterSeries(self, range1,range2, filterSize):
		for i in range(range1,range2):
			self.seriesImages[i].medianFilter(filterSize)

# Format for new ImageD (newOrRead = -1, numpy image array, imgType = image format, imagename)


class ToolsD:

	def subtractImage(self,image1,image2):

		subtracted = ImageD(-1,image1.array - image2.array,image1.fileExt,'Filtered_'+image1.fileName,image1.header)
		return subtracted

	def clearMakeFolder(self,path):
		if not os.path.exists(path): #check if background directory exists if not create it
		    os.makedirs(path)
		else: 
			shutil.rmtree(path) #Clear Background file and dir
			os.makedirs(path)

	def backgroundSubtraction(self,lowCut,highCut,seriesD):
		print(seriesD.filePath+seriesD.fileName)

		cutD = SeriesD(1,seriesD.filePath,seriesD.fileName) 
		cutD.cutSeries(0,cutD.numImages, lowCut,highCut)
		cutD.medianFilterSeries(0,cutD.numImages,5)

		if cutD.fileExt =='.img':
			backImage = ImageD(-1,cutD.combineSeriesArray(0,cutD.numImages),cutD.fileExt,'background',cutD.seriesImages[0].header)
		elif cutD.fileExt =='.cbf':	
			backImage = ImageD(-1,cutD.combineSeriesArray(0,cutD.numImages),cutD.fileExt,'background',cutD.seriesImages[0].cryioImg)
		else:
			print("Image Not Read Properly, Image Type Read: ", cutD.fileExt)
		backImage.divideImage(cutD.numImages)
		backImage.saveImage(cutD.filePath+"background")
		seriesD.subtractImageFromSeries(0,seriesD.numImages,backImage)
		backgroundFilePath = seriesD.filePath+seriesD.fileName+"_Background_Filtered/"
		self.clearMakeFolder(backgroundFilePath)
		seriesD.saveImageSeries(backgroundFilePath)