#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# try:
#     from packages.TransformClass import TransformClass
#     from packages.CharacterUnkParser import CharacterUnkParser
#     from packages.LanguageManager import LanguageManager
#     from packages.GuiManager import GuiManager
#     from packages.UnkEditorGui import *
#     print "import normal"
# except ImportError:
#     from packages import *
#     import packages
#     print "wea"
#     print dir(packages)
#     #print help(packages)
#     print packages.__builtins__
#     print packages.__doc__
#     print packages.__file__
#     print packages.__name__
#     print packages.__package__
#     print packages.__test__
import threading
import os

from TransformClass import TransformClass
from .CharacterUnkParser import CharacterUnkParser
from LanguageManager import LanguageManager
from GuiManager import GuiManager
from UnkEditorGui import *




class CharacterData:
    def __init__(self):
        self.data = None



def comboTransUpdate(event, languageFile="spanish.db"):
    language = LanguageManager(languageFile)
    for i in range(4):
        a = gui.comboboxs["trans"][i].get()
        a = language.getCharactersNamesID(a)

        b = gui.comboboxs["barras"][i].current()

        c = gui.comboboxs["ani"][i].get()
        c = language.getAnimationsID(c)

        d = gui.comboboxs["aura"][i].get()
        d = language.getAurasID(d)

        e = gui.comboboxs["absor"][i].get()
        e = language.getCharactersNamesID(e)

        character.data.transObj.setTransformData(i, [a, b, c, d, e], True)        

        if gui.comboboxs["ani"][i].current() == 3:
            gui.comboboxs["absor"][i]["state"] = "readonly"
        else:
            gui.comboboxs["absor"][i]["state"] = "disabled"


    r3 = gui.comboboxs["R3"].get()
    r3 = language.getR3CommandID(r3)
    character.data.transObj.setR3Command(r3, True)

    bonus = gui.comboboxs["bonus"].get()
    bonus = language.getTransformationBonusID(bonus)
    character.data.transObj.setBonus(bonus, True)

    language.close()
    return

def comboFusUpdate(event, languageFile="spanish.db"):
    language = LanguageManager(languageFile)

    for i in range(3):
        fusBarras = gui.comboboxs["fusBarras"][i].current()

        fusTypeSelected = gui.comboboxs["fusType"][i].get()
        fusTypeID = language.getFusionsTypesID(fusTypeSelected)

        fusResulSelected = gui.comboboxs["fusResul"][i].get()
        fusResulID = language.getCharactersNamesID(fusResulSelected)

        fusCompaSelected = gui.comboboxs["fusCompa"][i].get()
        fusCompaID = language.getCharactersNamesID(fusCompaSelected)

        fusionData = [fusBarras, fusTypeID, fusResulID, fusCompaID]

        if event and event.widget == gui.comboboxs["fusCompa"][i]:
            gui.comboboxs["fusEquipo"][i][0].current(gui.comboboxs["fusCompa"][i].current())

        for j in gui.comboboxs["fusEquipo"][i]:
            fusionData.append(language.getCharactersNamesID(j.get()))

        character.data.fusionObj.setFusionData(i, fusionData, True)

    language.close()
    return

def menusUpdate(event, languageFile="spanish.db"):
    language = LanguageManager(languageFile)
    for i in range(8):
        for j in range(7):
            #print gui.entries["nombreMenu"][i][j].get()
            subMenuLoop = character.data.menusList[i].subMenus
            if j < len(subMenuLoop):
                if not subMenuLoop[j].isNone():
                    subMenuLoop[j].setMenuName(gui.entries["nombreMenu"][i][j].get())
            for k in range(24):
                if gui.checkbuttons["addStat"][i][j][k].is_checked():
                    a = gui.entries["nombreStat"][i][j][k].get()
                    subMenuLoop[j].stats[k].setName(a)

                    maxPower = gui.checkbuttons["maxPower"][i][j][k].is_checked()
                    subMenuLoop[j].stats[k].setMaxPower(str(maxPower))

                    barrasKi = gui.comboboxs["barrasKiMenus"][i][j][k].get()
                    subMenuLoop[j].stats[k].setBarrasKi(barrasKi)

                    reservaKi = gui.comboboxs["reservaKi"][i][j][k].get()
                    subMenuLoop[j].stats[k].setReservaKi(reservaKi)
    language.close()
    return

