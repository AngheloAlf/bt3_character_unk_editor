import Constants


class StatMenu:
    def __init__(self, statName, statChars):
        self.name = statName[1]
        self.data = statName[0]  # Necesita MaxPower, BarrasKiOcupa, KiOcupa
        self.statChars = statChars

    # print "\t\t",self

    def getName(self):
        return unicode(self.name, "utf-16")

    def setName(self, name):
        # print name
        # print self.name
        self.name = name.encode("utf-16")[2:]
        return

    def getStatData(self):
        return map(lambda x: unicode(x, "utf-16"), self.data)

    def setStatData(self, data):
        self.data = map(lambda x: x.encode("utf-16")[2:], data)
        return

    def getMaxPower(self):
        return unicode(self.data[0], "utf-16")

    def setMaxPower(self, data):
        self.data[0] = data.encode("utf-16")[2:]

    def getBarrasKi(self):
        return unicode(self.data[1], "utf-16")

    def setBarrasKi(self, data):
        self.data[1] = data.encode("utf-16")[2:]

    def getReservaKi(self):
        return unicode(self.data[2], "utf-16")

    def setReservaKi(self, data):
        self.data[2] = data.encode("utf-16")[2:]

    def getStatChars(self):
        return map(lambda x: [unicode(y, "utf-16") for y in x], self.statChars)

    # def setStatChars(self, data):
    #    a = map(lambda x: [y.encode("utf-16")[2:] for y in x], data)
    #    print a
    #    print self.statChars
    #    return a == self.statChars

    def getAsLine(self):
        statCode = Constants.hexListToChar(Constants.Constants.statCode)
        endOfLine = Constants.hexListToChar(Constants.Constants.endOfLine)
        line = statCode + "".join(self.data) + self.name + endOfLine
        line += "".join(["".join(x) + endOfLine for x in self.statChars])

        return line

    def __str__(self):
        return "StatMenu <" + self.name[1][::2] + ">"
