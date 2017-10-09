from __future__ import absolute_import

from . import Constants, StatChars


class StatMenu:
    def __init__(self, statName, statChars):
        self.name = statName[1]
        self.data = statName[0]  # MaxPower, BarrasKiOcupa, KiOcupa
        self.statChars = []
        for i in statChars:
            self.statChars.append(StatChars.StatChars(i))

    def getName(self):
        # type: () -> str
        return self.name.decode("utf-16")

    def setName(self, name):
        # type: (str) -> None
        self.name = name.encode("utf-16")[2:]
        return

    def getMaxPower(self):
        # type: () -> int
        return int(self.data[0].decode("utf-16"))

    def setMaxPower(self, data):
        # type: (int) -> None
        self.data[0] = str(data).encode("utf-16")[2:]
        return

    def getBarrasKi(self):
        # type: () -> str
        return self.data[1].decode("utf-16")

    def setBarrasKi(self, data):
        # type: (str) -> None
        self.data[1] = data.encode("utf-16")[2:]
        return

    def getReservaKi(self):
        # type: () -> str
        return self.data[2].decode("utf-16")

    def setReservaKi(self, data):
        # type: (str) -> None
        self.data[2] = data.encode("utf-16")[2:]
        return

    def getStatChars(self):
        # type: () -> list
        return [x.getUnicodeList() for x in self.statChars]

    def getAsLine(self):
        # type: () -> str
        filesConst = Constants.FilesConst()
        statCode = filesConst.statCode
        endOfLine = filesConst.endOfLine
        line = statCode + b"".join(self.data) + self.name + endOfLine
        line += b"".join([x.getAsLine() for x in self.statChars])
        return line

    def __str__(self):
        # type: () -> str
        if type(b"") == bytes:
            return "StatMenu <" + self.name.decode('utf-16') + ">"
        return "StatMenu <" + self.name[::2] + ">"