def parseUnkFile(fileName, comboboxs=None, entries=None, checkbuttons=None, buttons=None, languageFile="spanish.db"):
    if not fileName:
        return
    character.data = CharacterUnkParser(fileName)
    if comboboxs or entries or checkbuttons or buttons:
        #character.data.parse(gui)
        #language = LanguageManager(languageFile)
        threading.Thread(target=updateGui, args=[comboboxs, entries, checkbuttons, buttons]).start()
        #trans = threading.Thread(target=updateTransformations, args=[comboboxs, entries, checkbuttons, buttons])
        #fus = threading.Thread(target=updateFusions, args=[comboboxs, entries, checkbuttons, buttons])
        #men = threading.Thread(target=updateMenus, args=[comboboxs, entries, checkbuttons, buttons])
        #trans.start()
        #fus.start()
        #men.start()
        #threading.Thread(target=threadsStop, args=[trans, fus, men]).start()
    
def threadsStop(*args):
    while True:
        a = 0
        for i in args:
            if not i.isAlive():
                a += 1
        if a == len(args):
            break
    print "ready"

def popData(data):
    pop = Tkinter.Toplevel()
    for i in range(7):

        entry1 = ttk.Entry(pop)
        entry1.grid(row=i, column=0)
        entry2 = ttk.Entry(pop, width=50)
        entry2.grid(row=i, column=1)
        if i < len(data):
            if data[i][0] == u'!F%':
                entry1.insert("end", data[i][0]+data[i][1][0])
                entry2.insert("end", data[i][1][1:])
            else:
                entry1.insert("end", data[i][0])
                entry2.insert("end", data[i][1])
        entry1["state"]="disabled"
        entry2["state"]="disabled"

def updateTransformations(comboboxs, entries, checkbuttons, buttons, languageFile="spanish.db"):
    language = LanguageManager(languageFile)
    for i in range(4):
        transformData = character.data.transObj.getTransformData(i, True)

        char = language.getCharactersNamesPos(transformData[0])
        comboboxs["trans"][i].current(char)
        comboboxs["trans"][i]["state"] = "readonly"

        comboboxs["barras"][i].current(transformData[1])
        comboboxs["barras"][i]["state"] = "readonly"
        
        ani = language.getAnimationsPos(transformData[2])
        comboboxs["ani"][i].current(ani)
        comboboxs["ani"][i]["state"] = "readonly"
        
        aura = language.getAurasPos(transformData[3])
        comboboxs["aura"][i].current(aura)
        comboboxs["aura"][i]["state"] = "readonly"
        
        absor = language.getCharactersNamesPos(transformData[4])
        comboboxs["absor"][i].current(absor)
        if transformData[2] == 3:
            comboboxs["absor"][i]["state"] = "readonly"
        else:
            comboboxs["absor"][i]["state"] = "disabled"

    r3 = character.data.transObj.getR3Command(True)
    r3 = language.getTransformationBonusPos(r3)
    comboboxs["R3"].current(r3)
    comboboxs["R3"]["state"] = "readonly"

    bonus = character.data.transObj.getBonus(True)
    bonus = language.getTransformationBonusPos(bonus)
    comboboxs["bonus"].current(bonus)
    comboboxs["bonus"]["state"] = "readonly"
    language.close()
    print "trans ready"

