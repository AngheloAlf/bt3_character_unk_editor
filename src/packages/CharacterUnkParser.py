import TransformClass
import FusionClass
import CharacterMenu
import Constants
import os

def obtenerDiferencias(linea1, linea2):
	i = 0
	wea = []
	largo = min(len(linea2), len(linea1))
	while i < largo:
		if linea1[i] != linea2[i]:
			dif1 = ""
			dif2 = ""
			o = i
			while linea1[i] != linea2[i]:
				dif1 += linea1[i]
				dif2 += linea2[i]
				i+=1
			wea.append([o, dif1, dif2])
		i+=1
	return wea

def getTransformData(archivo, pointerFile):
	line1 = archivo[pointerFile:pointerFile+16]
	pointerFile += 16
	line2 = archivo[pointerFile:pointerFile+14]
	pointerFile += 14
	return TransformClass.TransformClass(line1, line2), pointerFile

def getFusionData(archivo, pointerFile):
	line = archivo[pointerFile:pointerFile+24]
	pointerFile += 24
	return FusionClass.FusionClass(line), pointerFile

def getMenusData(archivo, lineaArchivo, pointerFile):
	charMenuObj = None
	menu = ""

	while lineaArchivo != "":
		puntero = map(lambda x: ord(x), lineaArchivo)
		menu += lineaArchivo[0:2]
		if puntero == Constants.Constants.endOfMenuFile:
			menu += lineaArchivo[2:4]
			charMenuObj = CharacterMenu.CharacterMenu(menu)
			break
		lineaArchivo = lineaArchivo[2:4]
		lineaArchivo += archivo[pointerFile:pointerFile+2]
		pointerFile += 2
	return charMenuObj, pointerFile

def setTransformData(archivo, pointerFile, transLines):
	archivo = archivo[:pointerFile] + transLines[0] + transLines[1] + archivo[pointerFile+30:]
	pointerFile += 16 + 14
	return archivo, pointerFile 

def setFusionData(archivo, pointerFile, fusionLine):
	archivo = archivo[:pointerFile] + fusionLine + archivo[pointerFile+24:]
	pointerFile += 24
	return archivo, pointerFile


