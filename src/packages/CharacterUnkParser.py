import TransformClass
import FusionClass
import CharacterMenu
import Constants
import GuiManager


def getTransformData(archivo, pointerFile):
    # type: (str, int) -> (TransformClass.TransformClass, int)
    line1 = archivo[pointerFile:pointerFile + 16]
    pointerFile += 16
    line2 = archivo[pointerFile:pointerFile + 14]
    pointerFile += 14
    return TransformClass.TransformClass(line1, line2), pointerFile


def getFusionData(archivo, pointerFile):
    # type: (str, int) -> (FusionClass.FusionClass, int)
    line = archivo[pointerFile:pointerFile + 24]
    pointerFile += 24
    return FusionClass.FusionClass(line), pointerFile

def getMenusData(archivo, pointerFile):
    # type: (str, int) -> (CharacterMenu.CharacterMenu, int)
    charMenuObj = None
    menu = ""

    lineaArchivo = archivo[pointerFile-4:pointerFile]

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
    return charMenuObj, pointerFile


def setTransformData(archivo, pointerFile, transLines):
    # type: (str, int, list) -> (str, int)
    archivo = archivo[:pointerFile] + transLines[0] + transLines[1] + archivo[pointerFile + 30:]
    pointerFile += 16 + 14
    return archivo, pointerFile


def setFusionData(archivo, pointerFile, fusionLine):
    # type: (str, int, str) -> (str, int)
    archivo = archivo[:pointerFile] + fusionLine + archivo[pointerFile + 24:]
    pointerFile += 24
    return archivo, pointerFile


class CharacterUnkParser:
    def __init__(self, name):
        # type: (str) -> None
        self.filename = name
        self.transObj = None
        self.fusionObj = None
        self.menusList = None
        self.fullFile = ""
        self.fastMode = False
        self.fastModeStart = 0.6

    def parse(self, gui=None):
        # type: (GuiManager.GuiManager) -> CharacterUnkParser
        archivo = open(self.filename, "rb")
        self.fullFile = archivo.read()
        archivo.close()

        fileSize = float(len(self.fullFile))

        startOfMenuFile = Constants.startOfMenuFile
        transformCode = Constants.transformCode

        self.menusList = []

        if gui:
            gui.restartProgressBar()

        pointerFile = 0
        if self.fastMode:
            pointerFile = int(fileSize * self.fastModeStart)
            while pointerFile % 4 != 0:
                pointerFile += 1
            pointerFile += 4
            if gui is not None:
                for i in range(int(20 * self.fastModeStart)):
                    gui.updateProgressBar()

        porcentajeAnterior = -1

        transFound = False

        lineaArchivo = self.fullFile[pointerFile:4 + pointerFile]
        pointerFile += 4

        while lineaArchivo != "" and len(lineaArchivo) == 4:
            puntero = map(ord, lineaArchivo)

            if startOfMenuFile == puntero:
                # lineaArchivo = lineaArchivo[2:4]
                # lineaArchivo += self.fullFile[pointerFile:pointerFile + 2]
                pointerFile += 2
                charMenuObj, pointerFile = getMenusData(self.fullFile, pointerFile)
                self.menusList.append(charMenuObj)

            if not transFound and puntero == transformCode:
                # print "encontrado"
                pointerFile += 16 * 7 - 8
                self.transObj, pointerFile = getTransformData(self.fullFile, pointerFile)
                self.fusionObj, pointerFile = getFusionData(self.fullFile, pointerFile)
                transFound = True

            lineaArchivo = lineaArchivo[2:4]
            lineaArchivo += self.fullFile[pointerFile:pointerFile + 2]
            pointerFile += 2

            if int(pointerFile / fileSize * 20) > porcentajeAnterior:
                porcentajeAnterior = int(pointerFile / fileSize * 20)
                if gui is not None:
                    gui.updateProgressBar()
                else:
                    print 100 * pointerFile / fileSize

        # pointerFile -= 2
        return self

    def updateFileData(self, gui=None):
        # type: (GuiManager.GuiManager) -> CharacterUnkParser
        fileSize = float(len(self.fullFile))

        startOfMenuFile = Constants.startOfMenuFile
        transformCode = Constants.transformCode

        pointerFile = 0
        if self.fastMode:
            pointerFile = int(fileSize * self.fastModeStart)
            while pointerFile % 4 != 0:
                pointerFile += 1
            pointerFile += 4
            if gui is not None:
                for i in range(int(10 * self.fastModeStart)):
                    gui.updateProgressBar()

        porcentajeAnterior = -1

        transFound = False

        lineaArchivo = self.fullFile[pointerFile:4 + pointerFile]
        pointerFile += 2

        while lineaArchivo != "" and len(lineaArchivo) == 4:
            puntero = map(ord, lineaArchivo)

            if not transFound and puntero == transformCode:
                # print "encontrado"
                pointerFile += 16 * 7 - 8
                self.fullFile, pointerFile = setTransformData(self.fullFile, pointerFile, self.transObj.getAsLines())
                self.fullFile, pointerFile = setFusionData(self.fullFile, pointerFile, self.fusionObj.getAsLines())
                transFound = True

            lineaArchivo = lineaArchivo[2:4]
            lineaArchivo += self.fullFile[pointerFile:pointerFile + 2]
            pointerFile += 2

            if int(pointerFile / fileSize * 10) > porcentajeAnterior:
                porcentajeAnterior = int(pointerFile / fileSize * 10)
                if gui is not None:
                    gui.updateProgressBar()
                else:
                    print 100 * pointerFile / fileSize

        pointerFile -= 2

        porcentajeAnterior = -1
        startOfMenuFile = Constants.hexListToChar(startOfMenuFile)
        endOfMenuFile = Constants.hexListToChar(Constants.endOfMenuFile)
        pointerFile = 0
        lineaArchivo = self.fullFile[pointerFile:pointerFile + 4]
        pointerFile += 2
        newFile = ""
        i = 0
        while pointerFile < int(fileSize):
            if lineaArchivo == startOfMenuFile:
                while lineaArchivo != endOfMenuFile:
                    lineaArchivo = lineaArchivo[2:4]
                    lineaArchivo += self.fullFile[pointerFile:pointerFile + 2]
                    pointerFile += 2

                lineaArchivo = lineaArchivo[2:4]
                lineaArchivo += self.fullFile[pointerFile:pointerFile + 2]
                newFile += self.menusList[i].getAsLine()
                i += 1
            else:
                newFile += lineaArchivo[:2]

            pointerFile += 2
            lineaArchivo = lineaArchivo[2:4]
            lineaArchivo += self.fullFile[pointerFile:pointerFile + 2]

            if int(pointerFile / fileSize * 10) > porcentajeAnterior:
                porcentajeAnterior = int(pointerFile / fileSize * 10)
                if gui is not None:
                    gui.updateProgressBar()
                else:
                    print 100 * pointerFile / fileSize

        newFile += lineaArchivo[:2]
        self.fullFile = newFile
        return self

    def saveFile(self, filename=None, gui=None):
        # type: (str, GuiManager.GuiManager) -> CharacterUnkParser
        if not filename:
            filename = self.filename

        self.updateFileData(gui)

        archivo = open(filename, "wb")
        archivo.write(self.fullFile)
        archivo.close()
        return self

    def __str__(self):
        # type: () -> str
        return "CharacterUnkParser <" + self.filename + ">"
