import Constants


class StatMenu:
    def __init__(self, statName, statChars):
        self.name = statName[1]
        self.data = statName[0]  # MaxPower, BarrasKiOcupa, KiOcupa
        self.statChars = statChars

    def getName(self):
        # type: () -> unicode
        return unicode(self.name, "utf-16")

    def setName(self, name):
        # type: (unicode) -> None
        self.name = name.encode("utf-16")[2:]
        return

    def getMaxPower(self):
        # type: () -> int
        return int(unicode(self.data[0], "utf-16"))

    def setMaxPower(self, data):
        # type: (int) -> None
        self.data[0] = unicode(data).encode("utf-16")[2:]
        return

    def getBarrasKi(self):
        # type: () -> unicode
        return unicode(self.data[1], "utf-16")

    def setBarrasKi(self, data):
        # type: (str) -> None
        self.data[1] = data.encode("utf-16")[2:]
        return

    def getReservaKi(self):
        # type: () -> unicode
        return unicode(self.data[2], "utf-16")

    def setReservaKi(self, data):
        # type: (str) -> None
        self.data[2] = data.encode("utf-16")[2:]
        return

    def getStatChars(self):
        # type: () -> list
        return [[unicode(y, "utf-16") for y in x] for x in self.statChars]
        # return map(lambda x: [unicode(y, "utf-16") for y in x], self.statChars)

    # def setStatChars(self, data):
    #    a = map(lambda x: [y.encode("utf-16")[2:] for y in x], data)
    #    print a
    #    print self.statChars
    #    return a == self.statChars

    def getAsLine(self):
        # type: () -> str
        statCode = Constants.hexListToChar(Constants.statCode)
        endOfLine = Constants.hexListToChar(Constants.endOfLine)
        line = statCode + "".join(self.data) + self.name + endOfLine
        line += "".join(["".join(x) + endOfLine for x in self.statChars])
        return line

    def __str__(self):
        # type: () -> str
        return "StatMenu <" + self.name[1][::2] + ">"
