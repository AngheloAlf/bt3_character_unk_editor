#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from . import Constants


class StatChars:
    def __init__(self, chars):
        # type: (list) -> None
        self.type = chars[0]
        self.textType = chars[1][:2]
        if self.type == Constants.CharsTypes().text:
            self.text = chars[1][2:]
        else:
            self.text = chars[1]

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
        filesConst = Constants.FilesConst()
        endOfLine = filesConst.endOfLine
        line = self.type
        if self.type == Constants.CharsTypes().text:
            line += self.textType + self.text
        else:
            line += self.text
        line += endOfLine
        return line
