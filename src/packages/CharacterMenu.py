from __future__ import absolute_import
from . import SubMenu, Constants


class CharacterMenu:
    def __init__(self, menuData, printData=False):
        # type: (bytes, bool) -> None
        self.subMenus = []
        self.unknow = False
        self.printData = printData

        filesConst = Constants.FilesConst()
        menuNameCode = filesConst.menuNameCode

        indices = Constants.findDataPos(menuData, menuNameCode)

        if self.printData:
            print("\nCharacterMenu: \n\tindices: ", indices)

        for i in range(len(indices)):
            if i+1 == len(indices):
                subMenu = menuData[indices[i]:]
            else:
                subMenu = menuData[indices[i]:indices[i+1]]
            self.subMenus.append(SubMenu.SubMenu(subMenu, self.printData))

        if len(self.subMenus) <= 2:
            self.unknow = True

        return

    def isKnow(self):
        # type: () -> bool
        return not self.unknow

    def getAsLine(self):
        # type: () -> bytes
        line = b""
        filesConst = Constants.FilesConst()
        startOfutf16Text = filesConst.startOfutf16Text
        endOfFile = filesConst.endOfFile

        for i in self.subMenus:
            line += i.getAsLine()
        return startOfutf16Text + line + endOfFile

    def __str__(self):
        return "CharacterMenu <> SubMenus: " + str(len(self.subMenus)) + "\t unknow: " + str(self.unknow)
