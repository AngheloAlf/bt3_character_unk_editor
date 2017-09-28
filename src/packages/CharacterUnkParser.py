from __future__ import absolute_import

import packages.TransformClass as TransformClass
import packages.FusionClass as FusionClass
import packages.CharacterMenu as CharacterMenu
import packages.Constants as Constants


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
    # charMenuObj = None
    # menu = b""

    endOfMenuFile = Constants.FilesConst().endOfMenuFile

    pos = archivo.find(endOfMenuFile, pointerFile-4)

    encontrado = archivo[pointerFile-4:pos]

    charMenuObj = CharacterMenu.CharacterMenu(encontrado)

    # lineaArchivo = archivo[pointerFile - 4:pointerFile]

    # while lineaArchivo != "":
    #     menu += lineaArchivo[0:2]
    #     if lineaArchivo == endOfMenuFile:
    #         menu += lineaArchivo[2:4]
    #         print(menu == encontrado)
    #         print("menu\t\t", len(menu), menu)
    #         print("encontrado\t", len(encontrado), encontrado)
    #         print(len(menu)-len(encontrado))
    #         charMenuObj = CharacterMenu.CharacterMenu(menu)
    #         break
    #     lineaArchivo = lineaArchivo[2:4]
    #     lineaArchivo += archivo[pointerFile:pointerFile + 2]
    #     pointerFile += 2
    return charMenuObj


def setTransformData(archivo, pointerFile, transLines):
    # type: (str, int, list) -> str
    archivo = archivo[:pointerFile] + transLines[0] + transLines[1] + archivo[pointerFile + 30:]
    return archivo


def setFusionData(archivo, pointerFile, fusionLine):
    # type: (str, int, str) -> str
    archivo = archivo[:pointerFile] + fusionLine + archivo[pointerFile + 24:]
    return archivo


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
        # transformCode = Constants.hexListToChar(Constants.FilesConst().transformCode)
        transformCode = Constants.FilesConst().transformCode
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4
        print(pointerFile)
        self.transObj = getTransformData(self.fullFile, pointerFile, self.printData)
        self.fusionObj = getFusionData(self.fullFile, pointerFile+30, self.printData)

        # startOfMenuFile = Constants.hexListToChar(Constants.FilesConst().startOfMenuFile)
        startOfMenuFile = Constants.FilesConst().startOfMenuFile
        starts = Constants.findDataPos(self.fullFile, startOfMenuFile, 8)
        pointer = 0
        while pointer < len(starts):
            charMenuObj = getMenusData(self.fullFile, starts[pointer]+2)
            self.menusList.append(charMenuObj)
            pointer += 1

        return

    def updateFileData(self, src):
        # type: (CharacterUnkParser) -> None
        # transformCode = Constants.hexListToChar(Constants.FilesConst().transformCode)
        transformCode = Constants.FilesConst().transformCode
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4
        
        if src:
            transLines = src.transObj.getAsLines()
            fusionLine = src.fusionObj.getAsLines()
        else:
            transLines = self.transObj.getAsLines()
            fusionLine = self.fusionObj.getAsLines()
        
        self.fullFile = setTransformData(self.fullFile, pointerFile, transLines)
        self.fullFile = setFusionData(self.fullFile, pointerFile+30, fusionLine)

        # startOfMenuFile = Constants.hexListToChar(Constants.FilesConst().startOfMenuFile)
        startOfMenuFile = Constants.FilesConst().startOfMenuFile
        # endOfMenuFile = Constants.hexListToChar(Constants.FilesConst().endOfMenuFile)
        endOfMenuFile = Constants.FilesConst().endOfMenuFile
        starts = Constants.findDataPos(self.fullFile, startOfMenuFile, 8)
        ends = Constants.findDataPos(self.fullFile, endOfMenuFile, 8)

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
