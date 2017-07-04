#!/usr/local/bin/python
# -*- coding: utf-8 -*-


class Constants:
    def __init__(self):
        pass

    menuNameCode = [0x21, 0x00, 0x46, 0x00, 0x24, 0x00]
    endOfLine = [0x0a, 0x00]

    statCode = [0x21, 0x00, 0x46, 0x00, 0x2A, 0x00]

    numberSign = [0x23, 0x00]

    transformCode = [0xa0, 0x86, 0x01, 0x00]

    startOfMenuFile = [0xFF, 0xFE, 0x21, 0x00]
    endOfMenuFile = [0x46, 0x00, 0x40, 0x00]

    endOfFile = [0x21, 0x00, 0x46, 0x00, 0x40, 0x00]

    startOfutf16Text = [0xFF, 0xFE]

    # u'!1#' <PAD=Ｌ２＋○>
    # u'!2#' <PAD=†上＋†振縦>
    # u'!8#' <PAD=Ｒ１＋○>
    # u'!4#' <PAD=Ｌ１＋○>

    # u'!F%' 0Partner: Goku (End) / 1Chargeable
    # u'!D#' <PAD=□△♂>


def hexListToChar(hexList):
    return "".join(map(lambda x: chr(x), hexList))
