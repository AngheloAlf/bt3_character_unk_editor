#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import functools
import os
import sys
try:
    import GuiManager
    import CharacterUnkParser
    import SubMenu
    import StatMenu
    import LanguageManager
    import Constants
    import UnkGuiGenerator
    import OptionsManager

    import Tkinter as tk
    import ttk
except Exception:
    import packages.GuiManager as GuiManager
    import packages.CharacterUnkParser as CharacterUnkParser
    import packages.SubMenu as SubMenu
    import packages.StatMenu as StatMenu
    import packages.LanguageManager as LanguageManager
    import packages.Constants as Constants
    import packages.UnkGuiGenerator as UnkGuiGenerator
    import packages.OptionsManager as OptionsManager

    import tkinter as tk
    from tkinter import ttk

    unicode = str


class CharacterData:
    def __init__(self):
        self.data = None


def updateTransObject():
    # type: () -> None
    language = LanguageManager.LanguageManager(conf[u"language"])
    for i in range(4):
        a = gui.comboboxs["trans"][i].get()
        a = language.getCharactersNamesID(unicode(a))

        b = gui.comboboxs["barras"][i].current()

        c = gui.comboboxs["ani"][i].get()
        c = language.getAnimationsID(unicode(c))

        d = gui.comboboxs["aura"][i].get()
        d = language.getAurasID(unicode(d))

        e = gui.comboboxs["absor"][i].get()
        e = language.getCharactersNamesID(unicode(e))

        character.data.transObj.setTransformData(i, [a, b, c, d, e], True)

    r3 = gui.comboboxs["R3"][0].get()
    r3 = language.getR3CommandID(unicode(r3))
    character.data.transObj.setR3Command(r3, True)

    bonus = gui.comboboxs["bonus"][0].get()
    bonus = language.getTransformationBonusID(unicode(bonus))
    character.data.transObj.setBonus(bonus, True)

    language.close()
    return


def updateFusObject():
    # type: () -> None
    language = LanguageManager.LanguageManager(conf[u"language"])

    for i in range(3):
        fusBarras = gui.comboboxs["fusBarras"][i].current()

        fusTypeSelected = gui.comboboxs["fusType"][i].get()
        fusTypeID = language.getFusionsTypesID(unicode(fusTypeSelected))

        fusResulSelected = gui.comboboxs["fusResul"][i].get()
        fusResulID = language.getCharactersNamesID(unicode(fusResulSelected))

        fusCompaSelected = gui.comboboxs["fusCompa"][i].get()
        fusCompaID = language.getCharactersNamesID(unicode(fusCompaSelected))

        fusionData = [fusBarras, fusTypeID, fusResulID, fusCompaID]

        for j in gui.comboboxs["fusEquipo"][i]:
            fusionData.append(language.getCharactersNamesID(unicode(j.get())))

        character.data.fusionObj.setFusionData(i, fusionData, True)

    language.close()
    return


def updateMenusObject():
    # type: () -> None
    for i in range(Constants.AmountConst().languagesAmount):
        j0 = 0
        subMenuLoop = character.data.menusList[i].subMenus
        for j in range(Constants.AmountConst().menusAmount):
            if gui.checkbuttons["menuOn"][i][j].is_checked():
                # if j < len(subMenuLoop):
                nombreMenu = unicode(gui.entries["nombreMenu"][i][j].get())

                if j < len(subMenuLoop) and subMenuLoop[j].isNone():
                    raise
                # if not subMenuLoop[j].isNone():

                if j >= len(subMenuLoop):
                    nuevoSubMenu = SubMenu.SubMenu("")
                    subMenuLoop.append(nuevoSubMenu)

                subMenuLoop[j0].setMenuName(nombreMenu)
                subMenuLoop[j0].setMenuNum(j0)
                stats = subMenuLoop[j0].stats
                k0 = 0
                for k in range(Constants.AmountConst().statsAmount):
                    if gui.checkbuttons["addStat"][i][j][k].is_checked():
                        nombrestat = unicode(gui.entries["nombreStat"][i][j][k].get())
                        maxPower = gui.checkbuttons["maxPower"][i][j][k].is_checked()
                        barrasKi = gui.comboboxs["barrasKiMenus"][i][j][k].get()
                        reservaKi = gui.comboboxs["reservaKi"][i][j][k].get()

                        if k >= len(stats):
                            statName = [['', '', ''], '']
                            # statChars = [["", ""]]
                            statChars = []
                            nuevoStat = StatMenu.StatMenu(statName, statChars)
                            stats.append(nuevoStat)

                        stats[k0].setName(nombrestat)
                        stats[k0].setMaxPower(maxPower)
                        stats[k0].setBarrasKi(barrasKi)
                        stats[k0].setReservaKi(reservaKi)
                        k0 += 1
                del stats[k0:]

                j0 += 1
        del subMenuLoop[j0:]
    return


