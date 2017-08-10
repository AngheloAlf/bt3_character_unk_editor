#!/usr/local/bin/python
# -*- coding: utf-8 -*-


menuNameCode = [0x21, 0x00, 0x46, 0x00, 0x24, 0x00]
endOfLine = [0x0a, 0x00]

statCode = [0x21, 0x00, 0x46, 0x00, 0x2A, 0x00]

numberSign = [0x23, 0x00]

transformCode = [0xa0, 0x86, 0x01, 0x00]

startOfMenuFile = [0xFF, 0xFE, 0x21, 0x00]
endOfMenuFile = [0x46, 0x00, 0x40, 0x00]

endOfFile = [0x21, 0x00, 0x46, 0x00, 0x40, 0x00]

startOfutf16Text = [0xFF, 0xFE]

Title = u"BT3 Character 'unk' Editor"
Version = u"0.2.0-beta"

FileTypes = ((u"Archivos 'unk' de personajes", u"*.unk"), (u"Todos los archivos", u"*.*"))

statsAmount = 32
menusAmount = 7
languagesAmount = 8

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
