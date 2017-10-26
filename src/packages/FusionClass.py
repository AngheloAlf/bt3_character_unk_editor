from __future__ import print_function


class FusionClass:
    def __init__(self, datos, printData=False):
        # type: (bytes, bool) -> None
        if len(datos) != 24:
            raise TypeError("data len != 24")
        self.barras = datos[0:3]
        self.tipoFusion = datos[3:6]
        self.resultado = datos[6:9]
        self.compaAni = datos[9:12]
        self.compaEquipo = [datos[12:16], datos[16:20], datos[20:24]]

        if printData:
            print(u"Fusion:")
            print(u"barras:", self.barras)
            print(u"tipoFusion:", self.tipoFusion)
            print(u"resultado:", self.resultado)
            print(u"compaAni:", self.compaAni)
            print(u"compaEquipo", self.compaEquipo)
            print(u"\n")

    def getFusionData(self, fusionNumb):
        # type: (int) -> list[int]
        if fusionNumb < 0 or fusionNumb > 2:
            return list()

        data = [self.barras[fusionNumb], self.tipoFusion[fusionNumb], self.resultado[fusionNumb],
                self.compaAni[fusionNumb]]
        data += self.compaEquipo[fusionNumb]

        if type(data[0]) == int:
            return data
        return list(map(ord, data))

    def setFusionData(self, fusionNumb, data):
        # type: (int, list[int]) -> bool
        if fusionNumb < 0 or fusionNumb > 3 or len(data) != 8:
            return False

        for i in range(8):
            j = data[i]
            if j < 0 or j > 255:
                return False

        if type(self.barras[fusionNumb]) != int:
            data = list(map(chr, data))

        if type(data[0]) == int:
            data = [bytes([x]) for x in data]

        self.barras = self.barras[:fusionNumb] + data[0] + self.barras[fusionNumb+1:]
        self.tipoFusion = self.tipoFusion[:fusionNumb] + data[1] + self.tipoFusion[fusionNumb+1:]
        self.resultado = self.resultado[:fusionNumb] + data[2] + self.resultado[fusionNumb+1:]
        self.compaAni = self.compaAni[:fusionNumb] + data[3] + self.compaAni[fusionNumb+1:]
        self.compaEquipo[fusionNumb] = b"".join(data[4:8])

        return True

    def getAsLine(self):
        # type: () -> bytes
        line = self.barras + self.tipoFusion + self.resultado + self.compaAni
        line += b"".join(self.compaEquipo)
        return line

    def __str__(self):
        # type: () -> str
        return "FusionClass <>"
