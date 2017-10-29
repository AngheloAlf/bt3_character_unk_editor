#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import functools
import os
import sys

from . import GuiManager
from . import CharacterUnkParser
from . import SubMenu
from . import StatMenu
from . import LanguageManager
from . import Constants
from . import UnkGuiGenerator
from . import OptionsManager


def WIP():
    # type: () -> None
    GuiManager.popupInfo(u"WIP", u"Work in progress.")
    return


class UnkEditor:
    def __init__(self, confName=u"options.ini"):
        # type: (str) -> None
        self.title = Constants.ProgramConst().Title + u" v" + Constants.ProgramConst().Version
        print(self.title)
        self.unkData = None

        print(u"Cargando opciones...")
        self.conf = OptionsManager.OptionsManager(confName)

        print(u"Inicializando interfaz...")
        self.icon = os.path.join(u"resources", u"icon.ico")
        self.gui = GuiManager.GuiManager(self.title, icon=self.icon)
        self.subGui = None
        return

    def start(self):
        # type: () -> bool
        language = LanguageManager.LanguageManager(self.conf["language"])

        print(u"Cargando idioma...")
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
                (mainmenu_open, self.openFileCaller),
                (mainmenu_save, self.saveFile),
                (mainmenu_save_as, self.saveAsUnkFileCaller),
                (mainmenu_select_unks, self.updateMultiplesUnkFilesCaller),
                (u"[WIP]" + mainmenu_select_unks_folder, self.openFolderCaller),
                (None, None),
                (mainmenu_quit, self.onMainClose)
            ],
            [
                (u"[WIP]" + mainmenu_options, self.optionsCaller),
                (u"[WIP]Debug", self.debugMain)
            ],
            [(mainmenu_about, self.about)]
        ]
        self.gui.addMenu(cascadeNames, cascadeData)

        print(u"Preparando pestañas...")
        addTrans = UnkGuiGenerator.addTrans
        self.gui.addTab(tab_transformations, functools.partial(addTrans, conf=self.conf))
        print(u"'Transformaciones' lista.")
        addFusion = UnkGuiGenerator.addFusion
        self.gui.addTab(tab_fusions, functools.partial(addFusion, conf=self.conf))
        print(u"'Fusiones' lista.")
        addMenusTab = UnkGuiGenerator.addMenusTab
        self.gui.addTab(tab_menus, functools.partial(addMenusTab, conf=self.conf))
        print(u"'Menús' lista")
        print(u"Pestañas listas!")

        if len(sys.argv) > 1:
            archivito = sys.argv[1]
            print(u"\nAbriendo " + archivito + u" ...")
            self.parseUnkFile(archivito)
            print(u"Archivo abierto correctamente.\n")

        self.gui.overrideClose(self.onMainClose)

        print(u"Iniciando interfaz.\n")
        self.gui.start()

        return self.gui.isRestart()

    def startLoop(self):
        # type: () -> None
        while self.start():
            print(u"\nReiniciando...\n")
            self.gui.stop()
        return

    def updateTransTab(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        for i in range(4):
            transformData = self.unkData.transObj.getTransformData(i)

            char = language.getCharactersNamesPos(transformData[0])
            self.gui.comboboxs["trans"][i].current(char)
            self.gui.comboboxs["trans"][i]["state"] = "readonly"

            self.gui.comboboxs["barras"][i].current(transformData[1])
            self.gui.comboboxs["barras"][i]["state"] = "readonly"

            ani = language.getAnimationsPos(transformData[2])
            self.gui.comboboxs["ani"][i].current(ani)
            self.gui.comboboxs["ani"][i]["state"] = "readonly"

            aura = language.getAurasPos(transformData[3])
            self.gui.comboboxs["aura"][i].current(aura)
            self.gui.comboboxs["aura"][i]["state"] = "readonly"

            absor = language.getCharactersNamesPos(transformData[4])
            self.gui.comboboxs["absor"][i].current(absor)
            if transformData[2] == 3:
                self.gui.comboboxs["absor"][i]["state"] = "readonly"
            else:
                self.gui.comboboxs["absor"][i]["state"] = "disabled"

        r3 = self.unkData.transObj.getR3Command()
        r3 = language.getR3CommandPos(r3)
        self.gui.comboboxs["R3"][0].current(r3)
        self.gui.comboboxs["R3"][0]["state"] = "readonly"

        bonus = self.unkData.transObj.getBonus()
        bonus = language.getTransformationBonusPos(bonus)
        self.gui.comboboxs["bonus"][0].current(bonus)
        self.gui.comboboxs["bonus"][0]["state"] = "readonly"
        language.close()
        print(u"Datos de pestaña 'Transformaciones' lista")
        return

    def updateFusionsTab(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        for i in range(3):
            fusionData = self.unkData.fusionObj.getFusionData(i)

            self.gui.comboboxs["fusBarras"][i].current(fusionData[0])
            self.gui.comboboxs["fusBarras"][i]["state"] = "readonly"

            fusType = language.getFusionsTypesPos(fusionData[1])
            self.gui.comboboxs["fusType"][i].current(fusType)
            self.gui.comboboxs["fusType"][i]["state"] = "readonly"

            fusResul = language.getCharactersNamesPos(fusionData[2])
            self.gui.comboboxs["fusResul"][i].current(fusResul)
            self.gui.comboboxs["fusResul"][i]["state"] = "readonly"

            fusCompa = language.getCharactersNamesPos(fusionData[3])
            self.gui.comboboxs["fusCompa"][i].current(fusCompa)
            self.gui.comboboxs["fusCompa"][i]["state"] = "readonly"

            for j in range(4):
                fusEquipo = language.getCharactersNamesPos(fusionData[4 + j])
                self.gui.comboboxs["fusEquipo"][i][j].current(fusEquipo)
                self.gui.comboboxs["fusEquipo"][i][j]["state"] = "readonly"
        language.close()
        print(u"Datos de pestaña 'Fusiones' lista")
        return

    def updateMenusTab(self):
        # type: () -> None
        i = 0
        amountConst = Constants.AmountConst()
        languagesAmount = amountConst.languagesAmount
        menusAmount = amountConst.menusAmount
        statsAmount = amountConst.statsAmount
        for menu in self.unkData.menusList:
            if menu.isKnow():
                if i >= languagesAmount:
                    print(u"ERROR: Mas idiomas de lo esperado")
                    break

                j = 0
                for submenu in menu.subMenus:
                    if not submenu.isNone():
                        if j >= menusAmount:
                            print(u"ERROR: Mas menus de lo esperado")
                            break

                        menuName = submenu.getMenuName()

                        self.gui.entries["nombreMenu"][i][j]["state"] = "normal"
                        self.gui.entries["nombreMenu"][i][j].delete(0, "end")
                        self.gui.entries["nombreMenu"][i][j].insert("end", menuName)

                        self.gui.checkbuttons["menuOn"][i][j].select()

                        k, k0 = 0, 0
                        statsInesperados = False
                        for stat in submenu.stats:
                            if k >= statsAmount:
                                statsInesperados = True
                                k += 1
                                continue
                            statName = stat.getName()

                            self.gui.entries["nombreStat"][i][j][k]["state"] = "normal"
                            self.gui.entries["nombreStat"][i][j][k].delete(0, "end")
                            self.gui.entries["nombreStat"][i][j][k].insert("end", statName)

                            self.gui.checkbuttons["addStat"][i][j][k].select()

                            if stat.getMaxPower():
                                self.gui.checkbuttons["maxPower"][i][j][k].select()
                            else:
                                self.gui.checkbuttons["maxPower"][i][j][k].deselect()
                            self.gui.checkbuttons["maxPower"][i][j][k]["state"] = "normal"

                            self.gui.comboboxs["barrasKiMenus"][i][j][k].current(int(stat.getBarrasKi()))
                            self.gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "readonly"

                            self.gui.comboboxs["reservaKi"][i][j][k].current(int(stat.getReservaKi()))
                            self.gui.comboboxs["reservaKi"][i][j][k]["state"] = "readonly"

                            # TODO: rehacer
                            # gui.buttons["showData"][i][j][k]["command"] = functools.partial(popData, stat.getStatChars())
                            # gui.buttons["showData"][i][j][k]["state"] = "normal"

                            k += 1
                            k0 += 1
                        while k0 < statsAmount:
                            self.gui.checkbuttons["addStat"][i][j][k0].deselect()
                            self.gui.checkbuttons["maxPower"][i][j][k0].deselect()
                            self.gui.buttons["showData"][i][j][k0]["state"] = "disabled"
                            self.gui.checkbuttons["maxPower"][i][j][k0]["state"] = "disabled"
                            # self.gui.buttons["showData"][i][j][k0]["command"] = functools.partial(popData, list())
                            self.gui.buttons["showData"][i][j][k0]["state"] = "disabled"
                            k0 += 1
                        if statsInesperados:
                            print(u"Error: Mas stats que los esperados:", k)
                        j += 1
                i += 1
        for i in range(languagesAmount):
            for j in range(menusAmount):
                self.gui.checkbuttons["menuOn"][i][j]["state"] = "normal"
                for k in range(statsAmount):
                    self.gui.checkbuttons["addStat"][i][j][k]["state"] = "normal"

        print(u"Datos de pestaña 'Menús' lista")
        return

    def updateTransObject(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        for i in range(4):
            a = self.gui.comboboxs["trans"][i].get()
            a = language.getCharactersNamesID(a)

            b = self.gui.comboboxs["barras"][i].current()

            c = self.gui.comboboxs["ani"][i].get()
            c = language.getAnimationsID(c)

            d = self.gui.comboboxs["aura"][i].get()
            d = language.getAurasID(d)

            e = self.gui.comboboxs["absor"][i].get()
            e = language.getCharactersNamesID(e)

            self.unkData.transObj.setTransformData(i, [a, b, c, d, e])

        r3 = self.gui.comboboxs["R3"][0].get()
        r3 = language.getR3CommandID(r3)
        self.unkData.transObj.setR3Command(r3)

        bonus = self.gui.comboboxs["bonus"][0].get()
        bonus = language.getTransformationBonusID(bonus)
        self.unkData.transObj.setBonus(bonus)

        language.close()
        return

    def updateFusObject(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])

        for i in range(3):
            fusBarras = self.gui.comboboxs["fusBarras"][i].current()

            fusTypeSelected = self.gui.comboboxs["fusType"][i].get()
            fusTypeID = language.getFusionsTypesID(fusTypeSelected)

            fusResulSelected = self.gui.comboboxs["fusResul"][i].get()
            fusResulID = language.getCharactersNamesID(fusResulSelected)

            fusCompaSelected = self.gui.comboboxs["fusCompa"][i].get()
            fusCompaID = language.getCharactersNamesID(fusCompaSelected)

            fusionData = [fusBarras, fusTypeID, fusResulID, fusCompaID]

            for j in self.gui.comboboxs["fusEquipo"][i]:
                fusionData.append(language.getCharactersNamesID(j.get()))

            self.unkData.fusionObj.setFusionData(i, fusionData)

        language.close()
        return

    def updateMenusObject(self):
        # type: () -> None
        amountConst = Constants.AmountConst()
        for i in range(amountConst.languagesAmount):
            j0 = 0
            subMenuLoop = self.unkData.menusList[i].subMenus
            for j in range(amountConst.menusAmount):
                if self.gui.checkbuttons["menuOn"][i][j].is_checked():
                    nombreMenu = self.gui.entries["nombreMenu"][i][j].get()

                    if j < len(subMenuLoop) and subMenuLoop[j].isNone():
                        raise TypeError("NoneType found")

                    if j >= len(subMenuLoop):
                        subMenuLoop.append(SubMenu.SubMenu(b""))

                    subMenuLoop[j0].setMenuName(nombreMenu)
                    subMenuLoop[j0].setMenuNum(j0)
                    stats = subMenuLoop[j0].stats
                    k0 = 0
                    for k in range(amountConst.statsAmount):
                        if self.gui.checkbuttons["addStat"][i][j][k].is_checked():
                            nombrestat = self.gui.entries["nombreStat"][i][j][k].get()
                            maxPower = self.gui.checkbuttons["maxPower"][i][j][k].is_checked()
                            barrasKi = self.gui.comboboxs["barrasKiMenus"][i][j][k].get()
                            reservaKi = self.gui.comboboxs["reservaKi"][i][j][k].get()

                            if k >= len(stats):
                                stats.append(StatMenu.StatMenu(b""))

                            stats[k0].setName(nombrestat)
                            stats[k0].setMaxPower(maxPower)
                            stats[k0].setBarrasKi(barrasKi)
                            stats[k0].setReservaKi(reservaKi)
                            k0 += 1
                    del stats[k0:]

                    j0 += 1
            del subMenuLoop[j0:]
        return

    def parseUnkFile(self, fileName):
        # type: (str) -> None
        if not fileName:
            return
        printData = self.conf["printData"].capitalize() == "True"
        self.unkData = CharacterUnkParser.CharacterUnkParser(fileName, printData=printData)
        self.gui.clean()

        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_actionfail = language.getLanguageData("popup_actionfail")
        popup_errorreading = language.getLanguageData("popup_errorreading")
        popup_errorshowing = language.getLanguageData("popup_errorshowing")
        language.close()

        try:
            self.unkData.parse()
        except Exception as err:
            print(err)
            self.unkData = None
            # GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado leyendo el archivo.")
            GuiManager.popupError(popup_actionfail, popup_errorreading)
            raise
        else:
            try:
                self.updateTransTab()
                self.updateFusionsTab()
                self.updateMenusTab()
            except Exception as err:
                print(err)
                # GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado al mostrar los datos.")
                GuiManager.popupError(popup_actionfail, popup_errorshowing)
                raise
        return

    def saveFile(self):
        # type () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_actionfail = language.getLanguageData("popup_actionfail")
        popup_actioncompleted = language.getLanguageData("popup_actioncompleted")
        popup_filesaved = language.getLanguageData("popup_filesaved")
        popup_filenotsaved = language.getLanguageData("popup_filenotsaved")
        popup_mustopenfile = language.getLanguageData("popup_mustopenfile")
        language.close()

        if self.unkData is not None:
            self.updateTransObject()
            self.updateFusObject()
            self.updateMenusObject()
            try:
                self.unkData.saveFile()
                # GuiManager.popupInfo(u"Accion completada.", u"Archivo actualizado correctamente.")
                GuiManager.popupInfo(popup_actioncompleted, popup_filesaved)
            except Exception as err:
                print(err)
                # text1 = u"Acción fallida."
                # text2 = u"Ha ocurrido un error inesperado. Su archivo no ha sido modificado."
                GuiManager.popupError(popup_actionfail, popup_filenotsaved)
                raise
        else:
            # GuiManager.popupWarning(u"Acción fallida.", u"Debe abrir un archivo primero.")
            GuiManager.popupWarning(popup_actionfail, popup_mustopenfile)
        return

    def saveAsUnkFile(self, fileName):
        # type: (str) -> None
        if not fileName:
            return
        if not fileName.lower().endswith(u".unk"):
            fileName = fileName + u".unk"

        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_actionfail = language.getLanguageData("popup_actionfail")
        popup_actioncompleted = language.getLanguageData("popup_actioncompleted")
        popup_filenotsaved = language.getLanguageData("popup_filenotsaved")
        popup_mustopenfile = language.getLanguageData("popup_mustopenfile")
        popup_namesaved = language.getLanguageData("popup_namesaved").format(filename=fileName)
        language.close()

        if self.unkData is None:
            GuiManager.popupWarning(popup_actionfail, popup_mustopenfile)

        try:
            self.updateTransObject()
            self.updateFusObject()
            self.updateMenusObject()
            self.unkData.saveFile(fileName)
            # GuiManager.popupInfo(u"Accion completada", u"Archivo " + fileName + u" guardado satisfactoriamente")
            GuiManager.popupInfo(popup_actioncompleted, popup_namesaved)
        except Exception as err:
            print(err)
            # GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado.\nSu archivo no ha sido guardado.")
            GuiManager.popupError(popup_actionfail, popup_filenotsaved)
            raise
        return

    def updateMultiplesUnkFiles(self, archivos):
        # type: (list) -> None
        if not archivos:
            return

        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_actionfail = language.getLanguageData("popup_actionfail")
        popup_actioncompleted = language.getLanguageData("popup_actioncompleted")
        popup_filessaved = language.getLanguageData("popup_filessaved")
        popup_errornotcharacter = language.getLanguageData("popup_errornotcharacter")
        language.close()

        try:
            self.updateTransObject()
            self.updateFusObject()
            self.updateMenusObject()
            for arch in archivos:
                print((arch,))
                personaje = CharacterUnkParser.CharacterUnkParser(arch)
                personaje.parse()
                personaje.saveFile(src=self.unkData)
            # GuiManager.popupInfo(u"Acción completada", u"Archivos actualizados satisfactoriamente")
            GuiManager.popupInfo(popup_actioncompleted, popup_filessaved)
        except Exception as err:
            print(err)
            texto = u"Ha ocurrido un error inesperado.\nQuizas intentaste actualizar un archivo que no es de personaje."
            GuiManager.popupError(popup_actionfail, popup_errornotcharacter)
            raise
        return

    # TODO: Make this a class
    def logData(self):
        log = open(os.path.join("logs", "transObj.log"), "wb")
        dataLog = self.unkData.transObj.getAsLines()
        log.write(dataLog[0] + dataLog[1])
        log.close()

        log = open(os.path.join("logs", "fusionObj.log"), "wb")
        dataLog = self.unkData.fusionObj.getAsLine()
        log.write(dataLog)
        log.close()

        for i in range(len(self.unkData.menusList)):
            iMenu = self.unkData.menusList[i]
            dataLog = iMenu.getAsLine()
            log = open(os.path.join("logs", "menusListObj" + str(i) + ".log"), "wb")
            log.write(dataLog)
            log.close()
        return

    def openFileCaller(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_openfile = language.getLanguageData("popup_openfile")
        language.close()

        # nombre = GuiManager.openFile(u"Abrir archivo", Constants.ProgramConst().FileTypes)
        nombre = GuiManager.openFile(popup_openfile, Constants.ProgramConst().FileTypes)
        self.parseUnkFile(nombre)
        return

    def saveAsUnkFileCaller(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_savefile = language.getLanguageData("popup_savefile")
        popup_actionfail = language.getLanguageData("popup_actionfail")
        popup_mustopenfile = language.getLanguageData("popup_mustopenfile")
        language.close()

        if self.unkData is not None:
            # nombre = GuiManager.saveFile(u"Guardar archivo", Constants.ProgramConst().FileTypes)
            nombre = GuiManager.saveFile(popup_savefile, Constants.ProgramConst().FileTypes)
            self.saveAsUnkFile(nombre)
        else:
            # GuiManager.popupWarning(u"Acción fallida", u"Debe abrir un archivo primero.")
            GuiManager.popupWarning(popup_actionfail, popup_mustopenfile)
        return

    def updateMultiplesUnkFilesCaller(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_selectfiles = language.getLanguageData("popup_selectfiles")
        popup_actionfail = language.getLanguageData("popup_actionfail")
        popup_mustopenfile = language.getLanguageData("popup_mustopenfile")
        language.close()

        if self.unkData is not None:
            # nombre = GuiManager.selectMultiplesFiles(u"Seleccionar archivos", Constants.ProgramConst().FileTypes)
            nombre = GuiManager.selectMultiplesFiles(popup_selectfiles, Constants.ProgramConst().FileTypes)
            self.updateMultiplesUnkFiles(nombre)
        else:
            # GuiManager.popupWarning(u"Acción fallida", u"Debe abrir un archivo primero.")
            GuiManager.popupWarning(popup_actionfail, popup_mustopenfile)
        return

    def openFolderCaller(self):
        # type: () -> None
        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_selectunkfolder = language.getLanguageData("popup_selectunkfolder")
        popup_actionfail = language.getLanguageData("popup_actionfail")
        popup_mustopenfile = language.getLanguageData("popup_mustopenfile")
        language.close()

        if self.unkData is not None:
            # if GuiManager.selectFolder(u"Selecciona carpeta de archivos 'unk' de personajes."):
            if GuiManager.selectFolder(popup_selectunkfolder):
                WIP()
        else:
            # GuiManager.popupWarning(u"Acción fallida", u"Debe abrir un archivo primero.")
            GuiManager.popupWarning(popup_actionfail, popup_mustopenfile)
        return

    def undoOptionsChange(self):
        # type: () -> None
        languagesFiles = self.subGui.comboboxs["lang"][0]["values"]
        languagesFiles = [x.lower() for x in languagesFiles]
        langIndex = languagesFiles.index(".".join(self.conf["language"].split(".")[:-1]))
        self.subGui.comboboxs["lang"][0].current(langIndex)
        return

    def acceptOptionsChange(self):
        # type: () -> None
        self.subGui.disableAll()

        language = LanguageManager.LanguageManager(self.conf["language"])
        popup_restart = language.getLanguageData("popup_restart")
        popup_askrestart = language.getLanguageData("popup_askrestart")
        language.close()

        # restart = GuiManager.popupYesNo(u"Reiniciar.", u"Para aplicar los cambios se necesita reinicar.\n¿Quiere reiniciar?")
        restart = GuiManager.popupYesNo(popup_restart, popup_askrestart)
        if restart:
            print(u"\n")
            langSelected = self.subGui.comboboxs["lang"][0].get() + u".db"
            print(u"Idioma: " + langSelected)
            self.conf["language"] = langSelected.lower()
            self.gui.setRestart(True)
            self.conf.updateFile()
            print(u"\n")
            self.onMainClose()
        else:
            self.subGui.enableAll()
        return

    def onOptionsOpen(self):
        # type: () -> None
        try:
            langFolder = os.path.join(os.getcwd(), "lang")
            os.listdir(langFolder)
        except OSError:
            langFolder = os.path.join(os.getcwd(), "..", "lang")
            os.listdir(langFolder)

        languagesFiles = [".".join(f.split(".")[:-1]) for f in os.listdir(langFolder)
                          if os.path.isfile(os.path.join(langFolder, f))]

        langIndex = languagesFiles.index(".".join(self.conf["language"].split(".")[:-1]))
        languagesFiles = [x.capitalize() for x in languagesFiles]

        self.subGui.comboboxs["lang"][0]["state"] = "readonly"
        self.subGui.comboboxs["lang"][0]["values"] = languagesFiles
        self.subGui.comboboxs["lang"][0].current(langIndex)

        # Accept button
        self.subGui.buttons["optionsConfirm"][0]["command"] = self.acceptOptionsChange
        # Cancel button
        self.subGui.buttons["optionsConfirm"][1]["command"] = self.subGui.quit
        # Redo button
        self.subGui.buttons["optionsConfirm"][2]["command"] = self.undoOptionsChange
        return

    def optionsCaller(self):
        # type: () -> None
        if self.subGui is not None and self.subGui.isRunning():
            self.subGui.stop()
        else:
            self.subGui = GuiManager.GuiManager(u"Opciones", self.icon)

        language = LanguageManager.LanguageManager(self.conf["language"])
        tab_generaloptions = language.getLanguageData("tab_generaloptions")
        options_title = language.getLanguageData("options_title")
        language.close()

        self.subGui.addTab(tab_generaloptions, functools.partial(UnkGuiGenerator.optionsTab, conf=self.conf))
        self.onOptionsOpen()

        self.subGui.start(options_title)
        return

    def about(self):
        # type: () -> None
        titulo = u"Acerca de"
        texto = self.title + u".\nCreado por AngheloAlf"
        GuiManager.popupInfo(titulo, texto)
        return

    def onMainClose(self):
        # type: () -> None
        if self.subGui is not None and self.subGui.isRunning():
            self.subGui.quit()
        print(u"\nCerrando...\n")
        self.gui.quit()
        return

    def debugMain(self):
        # type: () -> None
        print("\n\t[DEBUG] log\n")
        self.logData()
        print("\n\t[DEBUG] log\n")
        return
