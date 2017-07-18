import TransformClass
import FusionClass
import CharacterMenu
import Constants


def getTransformData(archivo, pointerFile, printData):
    # type: (str, int, bool) -> TransformClass.TransformClass
    line1 = archivo[pointerFile:pointerFile + 16]
    pointerFile += 16
    line2 = archivo[pointerFile:pointerFile + 14]
    return TransformClass.TransformClass(line1, line2, printData)


def getFusionData(archivo, pointerFile, printData):
    # type: (str, int, bool) -> FusionClass.FusionClass
    return FusionClass.FusionClass(archivo[pointerFile:pointerFile + 24], printData)


def getMenusData(archivo, pointerFile):
    # type: (str, int) -> CharacterMenu.CharacterMenu
    charMenuObj = None
    menu = ""

    lineaArchivo = archivo[pointerFile - 4:pointerFile]

    endOfMenuFile = Constants.endOfMenuFile

    while lineaArchivo != "":
        puntero = map(ord, lineaArchivo)
        menu += lineaArchivo[0:2]
        if puntero == endOfMenuFile:
            menu += lineaArchivo[2:4]
            charMenuObj = CharacterMenu.CharacterMenu(menu)
            break
        lineaArchivo = lineaArchivo[2:4]
        lineaArchivo += archivo[pointerFile:pointerFile + 2]
        pointerFile += 2
    return charMenuObj


def setTransformData(archivo, pointerFile, transLines):
    # type: (str, int, list) -> str
    archivo = archivo[:pointerFile] + transLines[0] + transLines[1] + archivo[pointerFile + 30:]
    return archivo


def setFusionData(archivo, pointerFile, fusionLine):
    # type: (str, int, str) -> str
    archivo = archivo[:pointerFile] + fusionLine + archivo[pointerFile + 24:]
    return archivo


def findDataPos(archivo, data, maxi):
    # type: (str, str, int) -> list
    i = 0
    l = list()
    pos = 0
    while i < maxi:
        finded = archivo.find(data, pos)
        if finded == -1:
            break
        l.append(finded)
        i += 1
        pos = finded+1
    return l


class CharacterUnkParser:
    def __init__(self, name, printData=False):
        # type: (unicode, bool) -> None
        self.filename = name
        self.transObj = None
        self.fusionObj = None
        self.menusList = list()
        self.printData = printData

        archivo = open(self.filename, "rb")
        self.fullFile = archivo.read()
        archivo.close()

    def parse(self):
        # type: () -> None
        transformCode = Constants.hexListToChar(Constants.transformCode)
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4
        print pointerFile
        self.transObj = getTransformData(self.fullFile, pointerFile, self.printData)
        self.fusionObj = getFusionData(self.fullFile, pointerFile+30, self.printData)

        startOfMenuFile = Constants.hexListToChar(Constants.startOfMenuFile)
        starts = findDataPos(self.fullFile, startOfMenuFile, 8)
        pointer = 0
        while pointer < len(starts):
            charMenuObj = getMenusData(self.fullFile, starts[pointer]+2)
            self.menusList.append(charMenuObj)
            pointer += 1

        return

    def updateFileData(self, src):
        # type: (CharacterUnkParser) -> None
        transformCode = Constants.hexListToChar(Constants.transformCode)
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4
        
        if src:
            transLines = src.transObj.getAsLines()
            fusionLine = src.fusionObj.getAsLines()
        else:
            transLines = self.transObj.getAsLines()
            fusionLine = self.fusionObj.getAsLines()
        
        self.fullFile = setTransformData(self.fullFile, pointerFile, transLines)
        self.fullFile = setFusionData(self.fullFile, pointerFile+30, fusionLine)

        startOfMenuFile = Constants.hexListToChar(Constants.startOfMenuFile)
        endOfMenuFile = Constants.hexListToChar(Constants.endOfMenuFile)
        starts = findDataPos(self.fullFile, startOfMenuFile, 8)
        ends = findDataPos(self.fullFile, endOfMenuFile, 8)

        newFile = self.fullFile[:starts[0]]
        pointer = 0
        while pointer < len(starts)-1:
            if src:
                newMenu = src.menusList[pointer].getAsLine()
            else:
                newMenu = self.menusList[pointer].getAsLine()
            newFile += newMenu + self.fullFile[ends[pointer]+4:starts[pointer+1]]
            pointer += 1
        if src:
            newMenu = src.menusList[pointer].getAsLine()
        else:
            newMenu = self.menusList[pointer].getAsLine()
        newFile += newMenu + self.fullFile[ends[pointer]+4:]

        self.fullFile = newFile
        return

    def saveFile(self, filename=None, src=None):
        # type: (unicode, CharacterUnkParser) -> None
        if not filename:
            filename = self.filename

        self.updateFileData(src)

        archivo = open(filename, "wb")
        archivo.write(self.fullFile)
        archivo.close()

    def __str__(self):
        # type: () -> str
        return str("CharacterUnkParser <" + self.filename + ">")