def parseUnkFile(fileName):
    # type: (unicode) -> None
    if not fileName:
        return
    character.data = CharacterUnkParser.CharacterUnkParser(fileName)
    gui.clean()

    try:
        character.data.parse()
        try:
            updateTransTab()
            updateFusionsTab()
            updateMenusTab()
        except Exception as err:
            print(err)
            GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado al mostrar los datos.")
            raise
    except Exception as err:
        print(err)
        character.data = None
        GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado leyendo el archivo.")
        raise


def popData(data):
    # type: (list) -> None
    pop = tk.Toplevel()
    for i in range(8):

        entry1 = ttk.Entry(pop)
        entry1.grid(row=i, column=0)
        entry2 = ttk.Entry(pop, width=50)
        entry2.grid(row=i, column=1)
        if i < len(data):
            if data[i][0] == u'!F%':
                entry1.insert("end", data[i][0] + data[i][1][0])
                entry2.insert("end", data[i][1][1:])
            else:
                entry1.insert("end", data[i][0])
                entry2.insert("end", data[i][1])
        entry1["state"] = "disabled"
        entry2["state"] = "disabled"


def updateTransTab():
    # type: () -> None
    language = LanguageManager.LanguageManager(conf[u"language"])
    for i in range(4):
        transformData = character.data.transObj.getTransformData(i, True)

        char = language.getCharactersNamesPos(transformData[0])
        gui.comboboxs["trans"][i].current(char)
        gui.comboboxs["trans"][i]["state"] = "readonly"

        gui.comboboxs["barras"][i].current(transformData[1])
        gui.comboboxs["barras"][i]["state"] = "readonly"

        ani = language.getAnimationsPos(transformData[2])
        gui.comboboxs["ani"][i].current(ani)
        gui.comboboxs["ani"][i]["state"] = "readonly"

        aura = language.getAurasPos(transformData[3])
        gui.comboboxs["aura"][i].current(aura)
        gui.comboboxs["aura"][i]["state"] = "readonly"

        absor = language.getCharactersNamesPos(transformData[4])
        gui.comboboxs["absor"][i].current(absor)
        if transformData[2] == 3:
            gui.comboboxs["absor"][i]["state"] = "readonly"
        else:
            gui.comboboxs["absor"][i]["state"] = "disabled"

    r3 = character.data.transObj.getR3Command(True)
    r3 = language.getR3CommandPos(r3)
    gui.comboboxs["R3"][0].current(r3)
    gui.comboboxs["R3"][0]["state"] = "readonly"

    bonus = character.data.transObj.getBonus(True)
    bonus = language.getTransformationBonusPos(bonus)
    gui.comboboxs["bonus"][0].current(bonus)
    gui.comboboxs["bonus"][0]["state"] = "readonly"
    language.close()
    print(u"Datos de pestaña 'Transformaciones' lista")
    return


