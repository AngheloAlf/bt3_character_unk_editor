class TransformClass:
    def __init__(self, line1, line2, printData=False):
        # type: (str, str, bool) -> None
        self.unknowFirst = line1[:8]
        self.trans = list(line1[8:12])
        self.barras = list(line1[12:])

        self.aniCam = list(line2[:4])
        self.aura = list(line2[4:8])
        self.abs = list(line2[8:12])
        self.command = line2[12]
        self.bonus = line2[13]
        if printData:
            print(u"Transform:")
            print(u"unknowFirst:", map(ord, list(self.unknowFirst)))
            print(u"trans:", map(ord, self.trans))
            print(u"barras:", map(ord, self.barras))
            print(u"ani:", map(ord, self.aniCam))
            print(u"abs:", map(ord, self.abs))
            print(u"r3command:", [ord(self.command)])
            print(u"bonus:", [ord(self.bonus)])
            print(u"\n")

    def getR3Command(self, asOrd=False):
        # type: (bool) -> int|str
        if asOrd:
            return ord(self.command)
        return self.command

    def setR3Command(self, command, asOrd=False):
        # type: (int|str, bool) -> bool
        if asOrd and (command < 0 or command > 255):
            return False

        if not asOrd and (ord(command) < 0 or ord(command) > 255):
            return False

        if asOrd:
            command = chr(command)

        self.command = command

        return True

    def getTransformData(self, charNumb, asOrd=False):
        # type: (int, bool) -> list
        if charNumb < 0 or charNumb > 3:
            return list()

        data = [self.trans[charNumb]] + [self.barras[charNumb]] + [self.aniCam[charNumb]] + [self.aura[charNumb]] + [
            self.abs[charNumb]]

        if asOrd:
            return map(ord, data)

        return data

    def setTransformData(self, charNumb, data, asOrd=False):
        # type: (int, list, bool) -> bool
        if charNumb < 0 or charNumb > 3 or len(data) != 5:
            return False

        for i in range(5):
            j = data[i]
            if asOrd and (j < 0 or j > 255):
                return False
            if not asOrd and (ord(j) < 0 or ord(j) > 255):
                return False

        if asOrd:
            data = map(chr, data)

        self.trans[charNumb] = data[0]
        self.barras[charNumb] = data[1]
        self.aniCam[charNumb] = data[2]
        self.aura[charNumb] = data[3]
        self.abs[charNumb] = data[4]

        return True

    def getBonus(self, asOrd=False):
        # type: (bool) -> int|str
        if asOrd:
            return ord(self.bonus)
        return self.bonus

    def setBonus(self, bonus, asOrd=False):
        # type: (int|str, bool) -> bool
        if asOrd and (bonus < 0 or bonus > 255):
            return False

        if not asOrd and (ord(bonus) < 0 or ord(bonus) > 255):
            return False

        if asOrd:
            bonus = chr(bonus)

        self.bonus = bonus
        return True

    def getAsLines(self):
        # type: () -> list
        line1 = self.unknowFirst
        line1 += "".join(self.trans)
        line1 += "".join(self.barras)

        line2 = "".join(self.aniCam)
        line2 += "".join(self.aura)
        line2 += "".join(self.abs)
        line2 += self.command
        line2 += self.bonus

        return [line1, line2]

    def __str__(self):
        # type: () -> str
        return "TransformClass <>"
