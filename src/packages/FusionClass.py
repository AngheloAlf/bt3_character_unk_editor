class FusionClass:
    def __init__(self, datos, printData=False):
        # type: (str, bool) -> None
        if len(datos) != 24:
            print(1 / 0)
        self.barras = list(datos[0:3])
        self.tipoFusion = list(datos[3:6])
        self.resultado = list(datos[6:9])
        self.compaAni = list(datos[9:12])
        self.compaEquipo = [list(datos[12:16]), list(datos[16:20]), list(datos[20:24])]

        if printData:
            print(u"Fusion:")
            print(u"barras:", map(ord, self.barras))
            print(u"tipoFusion:", map(ord, self.tipoFusion))
            print(u"resultado:", map(ord, self.resultado))
            print(u"compaAni:", map(ord, self.compaAni))
            print(u"compaEquipo", map(lambda x: map(ord, x), self.compaEquipo))
            print(u"\n")

    def getFusionData(self, fusionNumb, asOrd=False):
        # type: (int, bool) -> list
        if fusionNumb < 0 or fusionNumb > 2:
            return list()

        data = [self.barras[fusionNumb]]
        data += [self.tipoFusion[fusionNumb]]
        data += [self.resultado[fusionNumb]]
        data += [self.compaAni[fusionNumb]]
        data += self.compaEquipo[fusionNumb]

        if asOrd:
            data = map(ord, data)

        return data

    def setFusionData(self, fusionNumb, data, asOrd=False):
        # type: (int, list, bool) -> bool
        if fusionNumb < 0 or fusionNumb > 3 or len(data) != 8:
            return False

        for i in range(8):
            j = data[i]
            if asOrd and (j < 0 or j > 255):
                return False
            if not asOrd and (ord(j) < 0 or ord(j) > 255):
                return False

        if asOrd:
            data = map(chr, data)

        self.barras[fusionNumb] = data[0]
        self.tipoFusion[fusionNumb] = data[1]
        self.resultado[fusionNumb] = data[2]
        self.compaAni[fusionNumb] = data[3]
        self.compaEquipo[fusionNumb] = data[4:8]

        return True

    def getAsLines(self):
        # type: () -> str
        line = "".join(self.barras)
        line += "".join(self.tipoFusion)
        line += "".join(self.resultado)
        line += "".join(self.compaAni)
        for i in range(3):
            line += "".join(self.compaEquipo[i])
        return line

    def __str__(self):
        # type: () -> str
        return "FusionClass <>"