def updateFusionsTab():
    language = LanguageManager.LanguageManager(conf[u"language"])
    for i in range(3):
        fusionData = character.data.fusionObj.getFusionData(i, True)

        gui.comboboxs["fusBarras"][i].current(fusionData[0])
        gui.comboboxs["fusBarras"][i]["state"] = "readonly"

        fusType = language.getFusionsTypesPos(fusionData[1])
        gui.comboboxs["fusType"][i].current(fusType)
        gui.comboboxs["fusType"][i]["state"] = "readonly"

        fusResul = language.getCharactersNamesPos(fusionData[2])
        gui.comboboxs["fusResul"][i].current(fusResul)
        gui.comboboxs["fusResul"][i]["state"] = "readonly"

        fusCompa = language.getCharactersNamesPos(fusionData[3])
        gui.comboboxs["fusCompa"][i].current(fusCompa)
        gui.comboboxs["fusCompa"][i]["state"] = "readonly"

        for j in range(4):
            fusEquipo = language.getCharactersNamesPos(fusionData[4 + j])
            gui.comboboxs["fusEquipo"][i][j].current(fusEquipo)
            gui.comboboxs["fusEquipo"][i][j]["state"] = "readonly"
    language.close()
    print(u"Datos de pestaña 'Fusiones' lista")


def updateMenusTab():
    i = 0
    for menu in character.data.menusList:
        if menu.isKnow():
            if i >= len(gui.entries["nombreMenu"]):
                print(u"ERROR: Mas idiomas de lo esperado")
                break

            j = 0
            for submenu in menu.subMenus:
                if not submenu.isNone():
                    if j >= len(gui.entries["nombreMenu"][i]):
                        print(u"ERROR: Mas menus de lo esperado")
                        break

                    menuName = submenu.getMenuName()

                    gui.entries["nombreMenu"][i][j]["state"] = "normal"
                    gui.entries["nombreMenu"][i][j].delete(0, "end")
                    gui.entries["nombreMenu"][i][j].insert("end", menuName)

                    gui.checkbuttons["menuOn"][i][j].select()

                    k, k0 = 0, 0
                    statsInesperados = False
                    for stat in submenu.stats:
                        if k >= len(gui.entries["nombreStat"][i][j]):
                            statsInesperados = True
                            k += 1
                            continue
                        statName = stat.getName()

                        gui.entries["nombreStat"][i][j][k]["state"] = "normal"
                        gui.entries["nombreStat"][i][j][k].delete(0, "end")
                        gui.entries["nombreStat"][i][j][k].insert("end", statName)
                        # entries["nombreStat"][i][j][k]["state"] = "disabled"

                        gui.checkbuttons["addStat"][i][j][k].select()
                        # gui.checkbuttons["addStat"][i][j][k]["state"] = "normal"

                        if stat.getMaxPower():
                            gui.checkbuttons["maxPower"][i][j][k].select()
                        else:
                            gui.checkbuttons["maxPower"][i][j][k].deselect()
                        gui.checkbuttons["maxPower"][i][j][k]["state"] = "normal"

                        gui.comboboxs["barrasKiMenus"][i][j][k].current(int(stat.getBarrasKi()))
                        gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "readonly"

                        gui.comboboxs["reservaKi"][i][j][k].current(int(stat.getReservaKi()))
                        gui.comboboxs["reservaKi"][i][j][k]["state"] = "readonly"

                        gui.buttons["showData"][i][j][k]["command"] = functools.partial(popData, stat.getStatChars())
                        gui.buttons["showData"][i][j][k]["state"] = "normal"

                        k += 1
                        k0 += 1
                    while k0 < Constants.AmountConst().statsAmount:
                        # gui.checkbuttons["addStat"][i][j][k0]["state"] = "normal"
                        gui.checkbuttons["addStat"][i][j][k0].deselect()
                        gui.checkbuttons["maxPower"][i][j][k0].deselect()
                        gui.buttons["showData"][i][j][k0]["state"] = "disabled"
                        gui.checkbuttons["maxPower"][i][j][k0]["state"] = "disabled"
                        gui.buttons["showData"][i][j][k0]["command"] = functools.partial(popData, list())
                        gui.buttons["showData"][i][j][k0]["state"] = "disabled"
                        k0 += 1
                    if statsInesperados:
                        print(u"Error: Mas stats que los esperados:", k)
                    j += 1
            i += 1
    for i in range(Constants.AmountConst().languagesAmount):
        for j in range(Constants.AmountConst().menusAmount):
            gui.checkbuttons["menuOn"][i][j]["state"] = "normal"
            for k in range(Constants.AmountConst().statsAmount):
                gui.checkbuttons["addStat"][i][j][k]["state"] = "normal"

    print(u"Datos de pestaña 'Menús' lista")
    return