def updateFusions(comboboxs, entries, checkbuttons, buttons, languageFile="spanish.db"):
    language = LanguageManager(languageFile)
    for i in range(3):
        fusionData = character.data.fusionObj.getFusionData(i, True)

        comboboxs["fusBarras"][i].current(fusionData[0])
        comboboxs["fusBarras"][i]["state"] = "readonly"

        fusType = language.getFusionsTypesPos(fusionData[1])
        comboboxs["fusType"][i].current(fusType)
        comboboxs["fusType"][i]["state"] = "readonly"

        fusResul = language.getCharactersNamesPos(fusionData[2])
        comboboxs["fusResul"][i].current(fusResul)
        comboboxs["fusResul"][i]["state"] = "readonly"

        fusCompa = language.getCharactersNamesPos(fusionData[3])
        comboboxs["fusCompa"][i].current(fusCompa)
        comboboxs["fusCompa"][i]["state"] = "readonly"

        for j in range(4):
            fusEquipo = language.getCharactersNamesPos(fusionData[4+j])
            comboboxs["fusEquipo"][i][j].current(fusEquipo)
            comboboxs["fusEquipo"][i][j]["state"] = "readonly"
    language.close()
    print "fus ready"

def updateMenus(comboboxs, entries, checkbuttons, buttons, languageFile="spanish.db"):
    language = LanguageManager(languageFile)
    debug = dict()
    i = 0
    for menu in character.data.menusList:
        if menu.isKnow():
            #print unicode(menu.getAsLine(), "utf-16")
            if i >= len(entries["nombreMenu"]):
                print "ERROR: Mas idiomas de lo esperado"
                break

            j = 0
            for submenu in menu.subMenus:
                if not submenu.isNone():
                    if j >= len(entries["nombreMenu"][i]):
                        print "ERROR: Mas menus de lo esperado"
                        break

                    menuNum = int(submenu.getMenuNum())
                    menuName = submenu.getMenuName()
                    #print unicode(submenu.getAsLine(), "utf-16")

                    # print menuNum, menuName

                    entries["nombreMenu"][i][j]["state"] = "normal"
                    entries["nombreMenu"][i][j].delete(0, "end")
                    entries["nombreMenu"][i][j].insert("end", menuName)
                    #entries["nombreMenu"][i][j]["state"] = "disabled"

                    if menuNum<7:
                        comboboxs["dragonballIcon"][i][j].current(menuNum)
                    else:
                        comboboxs["dragonballIcon"][i][j]["value"] = list(comboboxs["dragonballIcon"][i][j]["value"]) + [menuNum]
                        comboboxs["dragonballIcon"][i][j].current(len(comboboxs["dragonballIcon"][i][j]["value"])-1)
                        comboboxs["dragonballIcon"][i][j]["state"] = "disabled"


                    k, k0 = 0, 0
                    statsInesperados = False
                    for stat in submenu.stats:
                        if k >= len(entries["nombreStat"][i][j]):
                            statsInesperados = True
                            k += 1
                            continue
                        #print unicode(stat.getAsLine(), "utf-16")
                        statName = stat.getName()
                        statData = stat.getStatData()

                        entries["nombreStat"][i][j][k]["state"] = "normal"
                        entries["nombreStat"][i][j][k].delete(0, "end")
                        entries["nombreStat"][i][j][k].insert("end", statName)
                        #entries["nombreStat"][i][j][k]["state"] = "disabled"

                        checkbuttons["addStat"][i][j][k].select()

                        if int(stat.getMaxPower()):
                            checkbuttons["maxPower"][i][j][k].select()
                        else:
                            checkbuttons["maxPower"][i][j][k].deselect()
                        checkbuttons["maxPower"][i][j][k]["state"] = "normal"

                        comboboxs["barrasKiMenus"][i][j][k].current(int(stat.getBarrasKi()))
                        comboboxs["barrasKiMenus"][i][j][k]["state"] = "readonly"

                        comboboxs["reservaKi"][i][j][k].current(int(stat.getReservaKi()))
                        comboboxs["reservaKi"][i][j][k]["state"] = "readonly"


                        buttons["showData"][i][j][k]["command"] = functools.partial(popData, stat.getStatChars())
                        buttons["showData"][i][j][k]["state"] = "normal"
                        #for debugeando in stat.getStatChars():
                        #    if debugeando[0] not in debug:
                        #        debug[debugeando[0]] = set()
                        #    debug[debugeando[0]].add(debugeando[1][0])
                        #print len(stat.getStatChars())
                        #if len(stat.getStatChars())>5:
                        #    print "WEA"


                        k += 1
                        k0 += 1
                    while k0 < 24:
                        checkbuttons["addStat"][i][j][k].deselect()
                        checkbuttons["maxPower"][i][j][k].deselect()
                        buttons["showData"][i][j][k]["state"] = "disabled"
                        k0 += 1
                    if statsInesperados:
                        print "Error: Mas stats que los esperados:", k
                    j += 1
            i += 1
    language.close()
    print "menus ready"

