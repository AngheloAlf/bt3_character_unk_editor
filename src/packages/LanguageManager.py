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
        self.cursor.execute("SELECT * FROM charactersNames")
        return self.cursor.fetchall()

    def getAnimations(self):
        self.cursor.execute("SELECT * FROM animations")
        return self.cursor.fetchall()

    def getAuras(self):
        self.cursor.execute("SELECT * FROM auras")
        return self.cursor.fetchall()

    def getR3Command(self):
        self.cursor.execute("SELECT * FROM r3Command")
        return self.cursor.fetchall()

    def getTransformationBonus(self):
        self.cursor.execute("SELECT * FROM transformationBonus")
        return self.cursor.fetchall()

    def getTransformationBonusID(self, name):
        self.cursor.execute("SELECT id FROM transformationBonus WHERE name='" + name + "'")
        ide = self.cursor.fetchone()[0]
        return ide

    def getR3CommandID(self, name):
        self.cursor.execute("SELECT id FROM r3Command WHERE name='" + name + "'")
        ide = self.cursor.fetchone()[0]
        return ide

    def getTransformationBonusPos(self, ide):
        contador = 0
        for bonusNames in self.getTransformationBonus():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getR3CommandPos(self, ide):
        contador = 0
        for bonusNames in self.getR3Command():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getCharactersNamesPos(self, ide):
        contador = 0
        for bonusNames in self.getCharactersNames():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getAnimationsPos(self, ide):
        contador = 0
        for bonusNames in self.getAnimations():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getAnimationsID(self, name):
        self.cursor.execute("SELECT id FROM animations WHERE name='" + name + "'")
        ide = self.cursor.fetchone()[0]
        return ide

    def getAurasPos(self, ide):
        contador = 0
        for bonusNames in self.getAuras():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getAurasID(self, name):
        self.cursor.execute("SELECT id FROM auras WHERE name='" + name + "'")
        ide = self.cursor.fetchone()[0]
        return ide

    def getFusionsTypes(self):
        self.cursor.execute("SELECT * FROM fusionsTypes")
        return self.cursor.fetchall()

    def getFusionsTypesPos(self, ide):
        contador = 0
        for bonusNames in self.getFusionsTypes():
            if bonusNames[0] == ide:
                return contador
            contador += 1
        return 0

    def getFusionsTypesID(self, name):
        self.cursor.execute("SELECT id FROM fusionsTypes WHERE name='" + name + "'")
        ide = self.cursor.fetchone()[0]
        return ide

    def getCharactersNamesID(self, name):
        self.cursor.execute("SELECT id FROM charactersNames WHERE name='" + name + "'")
        ide = self.cursor.fetchone()[0]
        return ide

    def executeScriptsFromFile(self, filename):
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
        self.connection.close()

if __name__ == "__main__":
    a = LanguageManager("spanish.db")
    # a.executeScriptsFromFile("main.sql")
    print len(a.getCharactersNames())
    print len(a.getAnimations())
    print len(a.getAuras())
    print len(a.getR3Command())
    a.close()
