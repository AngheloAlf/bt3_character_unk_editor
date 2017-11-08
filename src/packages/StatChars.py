#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from . import Constants


class StatChars:
    def __init__(self, data, printData=False):
        # type: (bytes, bool) -> None
        self.type = data[:6]
        rest = data[6:]
        self.textType = rest[:2]
        if self.type == Constants.CharsTypes().text:
            self.text = rest[2:]
        else:
            self.text = rest
        self.printData = printData
        if self.printData:
            print("\n\t\t\tStatChars:")
            print("\t\t\t\ttype:", self.type, self.type.decode("utf-16"))
            print("\t\t\t\ttextType:", self.textType, self.textType.decode("utf-16"))
            print("\t\t\t\ttext:", self.text, self.text.decode("utf-16"))
        # if b"=\x00" in self.text:
        #     wea = self.text.split(b"=\x00")[1][:-4]
        #     print(wea.decode("utf-16"), len(wea)/2)
        return

    def getUnicodeList(self):
        # type: () -> list
        data = [self.type.decode("utf-16")]
        if self.type == Constants.CharsTypes().text:
            data.append((self.textType + self.text).decode("utf-16"))
        else:
            data.append(self.text.decode("utf-16"))
        return data

    def getAsLine(self):
        # type: () -> bytes
        line = self.type
        if self.type == Constants.CharsTypes().text:
            line += self.textType + self.text
        else:
            line += self.text
        return line