def openFileCaller():
    GuiManager.openFile(u"Abrir archivo", Constants.ProgramConst().FileTypes, parseUnkFile)


def saveFile():
    # type () -> None
    if character.data:
        updateTransObject()
        updateFusObject()
        updateMenusObject()
        try:
            character.data.saveFile()
            GuiManager.popupInfo(u"Accion completada.", u"Archivo actualizado correctamente.")
        except Exception as err:
            print(err)
            text1 = u"Acción fallida."
            text2 = u"Ha ocurrido un error inesperado. Su archivo no ha sido modificado."
            GuiManager.popupError(text1, text2)
            raise
    else:
        GuiManager.popupWarning(u"Acción fallida.", u"Debe abrir un archivo primero.")
    return


def saveAsUnkFile(fileName):
    # type: (unicode) -> None
    if not fileName:
        return
    if not fileName.lower().endswith(".unk"):
        fileName = fileName + ".unk"
    try:
        updateTransObject()
        updateFusObject()
        updateMenusObject()
        character.data.saveFile(fileName)
        GuiManager.popupInfo(u"Accion completada", u"Archivo " + fileName + u" guardado satisfactoriamente")
    except Exception as err:
        print(err)
        GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado.\nSu archivo no ha sido guardado.")
        raise
    return


def saveAsUnkFileCaller():
    if character.data:
        GuiManager.saveFile(u"Guardar archivo", Constants.ProgramConst().FileTypes, saveAsUnkFile)
    else:
        GuiManager.popupWarning(u"Acción fallida", u"Debe abrir un archivo primero.")


def updateMultiplesUnkFiles(archivos):
    # type: (list) -> None
    if not archivos:
        return
    updateTransObject()
    updateFusObject()
    updateMenusObject()
    try:
        for arch in archivos:
            print( (arch, ) )
            personaje = CharacterUnkParser.CharacterUnkParser(arch)
            personaje.parse()
            personaje.saveFile(src=character.data)
        GuiManager.popupInfo(u"Acción completada", u"Archivos actualizados satisfactoriamente")
    except Exception as err:
        print(err)
        texto = u"Ha ocurrido un error inesperado.\nQuizas intentaste actualizar un archivo que no es de personaje."
        GuiManager.popupError(u"Acción fallida", texto)
        # raise


def updateMultiplesUnkFilesCaller():
    # type: () -> None
    if character.data:
        GuiManager.selectMultiplesFiles(u"Seleccionar archivos", Constants.ProgramConst().FileTypes,
                                        updateMultiplesUnkFiles)
    else:
        GuiManager.popupWarning(u"Acción fallida", u"Debe abrir un archivo primero.")


def openFolderCaller():
    # type: () -> None
    GuiManager.selectFolder(u"Selecciona carpeta de archivos 'unk' de personajes.")


def WIP():
    # type: () -> None
    GuiManager.popupInfo(u"WIP", u"Work in progress.")
    return


def optionsCaller():
    # type: () -> None
    if subGui[0] and subGui[0].isRunning():
        subGui[0].stop()
    else:
        subGui[0] = GuiManager.GuiManager(u"Opciones", icon)
    subGui[0].addTab(u"Opciones", functools.partial(UnkGuiGenerator.optionsTab, conf=conf))
    subGui[0].start(u"Opciones")
    return


