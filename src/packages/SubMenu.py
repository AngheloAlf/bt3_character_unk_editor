from __future__ import absolute_import
from __future__ import print_function

from . import StatMenu, Constants


def getMenuName(submenuData, i):
    # type: (bytes, int) -> list
    i += 6
    nameData = [submenuData[i:i + 2]]
    i += 2
    filesConst = Constants.FilesConst()
    name = submenuData.find(filesConst.endOfLine, i)
    nameData.append(submenuData[i:name])
    return nameData


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
    else:
        return StatMenu.StatMenu([statNumbers, statName], statChars)


class SubMenu:
    def __init__(self, submenuData):
        # type: (bytes) -> None
        self.menuName = []
        self.stats = []

        if submenuData != b"":
            filesConst = Constants.FilesConst()
            menuNameCode = filesConst.menuNameCode
            statCode = filesConst.statCode

            # Nombre del menu
            menuNamePos = submenuData.find(menuNameCode)
            self.menuName = getMenuName(submenuData, menuNamePos)

            # Cada stat
            eachStatPos = Constants.findDataPos(submenuData, statCode) + [len(submenuData)]
            for i in range(len(eachStatPos) - 1):
                j = eachStatPos[i]
                self.stats.append(getStat(submenuData, j))
        else:
            self.menuName = [b"", b""]

    def isNone(self):
        # type: () -> bool
        return len(self.menuName) < 2

    def getMenuNum(self):
        # type: () -> int
        return int(self.menuName[0].decode("utf-16"))

    def setMenuNum(self, num):
        # type: (int) -> None
        self.menuName[0] = str(num).encode("utf-16")[2:]

    def getMenuName(self):
        # type: () -> str
        return self.menuName[1].decode("utf-16")

    def setMenuName(self, name):
        # type: (str) -> None
        if self.menuName[1] != name.encode("utf-16")[2:]:
            print(u"Cambiando:")
            print("\t" + self.menuName[1].decode("utf-16") + "->" + name.encode("utf-16").decode("utf-16"))
        self.menuName[1] = name.encode("utf-16")[2:]
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
        if len(self.menuName) >= 2:
            return "SubMenu <" + self.menuName[1].decode("utf-16") + ">"
        else:
            return "SubMenu <None>"
