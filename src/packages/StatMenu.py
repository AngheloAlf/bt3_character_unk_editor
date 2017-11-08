from __future__ import absolute_import

from . import Constants, StatChars


class StatMenu:
    def __init__(self, statData, printData=False):
        # type: (bytes, bool) -> None
        self.printData = printData
        self.maxPower = statData[:2]
        self.usedBars = statData[2:4]
        self.usedKi = statData[4:6]
        self.name = b""
        self.statChars = []

        filesConst = Constants.FilesConst()
        endOfLine = filesConst.endOfLine
        pos = statData.find(endOfLine, 6)
        self.name = statData[6:pos]

        if self.printData:
            print("\n\t\tStatMenu:")
            print("\t\t\tname: ", self.name, self.name.decode("utf-16"))
            print("\t\t\tmaxPower: ", self.maxPower, self.maxPower.decode("utf-16"))
            print("\t\t\tusedBars: ", self.usedBars, self.usedBars.decode("utf-16"))
            print("\t\t\tusedKi ", self.usedKi, self.usedKi.decode("utf-16"))

        ends = Constants.findDataPos(statData, endOfLine, inicio=pos)[1:]
        for i in ends:
            newStatChars = StatChars.StatChars(statData[pos+2:i+2], self.printData)
            self.statChars.append(newStatChars)
            pos = i
        return

    def getName(self):
        # type: () -> str
        return self.name.decode("utf-16")

    def setName(self, name):
        # type: (str) -> None
        self.name = name.encode("utf-16")[2:]
        return

    def getMaxPower(self):
        # type: () -> int
        return int(self.maxPower.decode("utf-16"))

    def setMaxPower(self, data):
        # type: (int) -> None
        self.maxPower = str(data).encode("utf-16")[2:]
        return

    def getBarrasKi(self):
        # type: () -> str
        return self.usedBars.decode("utf-16")

    def setBarrasKi(self, data):
        # type: (str) -> None
        self.usedBars = data.encode("utf-16")[2:]
        return

    def getReservaKi(self):
        # type: () -> str
        return self.usedKi.decode("utf-16")

    def setReservaKi(self, data):
        # type: (str) -> None
        self.usedKi = data.encode("utf-16")[2:]
        return

    def getStatChars(self):
        # type: () -> list
        return [x.getUnicodeList() for x in self.statChars]

    def getAsLine(self):
        # type: () -> str
        filesConst = Constants.FilesConst()
        statCode = filesConst.statCode
        endOfLine = filesConst.endOfLine
        line = statCode
        line += self.maxPower + self.usedBars + self.usedKi
        line += self.name + endOfLine
        line += b"".join([x.getAsLine() for x in self.statChars])
        return line

    def __str__(self):
        # type: () -> str
        if type(b"") != str:  # py3
            return "StatMenu <" + self.name.decode('utf-16') + ">"
        return "StatMenu <" + self.name[::2] + ">"