def about():
    # type: () -> None
    titulo = u"Acerca de"
    texto = u"BT3 Character 'unk' Editor v" + Constants.ProgramConst().Version + u".\nCreado por AngheloAlf"
    GuiManager.popupInfo(titulo, texto)
    return


def onMainClose():
    # type: () -> None
    if subGui[0] and subGui[0].isRunning():
        subGui[0].quit()
    gui.quit()
    return


title = Constants.ProgramConst().Title + u" v" + Constants.ProgramConst().Version
print(title)
character = CharacterData()
print(u"Cargando opciones...")
conf = OptionsManager.OptionsManager(u"options.ini")
print(u"Inicializando interfaz...")
icon = os.path.join(u"resources", u"icon.ico")
gui = GuiManager.GuiManager(title, icon=icon)
subGui = [None]


def main():
    while True:
        language = LanguageManager.LanguageManager(conf[u"language"])

        # languageData
        mainmenu_file = language.getLanguageData(u"mainmenu_file")
        mainmenu_options = language.getLanguageData(u"mainmenu_options")
        mainmenu_help = language.getLanguageData(u"mainmenu_help")
        mainmenu_open = language.getLanguageData(u"mainmenu_open")
        mainmenu_save = language.getLanguageData(u"mainmenu_save")
        mainmenu_save_as = language.getLanguageData(u"mainmenu_save_as")
        mainmenu_select_unks = language.getLanguageData(u"mainmenu_select_unks")
        mainmenu_select_unks_folder = language.getLanguageData(u"mainmenu_select_unks_folder")
        mainmenu_quit = language.getLanguageData(u"mainmenu_quit")
        mainmenu_language = language.getLanguageData(u"mainmenu_language")
        mainmenu_about = language.getLanguageData(u"mainmenu_about")
        tab_transformations = language.getLanguageData(u"tab_transformations")
        tab_fusions = language.getLanguageData(u"tab_fusions")
        tab_menus = language.getLanguageData(u"tab_menus")

        language.close()

        print(u"Preparando menú superior...")
        cascadeNames = [mainmenu_file, mainmenu_options, mainmenu_help]
        cascadeData = [
            [
                (mainmenu_open, openFileCaller),
                (mainmenu_save, saveFile),
                (mainmenu_save_as, saveAsUnkFileCaller),
                (mainmenu_select_unks, updateMultiplesUnkFilesCaller),
                (u"[WIP]"+mainmenu_select_unks_folder, openFolderCaller),
                (None, None),
                (mainmenu_quit, onMainClose)
            ],
            [
                (u"[WIP]"+mainmenu_options, optionsCaller),
                (u"[WIP]Debug", gui.clean)
            ],
            [(mainmenu_about, about)]
        ]
        gui.addMenu(cascadeNames, cascadeData)

        print(u"Preparando pestañas...")
        gui.addTab(tab_transformations, functools.partial(UnkGuiGenerator.addTrans, conf=conf))
        # gui.addTab(tab_transformations, UnkGuiGenerator.addTrans)
        print(u"'Transformaciones' lista.")
        gui.addTab(tab_fusions, functools.partial(UnkGuiGenerator.addFusion, conf=conf))
        # gui.addTab(tab_fusions, UnkGuiGenerator.addFusion)
        print(u"'Fusiones' lista.")
        gui.addTab(tab_menus, functools.partial(UnkGuiGenerator.addMenusTab, conf=conf))
        # gui.addTab(tab_menus, UnkGuiGenerator.addMenusTab)
        print(u"'Menús' lista")
        print(u"Pestañas listas!")

        if len(sys.argv) > 1:
            archivito = unicode(sys.argv[1])
            print(u"\nAbriendo " + archivito + u" ...")
            parseUnkFile(archivito)
            print(u"Archivo abierto correctamente.\n")

        gui.overrideClose(onMainClose)

        print(u"Iniciando interfaz")
        gui.start()

        if not gui.isRestart():
            break

    return
