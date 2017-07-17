import sqlite3
import os


class LanguageManager:
    def __init__(self, dbname):
        self.dbname = dbname
        dbFolder = os.path.join(os.getcwd(), "lang", dbname)
        dbFolder2 = os.path.join(os.getcwd(), "..", "lang", dbname)
        try:
            self.connection = sqlite3.connect(dbFolder)
            self.dbFolder = dbFolder
        except:
            self.connection = sqlite3.connect(dbFolder2)
            self.dbFolder = dbFolder2
        self.cursor = self.connection.cursor()

    def getCharactersNames(self):
        # type: () -> list
        self.cursor.execute("SELECT * FROM charactersNames")
        return self.cursor.fetchall()

    def getAnimations(self):
        # type: () -> list
        self.cursor.execute("SELECT * FROM animations")
        return self.cursor.fetchall()

    def getAuras(self):
        # type: () -> list
        self.cursor.execute("SELECT * FROM auras")
        return self.cursor.fetchall()

    def getR3Command(self):
        # type: () -> list
        self.cursor.execute("SELECT * FROM r3Command")
        return self.cursor.fetchall()

    def getTransformationBonus(self):
        # type: () -> list
        self.cursor.execute("SELECT * FROM transformationBonus")
        return self.cursor.fetchall()

    def getFusionsTypes(self):
        # type: () -> list
        self.cursor.execute("SELECT * FROM fusionsTypes")
        return self.cursor.fetchall()


    def getCharactersNamesID(self, name):
        # type: (str) -> int
        self.cursor.execute("SELECT id FROM charactersNames WHERE name='" + name + "'")
        return self.cursor.fetchone()[0]

    def getAnimationsID(self, name):
        # type: (str) -> int
        self.cursor.execute("SELECT id FROM animations WHERE name='" + name + "'")
        return self.cursor.fetchone()[0]

    def getAurasID(self, name):
        # type: (str) -> int
        self.cursor.execute("SELECT id FROM auras WHERE name='" + name + "'")
        return self.cursor.fetchone()[0]

    def getR3CommandID(self, name):
        # type: (str) -> int
        self.cursor.execute("SELECT id FROM r3Command WHERE name='" + name + "'")
        return self.cursor.fetchone()[0]

    def getTransformationBonusID(self, name):
        # type: (str) -> int
        self.cursor.execute("SELECT id FROM transformationBonus WHERE name='" + name + "'")
        return self.cursor.fetchone()[0]

    def getFusionsTypesID(self, name):
        # type: (str) -> int
        self.cursor.execute("SELECT id FROM fusionsTypes WHERE name='" + name + "'")
        return self.cursor.fetchone()[0]


    def getCharactersNamesPos(self, ide):
        # type: (int) -> int
        contador = 0
        for bonusNames in self.getCharactersNames():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getAnimationsPos(self, ide):
        # type: (int) -> int
        contador = 0
        for bonusNames in self.getAnimations():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getAurasPos(self, ide):
        # type: (int) -> int
        contador = 0
        for bonusNames in self.getAuras():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getR3CommandPos(self, ide):
        # type: (int) -> int
        contador = 0
        for bonusNames in self.getR3Command():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getTransformationBonusPos(self, ide):
        # type: (int) -> int
        contador = 0
        for bonusNames in self.getTransformationBonus():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getFusionsTypesPos(self, ide):
        # type: (int) -> int
        contador = 0
        for bonusNames in self.getFusionsTypes():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0


    def executeScriptsFromFile(self, filename):
        # type: (str) -> None
        # Open and read the file as a single buffer
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        # all SQL commands (split on ';')
        sqlCommands = sqlFile.split(';')

        # Execute every command from the input file
        for command in sqlCommands:
            # This will skip and report errors
            # For example, if the tables do not yet exist, this will skip over
            # the DROP TABLE commands
            try:
                self.cursor.execute(command)
            except:
                print "Command skipped: ", command
        self.connection.commit()

    def close(self):
        # type: () -> None
        self.connection.close()

if __name__ == "__main__":
    a = LanguageManager(os.path.join("..", "..", "..", "lang", "spanish.db"))
    # a.executeScriptsFromFile("main.sql")
    cn = a.getCharactersNames()
    print len(cn)
    an = a.getAnimations()
    print len(an)
    au = a.getAuras()
    print len(au)
    r3 = a.getR3Command()
    print len(r3)
    tb = a.getTransformationBonus()
    print len(tb)
    ft = a.getFusionsTypes()
    print len(ft)
    a.close()
