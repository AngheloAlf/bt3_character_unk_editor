from __future__ import print_function


class TransformClass:
    def __init__(self, line1, line2, printData=False):
        # type: (bytes, bytes, bool) -> None
        self.unknowFirst = line1[:8]
        self.trans = line1[8:12]
        self.barras = line1[12:]

        self.aniCam = line2[:4]
        self.aura = line2[4:8]
        self.abs = line2[8:12]
        self.command = line2[12:13]
        self.bonus = line2[13:14]
        if printData:
            print(u"Transform:")
            print(u"unknowFirst:", list(self.unknowFirst))
            print(u"trans:", self.trans)
            print(u"barras:", self.barras)
            print(u"ani:", self.aniCam)
            print(u"abs:", self.abs)
            print(u"r3command:", self.command)
            print(u"bonus:", self.bonus)
            print(u"\n")

    def getR3Command(self):
        # type: () -> int
        if type(self.command) == int:
            return self.command
        return ord(self.command)

    def setR3Command(self, command):
        # type: (int) -> bool
        if command < 0 or command > 255:
            return False

        aux = b""
        if type(b"") == str:  # py2
            aux = chr(command)
        else:  # py3
            aux = bytes([command])
        self.command = aux
        return True

    def getTransformData(self, charNumb):
        # type: (int) -> list
        if charNumb < 0 or charNumb > 3:
            return list()

        data = [self.trans[charNumb], self.barras[charNumb], self.aniCam[charNumb], self.aura[charNumb],
                self.abs[charNumb]]

        if type(data[0]) == int:
            return data
        return list(map(ord, data))

    def setTransformData(self, charNumb, data):
        # type: (int, list) -> bool
        if charNumb < 0 or charNumb > 3 or len(data) != 5:
            return False

        for i in range(5):
            j = data[i]
            if j < 0 or j > 255:
                return False

        if type(self.trans[charNumb]) != int:
            data = list(map(chr, data))

        if type(data[0]) == int:
            data = [bytes([x]) for x in data]

        self.trans = self.trans[:charNumb] + data[0] + self.trans[charNumb+1:]
        self.barras = self.barras[:charNumb] + data[1] + self.barras[charNumb+1:]
        self.aniCam = self.aniCam[:charNumb] + data[2] + self.aniCam[charNumb+1:]
        self.aura = self.aura[:charNumb] + data[3] + self.aura[charNumb+1:]
        self.abs = self.abs[:charNumb] + data[4] + self.abs[charNumb+1:]

        return True

    def getBonus(self):
        # type: () -> int
        if type(self.bonus) == int:
            return self.bonus
        return ord(self.bonus)

    def setBonus(self, bonus):
        # type: (int) -> bool
        if bonus < 0 or bonus > 255:
            return False

        aux = b""
        if type(b"") == str:  # py2
            aux = chr(bonus)
        else:  # py3
            aux = bytes([bonus])
        self.bonus = aux
        return True

    def getAsLines(self):
        # type: () -> list
        line1 = self.unknowFirst
        line1 += self.trans
        line1 += self.barras

        line2 = self.aniCam
        line2 += self.aura
        line2 += self.abs
        line2 += self.command
        line2 += self.bonus

        return [line1, line2]

    def __str__(self):
        # type: () -> str
        return "TransformClass <>"
