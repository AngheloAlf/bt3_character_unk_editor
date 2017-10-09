from __future__ import absolute_import
from __future__ import print_function

from . import StatMenu, Constants


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
            # Nombre del menu
            self.__searchMenuName(submenuData)

            # Cada stat
            self.__searchAllStats(submenuData)
        return

    def __searchMenuName(self, submenuData):
        # type: (bytes) -> list[bytes]
        filesConst = Constants.FilesConst()
        menuNameCode = filesConst.menuNameCode
        pos = submenuData.find(menuNameCode) + 6
        self.menuNum = submenuData[pos:pos + 2]
        end = submenuData.find(filesConst.endOfLine, pos+2)
        self.menuName = submenuData[pos+2:end]
        if self.printData:
            print("\n\tsubMenu: ")
            print("\t\tmenuNum: ", self.menuNum, self.menuNum.decode("utf-16"))
            print("\t\tmenuName", self.menuName, self.menuName.decode("utf-16"))
        return [self.menuNum, self.menuName]

    def __searchAllStats(self, submenuData):
        # type: (bytes) -> list
        filesConst = Constants.FilesConst()
        statCode = filesConst.statCode

        start = submenuData.find(self.menuName) + len(self.menuName)
        ends = Constants.findDataPos(submenuData, statCode, inicio=start) + [len(submenuData)]
        start = ends[0]+6
        for tope in ends[1:]:
            statmenu = StatMenu.StatMenu(submenuData[start:tope], self.printData)
            self.stats.append(statmenu)
            start = tope+6
        return self.stats

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
        # type: () -> bytes
        filesConst = Constants.FilesConst()
        menuNameCode = filesConst.menuNameCode
        endOfLine = filesConst.endOfLine
        line = b""
        line += menuNameCode + self.menuNum + self.menuName + endOfLine
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
