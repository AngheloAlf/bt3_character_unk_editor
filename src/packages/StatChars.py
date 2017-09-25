#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import packages.Constants as Constants


class StatChars:
    def __init__(self, chars):
        self.type = chars[0]
        self.textType = chars[1][:2]
        if self.type == Constants.CharsTypes().text:
            self.text = chars[1][2:]
        else:
            self.text = chars[1]

    def getUnicodeList(self):
        # type: () -> list
        data = [unicode(self.type, "utf-16")]
        if self.type == Constants.CharsTypes().text:
            data.append(unicode(self.textType + self.text, "utf-16"))
        else:
            data.append(unicode(self.text, "utf-16"))
        return data

    def getAsLine(self):
        # type: () -> str
        endOfLine = Constants.hexListToChar(Constants.FilesConst().endOfLine)
        line = self.type
        if self.type == Constants.CharsTypes().text:
            line += self.textType + self.text
        else:
            line += self.text
        line += endOfLine
        return line
