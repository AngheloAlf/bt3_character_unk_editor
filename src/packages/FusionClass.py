class FusionClass:
    def __init__(self, datos):
        if len(datos) != 24:
            print 1 / 0
        self.barras = list(datos[0:3])
        self.tipoFusion = list(datos[3:6])
        self.resultado = list(datos[6:9])
        self.compaAni = list(datos[9:12])
        self.compaEquipo = [list(datos[12:16]), list(datos[16:20]), list(datos[20:24])]

        print "Fusion:"
        print "barras:", map(lambda x: ord(x), self.barras)
        print "tipoFusion:", map(lambda x: ord(x), self.tipoFusion)
        print "resultado:", map(lambda x: ord(x), self.resultado)
        print "compaAni:", map(lambda x: ord(x), self.compaAni)
        print "compaEquipo", map(lambda x: map(lambda y: ord(y), x), self.compaEquipo)
        print "\n"

    def getFusionData(self, fusionNumb, asOrd=False):
        if fusionNumb < 0 or fusionNumb > 2:
            return None

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
            data = map(lambda x: chr(x), data)

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