def updateGui(comboboxs, entries, checkbuttons, buttons, languageFile="spanish.db"):
    character.data.parse(gui)
    trans = threading.Thread(target=updateTransformations, args=[comboboxs, entries, checkbuttons, buttons])
    fus = threading.Thread(target=updateFusions, args=[comboboxs, entries, checkbuttons, buttons])
    men = threading.Thread(target=updateMenus, args=[comboboxs, entries, checkbuttons, buttons])
    trans.start()
    fus.start()
    men.start()
    threading.Thread(target=threadsStop, args=[trans, fus, men]).start()
    print "Ready"
    return

def saveFile():
    comboTransUpdate(None)
    comboFusUpdate(None)
    menusUpdate(None)
    threading.Thread(target = lambda: character.data.saveFile(gui=gui), args=[]).start()

def saveAsUnkFile(fileName, **kwargs):
    if not fileName:
        return
    comboTransUpdate(None)
    comboFusUpdate(None)
    menusUpdate(None)
    threading.Thread(target = character.data.saveFile, args=[fileName, gui]).start()




# a = CharacterUnkParser("koku.unk")
# a.parse()
# print [str(a)]
# print [str(a.menusList[3])]
# print [str(a.menusList[3].subMenus[5])]
# print [str(a.menusList[3].subMenus[5].stats[0])]

# stats = a.menusList[3].subMenus[5].stats
# for i in stats:
#     print unicode(i.name[1], "UTF-16")
#     for j in i.statChars:
#         print "\t", unicode(j[1], "UTF-16")

character = CharacterData()
gui = GuiManager("BT3 Character 'unk' Editor")

def main():
    while True:
        fileTypes = (("Archivos 'unk' de personajes", "*.unk"), ("Todos los archivos",  "*,*"))
        menuAbrir = lambda: gui.openFile("Abrir archivo", fileTypes, parseUnkFile)
        menuGuardar = lambda: saveFile()
        menuGuardarComo = lambda: gui.saveFile("Guardar archivo", fileTypes, saveAsUnkFile)
        menuMuchos = lambda: gui.openMultiplesFiles("Seleccionar archivos", fileTypes)
        menuCarpeta = lambda: gui.selectFolder("Selecciona carpeta de archivos 'unk' de personajes.")
        menuAcercaDe = lambda: gui.popUp("Acerca de", "Informacion", "Ok")

        print 3
        gui.addMenu(["Archivo", "Opciones", "Ayuda"], 
            [
            [("Abrir", menuAbrir), ("Guardar", menuGuardar), ("Guardar como...", menuGuardarComo), ("[WIP]Actualizar muchos", menuMuchos), ("[WIP]Actualizar en capeta", menuCarpeta), (None, None), ("Salir", gui.gui.quit)], 
            [("[WIP]Idioma", lambda: None)],
            [("Acerca de", menuAcercaDe)]
            ])

        print 4
        gui.addTab("Transformaciones", addTrans)
        gui.addTab("Fusiones", addFusion)
        gui.addTab("Menus", addMenusTab)
        gui.putProgressBar(20)
        print 5
        gui.start()

        if not gui.isRestart():
            break
