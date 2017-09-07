#!/usr/local/bin/python
# -*- coding: utf-8 -*-


class FilesConst:
    def __init__(self):
        self.menuNameCode = [0x21, 0x00, 0x46, 0x00, 0x24, 0x00]
        self.endOfLine = [0x0a, 0x00]

        self.statCode = [0x21, 0x00, 0x46, 0x00, 0x2A, 0x00]

        # numberSign = [0x23, 0x00]

        self.transformCode = [0xa0, 0x86, 0x01, 0x00]

        self.startOfMenuFile = [0xFF, 0xFE, 0x21, 0x00]
        self.endOfMenuFile = [0x46, 0x00, 0x40, 0x00]

        self.endOfFile = [0x21, 0x00, 0x46, 0x00, 0x40, 0x00]

        self.startOfutf16Text = [0xFF, 0xFE]


class ProgramConst:
    def __init__(self):
        self.Title = u"BT3 Character 'unk' Editor"
        self.Version = u"0.2.0-beta"
        self.FileTypes = ((u"Archivos 'unk' de personajes", u"*.unk"), (u"Todos los archivos", u"*.*"))


class AmountConst:
    def __init__(self):
        self.statsAmount = 32
        self.menusAmount = 7
        self.languagesAmount = 8


class CharsTypes:
    def __init__(self):
        self.text = "!\x00F\x00%\x00"
        self.unknown1 = "!\x001\x00#\x00"
        self.unknown2 = "!\x002\x00#\x00"
        self.unknown8 = "!\x008\x00#\x00"
        self.unknown4 = "!\x004\x00#\x00"
        self.unknownD = "!\x00D\x00#\x00"

        # u'!1#' <PAD=Ｌ２＋○>
        # u'!2#' <PAD=†上＋†振縦>
        # u'!8#' <PAD=Ｒ１＋○>
        # u'!4#' <PAD=Ｌ１＋○>

        # u'!F%' 0Partner: Goku (End) / 1Chargeable
        # u'!D#' <PAD=□△♂>


def hexListToChar(hexList):
    # type: (list) -> str
    return "".join(map(chr, hexList))


def findDataPos(archivo, data, maxi=-1, inicio=0, tope=-1):
    # type: (str, str, int, int, int) -> list
    i = 0
    l = list()
    while i < maxi or maxi == -1:
        if tope > 0:
            finded = archivo.find(data, inicio, tope)
        else:
            finded = archivo.find(data, inicio)
        if finded == -1:
            break
        l.append(finded)
        i += 1
        inicio = finded+1
    return l
