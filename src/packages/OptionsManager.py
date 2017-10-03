defaults = {u"language": u"spanish.db"}


def writeDefaultOptions(openFile):
    # type: (file) -> None
    for data in defaults.items():
        openFile.write("=".join(data) + "\n")
    return


class OptionsManager:
    def __init__(self, name):
        # type: (str) -> None
        self.name = name
        self.options = dict()
        try:
            opt = open(self.name)
        except IOError:
            opt = open(self.name, "w")
            writeDefaultOptions(opt)
            opt.close()
            opt = open(self.name)
        for line in opt:
            data = line.strip().split("=")
            self.options[data[0]] = data[1]
        opt.close()
        if self.checkOptions():
            self.updateFile()
        return

    def checkOptions(self):
        # type: () -> bool
        dif = False
        for key, value in defaults.items():
            if key not in self.options:
                self.options[key] = value
                dif = True
        return dif

    def updateFile(self):
        # type: () -> None
        opt = open(self.name, "w")
        for item in self.options.items():
            opt.write("=".join(item) + "\n")
        opt.close()
        return

    def __getitem__(self, option):
        # type: (str) -> str
        if str != type(option):
            raise TypeError("Bad type for option", (option, type(option)))
        if option not in self.options:
            raise ValueError("There is no option '"+option+"'", option)
        return self.options[option]

    def __setitem__(self, key, value):
        # type: (str, str) -> None
        if str != type(key) or str != type(value):
            raise TypeError("Bad type for option", (key, type(key)), (value, type(value)))
        else:
            self.options[key] = value
        return