class CharacterUnkParser:
	def __init__(self, name):
		# type: (str) -> None
		self.filename = name
		self.transObj = None
		self.menusList = None
		self.fullFile = ""
		self.fastMode = True
		self.fastModeStart = 3.0/5

	def parse(self, gui=None):
		archivo = open(self.filename, "rb")
		self.fullFile = archivo.read()
		archivo.close()

		#archivo = open(self.filename, "rb")
		fileSize = float(len(self.fullFile))

		startOfMenuFile = Constants.Constants.startOfMenuFile
		endOfMenuFile = Constants.Constants.endOfMenuFile
		transformCode = Constants.Constants.transformCode
		
		#indice = 0
		self.menusList = []
		menu = ""

		if gui:
			gui.restartProgressBar()

		pointerFile = 0
		if self.fastMode:
			pointerFile = int(fileSize*self.fastModeStart)
			while pointerFile % 4 != 0:
				pointerFile += 1
			if not gui is None:
				for i in range(int(20*self.fastModeStart)):
					gui.updateProgressBar()	

		porcentajeAnterior = -1

		transFound = False


		lineaArchivo = self.fullFile[pointerFile:4+pointerFile]
		pointerFile += 4

		while lineaArchivo != "" and len(lineaArchivo) == 4:
			puntero = map(lambda x: ord(x), lineaArchivo)

			if startOfMenuFile == puntero:
				lineaArchivo = lineaArchivo[2:4]
				lineaArchivo += self.fullFile[pointerFile:pointerFile+2]
				pointerFile += 2
				charMenuObj, pointerFile = getMenusData(self.fullFile, lineaArchivo, pointerFile)
				self.menusList.append(charMenuObj)
 
			if not transFound and puntero == transformCode:
				#print "encontrado"
				pointerFile += 16*7-8
				self.transObj, pointerFile = getTransformData(self.fullFile, pointerFile)
				self.fusionObj, pointerFile = getFusionData(self.fullFile, pointerFile)
				transFound = True

			lineaArchivo = lineaArchivo[2:4]
			lineaArchivo += self.fullFile[pointerFile:pointerFile+2]
			pointerFile += 2

			if int(pointerFile / fileSize * 20) > porcentajeAnterior:
				porcentajeAnterior = int(pointerFile / fileSize * 20)
				if not gui is None:
					gui.updateProgressBar()
				else:
					print 100 * pointerFile / fileSize

		pointerFile -= 2
		#archivo.close()

		#print pointerFile
		#print pointerFile, fileSize
		#print pointerFile == fileSize
		#print os.path.getsize(self.filename) == pointerFile
		return self

	def updateFileData(self, gui=None):
		fileSize = float(len(self.fullFile))

		startOfMenuFile = Constants.Constants.startOfMenuFile
		endOfMenuFile = Constants.Constants.endOfMenuFile
		transformCode = Constants.Constants.transformCode
		
		#indice = 0
		menu = ""

		#if not gui is None:
			#gui.restartProgressBar()

		pointerFile = 0
		if self.fastMode:
			pointerFile = int(fileSize*self.fastModeStart)
			while pointerFile % 4 != 0:
				pointerFile += 1
			if not gui is None:
				for i in range(int(10*self.fastModeStart)):
					gui.updateProgressBar()	

		porcentajeAnterior = -1

		transFound = False

		lineaArchivo = self.fullFile[pointerFile:4+pointerFile]
		pointerFile += 4

		while lineaArchivo != "" and len(lineaArchivo) == 4:
			puntero = map(lambda x: ord(x), lineaArchivo)

			if startOfMenuFile == puntero:
				lineaArchivo = lineaArchivo[2:4]
				lineaArchivo += self.fullFile[pointerFile:pointerFile+2]
				pointerFile += 2
				#TODO: Save menu modifications to file
				# charMenuObj, pointerFile = getMenusData(self.fullFile, lineaArchivo, pointerFile)
				# self.menusList.append(charMenuObj)
 
			if not transFound and puntero == transformCode:
				#print "encontrado"
				#self.transObj, pointerFile = getTransformData(self.fullFile, pointerFile)
				pointerFile += 16*7-8
				self.fullFile, pointerFile = setTransformData(self.fullFile, pointerFile, self.transObj.getAsLines())
				self.fullFile, pointerFile = setFusionData(self.fullFile, pointerFile, self.fusionObj.getAsLines())
				transFound = True

			lineaArchivo = lineaArchivo[2:4]
			lineaArchivo += self.fullFile[pointerFile:pointerFile+2]
			pointerFile += 2

			if int(pointerFile / fileSize * 10) > porcentajeAnterior:
				porcentajeAnterior = int(pointerFile / fileSize * 10)
				if not gui is None:
					gui.updateProgressBar()
				else:
					print 100 * pointerFile / fileSize

		pointerFile -= 2

		#print "la wea de la wea weon qlo"


		porcentajeAnterior = -1
		startOfMenuFile = Constants.hexListToChar(startOfMenuFile)
		endOfMenuFile = Constants.hexListToChar(Constants.Constants.endOfMenuFile)
		pointerFile = 0
		lineaArchivo = self.fullFile[pointerFile:pointerFile+4]
		pointerFile += 2
		newFile = ""
		i = 0
		while pointerFile < fileSize:
			if lineaArchivo == startOfMenuFile:
				while lineaArchivo != endOfMenuFile:
					lineaArchivo = lineaArchivo[2:4]
					lineaArchivo += self.fullFile[pointerFile:pointerFile+2]
					pointerFile += 2

				lineaArchivo = lineaArchivo[2:4]
				lineaArchivo += self.fullFile[pointerFile:pointerFile+2]
				pointerFile += 2
				#print [self.fullFile[pointerFile]]
				#print len(self.menusList), i
				newFile += self.menusList[i].getAsLine()
				#print [newFile[-4:]]
				#print [lineaArchivo]
				i+=1
			else:
				newFile += lineaArchivo[:2]


				pointerFile += 2
			lineaArchivo = lineaArchivo[2:4]
			lineaArchivo += self.fullFile[pointerFile:pointerFile+2]

			if int(pointerFile / fileSize * 10) > porcentajeAnterior:
				porcentajeAnterior = int(pointerFile / fileSize * 10)
				if not gui is None:
					gui.updateProgressBar()
				else:
					print 100 * pointerFile / fileSize

		#print len(self.fullFile), len(newFile)
		#print newFile == self.fullFile
		#print len(self.fullFile) - len(newFile)
		#a = obtenerDiferencias(self.fullFile, newFile)
		#for asd in range(len(a)-10, len(a)):
		#if a:
		#	for asd in range(min(10, len(a))):
		#		print a[asd]
		#	print len(a)

		debugOriginal = open("debugOriginal", "wb")
		debugOriginal.write(self.fullFile)
		debugOriginal.close()

		debugNew = open("debugNew", "wb")
		debugNew.write(newFile)
		debugNew.close()

		self.fullFile = newFile

	def saveFile(self, filename=None, gui=None):
		if not filename:
			filename = self.filename
		
		self.updateFileData(gui)

		archivo = open(filename, "wb")
		archivo.write(self.fullFile)
		archivo.close()

		return self

	def __str__(self):
		return "CharacterUnkParser <"+self.filename+">"
