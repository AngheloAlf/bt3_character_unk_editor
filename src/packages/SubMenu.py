from __future__ import absolute_import
from __future__ import print_function

from . import StatMenu, Constants


def getStat(submenuData, i):
    # type: (bytes, int) -> StatMenu.StatMenu
    i += 6
    filesConst = Constants.FilesConst()
    endOfLine = filesConst.endOfLine
    statCode = filesConst.statCode

    statNumbers = [submenuData[i:i + 2], submenuData[i + 2:i + 4], submenuData[i + 4:i + 6]]
    i += 6
    pos = submenuData.find(endOfLine, i)

    statName = submenuData[i:pos]
    i = pos + 2

    tope = submenuData.find(statCode, i)
    ends = Constants.findDataPos(submenuData, endOfLine, inicio=i, tope=tope)

    statChars = []
    if len(ends) > 0:
        subStatFirst = submenuData[i:i+6]
        subStatFirstList1 = [subStatFirst]
        description = submenuData[i+6:ends[0]]
        statChars.append([subStatFirst, description])
        for endI in range(len(ends[:-1])):
            end = ends[endI]
            end += 2
            subStatFirst = submenuData[end:end+6]
            subStatFirstList1.append(subStatFirst)
            end += 6

            description = submenuData[end:ends[endI+1]]
            statChars.append([subStatFirst, description])

    return StatMenu.StatMenu([statNumbers, statName], statChars)


class SubMenu:
    def __init__(self, submenuData, printData=False):
        # type: (bytes, bool) -> None
        self.menuNum = b''
        self.menuName = b''
        self.stats = []
        self.printData = printData
        if self.printData:
            print("\nsubMenu ")

        if submenuData != b"":
            filesConst = Constants.FilesConst()
            statCode = filesConst.statCode

            # Nombre del menu
            self.__searchMenuName(submenuData)

            # Cada stat
            for i in Constants.findDataPos(submenuData, statCode):
                self.stats.append(getStat(submenuData, i))
        return

    def __searchMenuName(self, submenuData):
        # type: (bytes) -> list[bytes]
        filesConst = Constants.FilesConst()
        menuNameCode = filesConst.menuNameCode
        pos = submenuData.find(menuNameCode) + 6
        self.menuNum = submenuData[pos:pos + 2]
        end = submenuData.find(filesConst.endOfLine, pos+2)
        self.menuName = submenuData[pos:end]
        if self.printData:
            print("\n\tsubMenu: ")
            print("\t\tmenuNum: ", self.menuNum)
            print("\t\t", self.menuName)
        return [self.menuNum, self.menuName]

    def isNone(self):
        # type: () -> bool
        return len(self.menuName) < 2

    def getMenuNum(self):
        # type: () -> int
        return int(self.menuNum.decode("utf-16"))

    def setMenuNum(self, num):
        # type: (int) -> None
        self.menuNum = str(num).encode("utf-16")[2:]
        return

    def getMenuName(self):
        # type: () -> str
        return self.menuName.decode("utf-16")

    def setMenuName(self, name):
        # type: (str) -> None
        if self.menuName != name.encode("utf-16")[2:]:
            print(u"Cambiando:")
            print("\t" + self.menuName.decode("utf-16") + "->" + name.encode("utf-16").decode("utf-16"))
        self.menuName = name.encode("utf-16")[2:]
        return

    def getAsLine(self):
        # type: () -> str
        filesConst = Constants.FilesConst()
        menuNameCode = filesConst.menuNameCode
        endOfLine = filesConst.endOfLine
        line = b""
        if len(self.menuName) == 2:
            line += menuNameCode + self.menuName[0] + self.menuName[1] + endOfLine
        else:
            print(self.menuName)
            print(len(self.stats))
        for i in self.stats:
            line += i.getAsLine()
        return line

    def __str__(self):
        if self.menuName != b"":
            if type(self.menuName) != str:  # py3
                return "SubMenu <" + self.menuName.decode("utf-16") + ">"
            else:  # py2
                return b"SubMenu <" + self.menuName[::2] + b">"
        else:
            return "SubMenu <None>"
