from __future__ import absolute_import, print_function
from . import TransformClass, FusionClass, CharacterMenu, Constants


class CharacterUnkParser:
    def __init__(self, name, printData=False):
        # type: (str, bool) -> None
        self.filename = name
        self.transObj = None
        self.fusionObj = None
        self.menusList = list()
        self.printData = printData

        fullFile = open(self.filename, "rb")
        self.fullFile = fullFile.read()
        fullFile.close()
        return

    def __getTransformData(self):
        # type: () -> TransformClass.TransformClass
        filesConst = Constants.FilesConst()
        transformCode = filesConst.transformCode
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4

        line = self.fullFile[pointerFile+8:pointerFile+30]

        # line1 = self.fullFile[pointerFile:pointerFile + 16]
        # pointerFile += 16
        # line2 = self.fullFile[pointerFile:pointerFile + 14]
        # self.transObj = TransformClass.TransformClass(line1, line2, self.printData)
        self.transObj = TransformClass.TransformClass(line, self.printData)
        return self.transObj

    def __getFusionData(self):
        # type: () -> FusionClass.FusionClass
        filesConst = Constants.FilesConst()
        transformCode = filesConst.transformCode
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4
        pointerFile += 30

        self.fusionObj = FusionClass.FusionClass(self.fullFile[pointerFile:pointerFile + 24], self.printData)
        return self.fusionObj

    def __getMenusData(self):
        # type: () -> list
        filesConst = Constants.FilesConst()
        startOfMenuFile = filesConst.startOfMenuFile
        endOfMenuFile = filesConst.endOfMenuFile

        starts = Constants.findDataPos(self.fullFile, startOfMenuFile, 8)
        pointer = 0
        while pointer < len(starts):
            pointerFile = starts[pointer]-2
            pos = self.fullFile.find(endOfMenuFile, pointerFile)
            menu = self.fullFile[pointerFile:pos]
            self.menusList.append(CharacterMenu.CharacterMenu(menu, self.printData))
            pointer += 1

        return self.menusList

    def parse(self):
        # type: () -> None
        self.__getTransformData()
        self.__getFusionData()
        self.__getMenusData()
        return

    def __setTransformData(self, src):
        # type: (CharacterUnkParser) -> bytes
        filesConst = Constants.FilesConst()
        transformCode = filesConst.transformCode
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4

        transLines = src.transObj.getAsLine()
        return self.fullFile[:pointerFile+8] + transLines + self.fullFile[pointerFile + 30:]

    def __setFusionData(self, src):
        # type: (CharacterUnkParser) -> bytes
        filesConst = Constants.FilesConst()
        transformCode = filesConst.transformCode
        pointerFile = self.fullFile.find(transformCode) + 16 * 7 - 4
        pointerFile += 30

        fusionLine = src.fusionObj.getAsLine()
        return self.fullFile[:pointerFile] + fusionLine + self.fullFile[pointerFile + 24:]

    def __setMenuData(self, src):
        # type: (CharacterUnkParser) -> bytes
        filesConst = Constants.FilesConst()
        startOfMenuFile = filesConst.startOfMenuFile
        endOfMenuFile = filesConst.endOfMenuFile

        starts = Constants.findDataPos(self.fullFile, startOfMenuFile, 8)
        ends = Constants.findDataPos(self.fullFile, endOfMenuFile, 8)

        newFile = self.fullFile[:starts[0]]
        for pointer in range(len(starts)):
            newFile += src.menusList[pointer].getAsLine()
            if pointer + 1 == len(starts):
                newFile += self.fullFile[ends[pointer] + 4:]
            else:
                newFile += self.fullFile[ends[pointer] + 4:starts[pointer + 1]]
        return newFile

    def updateFileData(self, src):
        # type: (CharacterUnkParser) -> None
        if not src:
            src = self
        self.fullFile = self.__setTransformData(src)
        self.fullFile = self.__setFusionData(src)
        self.fullFile = self.__setMenuData(src)
        return

    def saveFile(self, filename=None, src=None):
        # type: (str, CharacterUnkParser) -> None
        if not filename:
            filename = self.filename

        self.updateFileData(src)

        finalFile = open(filename, "wb")
        finalFile.write(self.fullFile)
        finalFile.close()
        return

    def __str__(self):
        # type: () -> str
        return str("CharacterUnkParser <" + self.filename + ">")
