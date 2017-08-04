import SubMenu
import Constants


class CharacterMenu:
    def __init__(self, menuData):
        # type: (str) -> None
        self.subMenus = []
        self.unknow = False

        menuNameCode = Constants.hexListToChar(Constants.menuNameCode)

        subMenu = ""

        for i in range(len(menuData)):
            byte = menuData[i]
            if i + 5 < len(menuData):
                line = menuData[i:i + 6]
                # if line == menuNameCode or line == endOfFile:
                if line == menuNameCode:
                    # if line == endOfFile:
                    if len(subMenu) > 4:
                        self.subMenus.append(SubMenu.SubMenu(subMenu))
                        subMenu = ""
            subMenu += byte

        self.subMenus.append(SubMenu.SubMenu(subMenu))

        if len(self.subMenus) <= 2:
            self.unknow = True


    def isKnow(self):
        # type: () -> bool
        return not self.unknow

    def getAsLine(self):
        # type: () -> str
        line = ""
        startOfutf16Text = Constants.hexListToChar(Constants.startOfutf16Text)
        endOfFile = Constants.hexListToChar(Constants.endOfFile)
        for i in self.subMenus:
            line += i.getAsLine()
        return startOfutf16Text + line + endOfFile

    def __str__(self):
        return "CharacterMenu <> SubMenus: " + str(len(self.subMenus)) + "\t unknow: " + str(self.unknow)
