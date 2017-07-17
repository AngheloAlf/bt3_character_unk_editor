import Constants
import StatMenu


def getMenuName(submenuData, i):
    # type: (str, int) -> (list, int)
    nameData = [submenuData[i:i + 2]]
    i += 2
    menuName = ""
    while map(ord, submenuData[i:i + 2]) != Constants.endOfLine:
        menuName += submenuData[i]
        i += 1
    nameData.append(menuName)
    return nameData, i


def getStat(submenuData, i):
    # type: (str, int) -> (StatMenu.StatMenu, int)
    statNumbers = [submenuData[i:i + 2], submenuData[i + 2:i + 4], submenuData[i + 4:i + 6]]
    i += 6
    statName = ""
    while map(ord, submenuData[i:i + 2]) != Constants.endOfLine:
        statName += submenuData[i]
        i += 1
    i += 2

    statChars = []
    while i + 7 < len(submenuData) and map(ord, submenuData[i + 1:i + 7]) != Constants.statCode:
        if ord(submenuData[i]) == 0x0:
            i += 1

        subStatFirst = submenuData[i:i + 6]
        i += 6

        description = ""
        while map(ord, submenuData[i:i + 2]) != Constants.endOfLine:
            description += submenuData[i]
            i += 1

        statChars.append([subStatFirst, description])
        i += 1

    return StatMenu.StatMenu([statNumbers, statName], statChars), i


class SubMenu:
    def __init__(self, submenuData):
        self.menuName = []
        self.stats = []
        i = 0

        while i < len(submenuData):
            if i + 5 < len(submenuData):
                # Nombre del menu
                if map(ord, submenuData[i:i + 6]) == Constants.menuNameCode:
                    i += 6
                    self.menuName, i = getMenuName(submenuData, i)

                # Cada stat
                if map(ord, submenuData[i:i + 6]) == Constants.statCode:
                    i += 6
                    newStat, i = getStat(submenuData, i)
                    self.stats.append(newStat)
            i += 1

    def isNone(self):
        # type: () -> bool
        return len(self.menuName) < 2

    def getMenuNum(self):
        # type: () -> int
        return int(unicode(self.menuName[0], "utf-16"))

    def getMenuName(self):
        # type: () -> unicode
        return unicode(self.menuName[1], "utf-16")

    def setMenuName(self, name):
        # type: (unicode) -> None
        if self.menuName[1] != name.encode("utf-16")[2:]:
            print "Cambiando:"
            print "\t", self.menuName[1], "->", name.encode("utf-16")[2:]
        self.menuName[1] = name.encode("utf-16")[2:]
        return

    def getAsLine(self):
        # type: () -> str
        menuNameCode = Constants.hexListToChar(Constants.menuNameCode)
        endOfLine = Constants.hexListToChar(Constants.endOfLine)
        line = ""
        if len(self.menuName) == 2:
            line += menuNameCode + self.menuName[0] + self.menuName[1] + endOfLine
        else:
            print self.menuName
            print len(self.stats)
        for i in self.stats:
            line += i.getAsLine()
        return line

    def __str__(self):
        if len(self.menuName) >= 2:
            return "SubMenu <" + self.menuName[1][::2] + ">"
        else:
            return "SubMenu <None>"
