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

    import Tkinter as tk
    import ttk
except Exception:
    import packages.GuiManager as GuiManager
    import packages.CharacterUnkParser as CharacterUnkParser
    import packages.SubMenu as SubMenu
    import packages.StatMenu as StatMenu
    import packages.LanguageManager as LanguageManager
    import packages.Constants as Constants

    import tkinter as tk
    from tkinter import ttk


class CharacterData:
    def __init__(self):
        self.data = None


def comboTransUpdate(event=None):
    # type: (tk.Event, str) -> None
    language = LanguageManager.LanguageManager(gui.languageFile)
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

        if gui.comboboxs["ani"][i].current() == 3:
            gui.comboboxs["absor"][i]["state"] = "readonly"
        else:
            gui.comboboxs["absor"][i]["state"] = "disabled"

    r3 = gui.comboboxs["R3"].get()
    r3 = language.getR3CommandID(unicode(r3))
    character.data.transObj.setR3Command(r3, True)

    bonus = gui.comboboxs["bonus"].get()
    bonus = language.getTransformationBonusID(unicode(bonus))
    character.data.transObj.setBonus(bonus, True)

    language.close()
    return


def comboFusUpdate(event=None):
    # type: (tk.Event) -> None
    language = LanguageManager.LanguageManager(gui.languageFile)

    for i in range(3):
        fusBarras = gui.comboboxs["fusBarras"][i].current()

        fusTypeSelected = gui.comboboxs["fusType"][i].get()
        fusTypeID = language.getFusionsTypesID(unicode(fusTypeSelected))

        fusResulSelected = gui.comboboxs["fusResul"][i].get()
        fusResulID = language.getCharactersNamesID(unicode(fusResulSelected))

        fusCompaSelected = gui.comboboxs["fusCompa"][i].get()
        fusCompaID = language.getCharactersNamesID(unicode(fusCompaSelected))

        fusionData = [fusBarras, fusTypeID, fusResulID, fusCompaID]

        if event and event.widget == gui.comboboxs["fusCompa"][i]:
            gui.comboboxs["fusEquipo"][i][0].current(gui.comboboxs["fusCompa"][i].current())

        for j in gui.comboboxs["fusEquipo"][i]:
            fusionData.append(language.getCharactersNamesID(unicode(j.get())))

        character.data.fusionObj.setFusionData(i, fusionData, True)

    language.close()
    return


def comboMenusUpdate(event=None):
    # type: (tk.Event) -> None
    if event and event.widget:
        for i in range(Constants.AmountConst().languagesAmount):
            for j in range(Constants.AmountConst().menusAmount):
                for k in range(Constants.AmountConst().statsAmount):
                    if event.widget == gui.comboboxs["barrasKiMenus"][i][j][k]:
                        if gui.comboboxs["barrasKiMenus"][i][j][k].current() != 0:
                            gui.comboboxs["reservaKi"][i][j][k].current(0)
                    elif event.widget == gui.comboboxs["reservaKi"][i][j][k]:
                        if gui.comboboxs["reservaKi"][i][j][k].current() != 0:
                            gui.comboboxs["barrasKiMenus"][i][j][k].current(0)
    return


def menusUpdate(event=None):
    # type: (tk.Event) -> None
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


def addTrans(tab):
    # type: (ttk.Frame) -> (int, int)

    language = LanguageManager.LanguageManager(gui.languageFile)
    charactersNames = [x[1] for x in language.getCharactersNames()]
    barras = range(8)  # [x[1] for x in language.get()]
    animations = [x[1] for x in language.getAnimations()]
    auras = [x[1] for x in language.getAuras()]
    absorbed = [x[1] for x in language.getCharactersNames()]

    r3Command = [x[1] for x in language.getR3Command()]
    transformationBonus = [x[1] for x in language.getTransformationBonus()]

    # languageData
    trans_transformation = language.getLanguageData(u"trans_transformation")
    trans_ki = language.getLanguageData(u"trans_ki")
    trans_animation = language.getLanguageData(u"trans_animation")
    trans_aura = language.getLanguageData(u"trans_aura")
    trans_absorbed = language.getLanguageData(u"trans_absorbed")
    trans_r3 = language.getLanguageData(u"trans_r3")
    trans_bonus = language.getLanguageData(u"trans_bonus")

    language.close()

    xPoss = [25, 60, 260, 330, 530, 700]
    yPoss = [30, 60, 90, 120, 180, 210]

    GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[1], 5, text=trans_transformation)
    GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[2], 5, text=trans_ki)
    GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[3], 5, text=trans_animation)
    GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[4], 5, text=trans_aura)
    GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[5], 5, text=trans_absorbed)

    gui.comboboxs["trans"] = list()
    gui.comboboxs["barras"] = list()
    gui.comboboxs["ani"] = list()
    gui.comboboxs["aura"] = list()
    gui.comboboxs["absor"] = list()

    for i in range(4):
        GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[0], yPoss[i], text=unicode(i + 1) + u": ")

        trans = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[1], yPoss[i], values=charactersNames,
                                             width=180, command=comboTransUpdate)
        gui.comboboxs["trans"].append(trans)

        barrasKi = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[2], yPoss[i], values=barras,
                                                width=50, command=comboTransUpdate)
        gui.comboboxs["barras"].append(barrasKi)

        ani = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[3], yPoss[i], values=animations,
                                           width=180, command=comboTransUpdate)
        gui.comboboxs["ani"].append(ani)

        aura = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[4], yPoss[i], values=auras,
                                            width=150, command=comboTransUpdate)
        gui.comboboxs["aura"].append(aura)

        absor = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[5], yPoss[i], values=absorbed,
                                             width=180, command=comboTransUpdate)
        gui.comboboxs["absor"].append(absor)

    GuiManager.generateTtkWidget(u"Label", tab, u"place", 25, 180, text=trans_r3+u": ")
    comboR3 = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", 180, 180, values=r3Command,
                                           width=210, command=comboTransUpdate)
    gui.comboboxs["R3"] = comboR3

    GuiManager.generateTtkWidget(u"Label", tab, u"place", 25, 210, text=trans_bonus+u": ")
    bonus = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", 180, 210, values=transformationBonus,
                                         width=210, command=comboTransUpdate)
    gui.comboboxs["bonus"] = bonus

    return xPoss[-1] + 200, yPoss[-1] + 60


def addFusion(tab):
    # type: (ttk.Frame) -> tuple
    newTabs = ttk.Notebook(tab)

    language = LanguageManager.LanguageManager(gui.languageFile)
    charactersNames = [x[1] for x in language.getCharactersNames()]
    barrasKi = range(8)
    fusionsTypes = [x[1] for x in language.getFusionsTypes()]

    # languageData
    fus_ki = language.getLanguageData(u"fus_ki")
    fus_type = language.getLanguageData(u"fus_type")
    fus_result = language.getLanguageData(u"fus_result")
    fus_ani_partner = language.getLanguageData(u"fus_ani_partner")

    xPoss = [40, 110, 240, 440, 40, 240, 440, 640]
    yPoss = [10, 35, 75, 100]

    gui.comboboxs["fusBarras"] = list()
    gui.comboboxs["fusType"] = list()
    gui.comboboxs["fusResul"] = list()
    gui.comboboxs["fusCompa"] = list()
    gui.comboboxs["fusEquipo"] = [list(), list(), list()]

    for i in range(3):
        i += 1
        subTab = ttk.Frame(newTabs, width=900, height=yPoss[-1] + 60)
        newTabs.add(subTab, text=language.getLanguageData(u"fus_tab_fus_" + unicode(i)))

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[0], yPoss[0], text=fus_ki)
        fusBarras = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[0], yPoss[1],
                                                 values=barrasKi, width=50, command=comboFusUpdate)
        gui.comboboxs["fusBarras"].append(fusBarras)

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[1], yPoss[0], text=fus_type)
        fusType = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[1], yPoss[1],
                                               values=fusionsTypes, width=110, command=comboFusUpdate)
        gui.comboboxs["fusType"].append(fusType)

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[2], yPoss[0],
                                     text=fus_result)
        fusResul = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[2], yPoss[1],
                                                values=charactersNames, width=180, command=comboFusUpdate)
        gui.comboboxs["fusResul"].append(fusResul)

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[3], yPoss[0], text=fus_ani_partner)
        fusCompa = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[3], yPoss[1],
                                                values=charactersNames, width=180, command=comboFusUpdate)
        gui.comboboxs["fusCompa"].append(fusCompa)

        for j in range(4):
            j += 1
            GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[3+j], yPoss[2],
                                         text=language.getLanguageData(u"fus_character_"+unicode(j)))
            fusEquipo = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[3 + j], yPoss[3],
                                                     values=charactersNames, width=180, command=comboFusUpdate)
            gui.comboboxs["fusEquipo"][i - 1].append(fusEquipo)

    newTabs.grid(column=0, row=0)

    language.close()

    return xPoss[-1] + 200, yPoss[-1] + 60


def updateScrollbar(canvas, event, width=200, height=100):
    canvas.configure(scrollregion=canvas.bbox("all"), width=width, height=height)


def onActiveRowClick(button, pos):
    # type: (GuiManager.CheckButton, tuple) -> None
    i, j, k = pos
    if button.is_checked():
        gui.entries["nombreStat"][i][j][k]["state"] = "normal"
        gui.checkbuttons["maxPower"][i][j][k]["state"] = "normal"
        gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "readonly"
        if gui.comboboxs["barrasKiMenus"][i][j][k].current() < 0:
            gui.comboboxs["barrasKiMenus"][i][j][k].current(0)
        gui.comboboxs["reservaKi"][i][j][k]["state"] = "readonly"
        if gui.comboboxs["reservaKi"][i][j][k].current() < 0:
            gui.comboboxs["reservaKi"][i][j][k].current(0)
        gui.buttons["showData"][i][j][k]["state"] = "normal"
    else:
        gui.entries["nombreStat"][i][j][k]["state"] = "disabled"
        gui.checkbuttons["maxPower"][i][j][k]["state"] = "disabled"
        gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "disabled"
        gui.comboboxs["reservaKi"][i][j][k]["state"] = "disabled"
        gui.buttons["showData"][i][j][k]["state"] = "disabled"


def onActiveMenuOn(button, pos):
    # type: (GuiManager.CheckButton, tuple) -> None
    i, j = pos
    if button.is_checked():
        gui.entries["nombreMenu"][i][j]["state"] = "normal"
    else:
        gui.entries["nombreMenu"][i][j]["state"] = "disabled"
    for k in range(Constants.AmountConst().statsAmount):
        if button.is_checked():
            gui.checkbuttons["addStat"][i][j][k]["state"] = "normal"
            if gui.checkbuttons["addStat"][i][j][k].is_checked():
                gui.entries["nombreStat"][i][j][k]["state"] = "normal"
                gui.checkbuttons["maxPower"][i][j][k]["state"] = "normal"
                gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "readonly"
                gui.comboboxs["reservaKi"][i][j][k]["state"] = "readonly"
                gui.buttons["showData"][i][j][k]["state"] = "normal"
        else:
            gui.checkbuttons["addStat"][i][j][k]["state"] = "disabled"
            gui.entries["nombreStat"][i][j][k]["state"] = "disabled"
            gui.checkbuttons["maxPower"][i][j][k]["state"] = "disabled"
            gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "disabled"
            gui.comboboxs["reservaKi"][i][j][k]["state"] = "disabled"
            gui.buttons["showData"][i][j][k]["state"] = "disabled"


def addMenusTab(tab):
    # type: (ttk.Frame) -> (int, int)

    language = LanguageManager.LanguageManager(gui.languageFile)

    # languageData
    menus_name = language.getLanguageData(u"menus_name")
    menus_activate = language.getLanguageData(u"menus_activate")
    menus_activate_sub = language.getLanguageData(u"menus_activate_sub")
    menus_sentence = language.getLanguageData(u"menus_sentence")
    menus_max_power = language.getLanguageData(u"menus_max_power")
    menus_ki_bars = language.getLanguageData(u"menus_ki_bars")
    menus_ki_number = language.getLanguageData(u"menus_ki_number")
    menus_data = language.getLanguageData(u"menus_data")

    newTabs = ttk.Notebook(tab)

    xPoss = [5, 20, 180, 240, 440, 40, 240, 440, 640]
    yPoss = [0, 20, 50, 100, 200]

    gui.entries["nombreMenu"] = list()

    gui.entries["nombreStat"] = list()
    gui.checkbuttons["menuOn"] = list()
    gui.checkbuttons["addStat"] = list()

    gui.checkbuttons["maxPower"] = list()
    gui.comboboxs["barrasKiMenus"] = list()
    gui.comboboxs["reservaKi"] = list()

    gui.buttons["showData"] = list()

    for i in range(Constants.AmountConst().languagesAmount):
        subTab = ttk.Frame(newTabs, width=900, height=yPoss[-1] + 60)

        newTabs.add(subTab, text=language.getLanguageData(u"menus_lang_"+unicode(i+1)))

        menuNameTab = ttk.Notebook(subTab)
        gui.entries["nombreMenu"].append(list())

        gui.entries["nombreStat"].append(list())
        gui.checkbuttons["menuOn"].append(list())
        gui.checkbuttons["addStat"].append(list())

        gui.checkbuttons["maxPower"].append(list())
        gui.comboboxs["barrasKiMenus"].append(list())
        gui.comboboxs["reservaKi"].append(list())

        gui.buttons["showData"].append(list())

        for j in range(Constants.AmountConst().menusAmount):
            menuTab = ttk.Frame(newTabs, width=900, height=yPoss[-1] + 60)
            menuNameTab.add(menuTab, text=language.getLanguageData(u"menus_menu_" + unicode(j+1)))

            nameTab = ttk.LabelFrame(menuTab, width=880, height=70)
            nameTab.pack()
            nameTab.place(x=10, y=0)

            GuiManager.generateTtkWidget(u"Label", nameTab, u"place", xPoss[1], yPoss[0], text=menus_name)

            nombreMenu = GuiManager.generateTtkWidget(u"Entry", nameTab, u"place", xPoss[1], yPoss[1], width=150)
            gui.entries["nombreMenu"][-1].append(nombreMenu)

            checkbutton = GuiManager.generateTtkWidget(u"CheckButton", nameTab, u"place", xPoss[3], yPoss[1]-5,
                                                       text=menus_activate)
            checkbutton["command"] = functools.partial(onActiveMenuOn, checkbutton, (i, j))
            gui.checkbuttons["menuOn"][-1].append(checkbutton)

            gui.entries["nombreStat"][-1].append(list())
            gui.checkbuttons["addStat"][-1].append(list())

            gui.checkbuttons["maxPower"][-1].append(list())
            gui.comboboxs["barrasKiMenus"][-1].append(list())
            gui.comboboxs["reservaKi"][-1].append(list())

            gui.buttons["showData"][-1].append(list())

            myframe = ttk.Frame(menuTab, width=880, height=200)
            myframe.place(x=10, y=80)

            canvas = tk.Canvas(myframe)
            frame = ttk.Frame(canvas)
            myscrollbar = ttk.Scrollbar(myframe, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=myscrollbar.set)

            myscrollbar.pack(side="right", fill="y")
            myscrollbar.config(command=canvas.yview)
            canvas.pack(side="left")
            canvas.create_window((0, 1), window=frame, anchor='nw')

            GuiManager.generateTtkWidget(u"Label", frame, u"grid", 0, 0, text=menus_activate_sub)
            GuiManager.generateTtkWidget(u"Label", frame, u"grid", 0, 1, text=menus_sentence)
            GuiManager.generateTtkWidget(u"Label", frame, u"grid", 0, 2, text=menus_max_power)
            GuiManager.generateTtkWidget(u"Label", frame, u"grid", 0, 3, text=menus_ki_bars)
            GuiManager.generateTtkWidget(u"Label", frame, u"grid", 0, 4, text=menus_ki_number)

            for k in range(Constants.AmountConst().statsAmount):
                checkbutton = GuiManager.generateTtkWidget(u"CheckButton", frame, u"grid", k+1, 0, text=unicode(k+1))
                checkbutton["command"] = functools.partial(onActiveRowClick, checkbutton, (i, j, k))
                gui.checkbuttons["addStat"][-1][-1].append(checkbutton)

                nombreStat = GuiManager.generateTtkWidget(u"Entry", frame, u"grid", k+1, 1, width=50)
                gui.entries["nombreStat"][-1][-1].append(nombreStat)

                maxPower = GuiManager.generateTtkWidget(u"CheckButton", frame, u"grid", k+1, 2)
                gui.checkbuttons["maxPower"][-1][-1].append(maxPower)

                barrasKiMenus = GuiManager.generateTtkWidget(u"Combobox", frame, u"grid", k+1, 3, values=range(6),
                                                             current=0, command=comboMenusUpdate)
                gui.comboboxs["barrasKiMenus"][-1][-1].append(barrasKiMenus)

                reservaKi = GuiManager.generateTtkWidget(u"Combobox", frame, u"grid", k+1, 4, values=range(8),
                                                         current=0, command=comboMenusUpdate)
                gui.comboboxs["reservaKi"][-1][-1].append(reservaKi)

                showData = GuiManager.generateTtkWidget(u"Button", frame, u"grid", k+1, 5,
                                                        text=u"[WIP]" + menus_data + u" " + unicode(k + 1))
                gui.buttons["showData"][-1][-1].append(showData)

            frame.bind("<Configure>", functools.partial(updateScrollbar, canvas, width=860, height=160))

        menuNameTab.grid(column=0, row=0)

    newTabs.grid(column=0, row=0)

    language.close()

    return 900, yPoss[-1] + 60


def parseUnkFile(fileName):
    # type: (unicode) -> None
    if not fileName:
        return
    character.data = CharacterUnkParser.CharacterUnkParser(fileName)
    gui.clean()

    try:
        character.data.parse()
        try:
            updateTransformations()
            updateFusions()
            updateMenus()
        except Exception as err:
            print(err)
            GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado al mostrar los datos.")
            raise
    except Exception as err:
        print(err)
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


def updateTransformations():
    # type: () -> None
    language = LanguageManager.LanguageManager(gui.languageFile)
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
    gui.comboboxs["R3"].current(r3)
    gui.comboboxs["R3"]["state"] = "readonly"

    bonus = character.data.transObj.getBonus(True)
    bonus = language.getTransformationBonusPos(bonus)
    gui.comboboxs["bonus"].current(bonus)
    gui.comboboxs["bonus"]["state"] = "readonly"
    language.close()
    print(u"Pestaña 'Transformaciones' lista")


def updateFusions():
    language = LanguageManager.LanguageManager(gui.languageFile)
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
    print(u"Pestaña 'Fusiones' lista")


# Archivo a interfaz
def updateMenus():
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

                    # entries["nombreMenu"][i][j]["state"] = "disabled"

                    # if menuNum < 7:
                    #     comboboxs["dragonballIcon"][i][j].current(menuNum)
                    # else:
                    #     comboboxs["dragonballIcon"][i][j]["value"] = list(
                    #         comboboxs["dragonballIcon"][i][j]["value"]) + [menuNum]
                    #     comboboxs["dragonballIcon"][i][j].current(len(comboboxs["dragonballIcon"][i][j]["value"]) - 1)
                    #     comboboxs["dragonballIcon"][i][j]["state"] = "disabled"

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

    print(u"Pestaña 'Menus' lista")
    return


def openFileCaller():
    GuiManager.openFile(u"Abrir archivo", Constants.ProgramConst().FileTypes, parseUnkFile)


def saveFile():
    # type () -> None
    if character.data:
        comboTransUpdate()
        comboFusUpdate()
        menusUpdate()
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


def saveAsUnkFile(fileName):
    # type: (unicode) -> None
    if not fileName:
        return
    if not fileName.lower().endswith(".unk"):
        fileName = fileName + ".unk"
    try:
        comboTransUpdate()
        comboFusUpdate()
        menusUpdate()
        character.data.saveFile(fileName)
        GuiManager.popupInfo(u"Accion completada", u"Archivo " + fileName + u" guardado satisfactoriamente")
    except Exception as err:
        print(err)
        GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado.\nSu archivo no ha sido guardado.")
        raise


def saveAsUnkFileCaller():
    if character.data:
        GuiManager.saveFile(u"Guardar archivo", Constants.ProgramConst().FileTypes, saveAsUnkFile)
    else:
        GuiManager.popupWarning(u"Acción fallida", u"Debe abrir un archivo primero.")


def updateMultiplesUnkFiles(archivos):
    # type: (list) -> None
    if not archivos:
        return
    comboTransUpdate()
    comboFusUpdate()
    menusUpdate()
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


def languageSelectorCaller():
    # type: () -> None
    GuiManager.popupInfo(u"WIP", u"Work in progress.")


def acercaDe():
    # type: () -> None
    titulo = u"Acerca de"
    texto = u"BT3 Character 'unk' Editor v" + Constants.ProgramConst().Version + u".\nCreado por AngheloAlf"
    GuiManager.popupInfo(titulo, texto)


title = Constants.ProgramConst().Title + u" v" + Constants.ProgramConst().Version
print(title)
character = CharacterData()
print(u"Inicializando interfaz...")
gui = GuiManager.GuiManager(title, icon=os.path.join(u"resources", u"icon.ico"))


def main():
    while True:
        language = LanguageManager.LanguageManager(gui.languageFile)

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
                (u"WIP"+mainmenu_select_unks_folder, openFolderCaller),
                (None, None),
                (mainmenu_quit, gui.quit)
            ],
            [(u"[WIP]"+mainmenu_language, languageSelectorCaller)],
            [(mainmenu_about, acercaDe)]
        ]

        gui.addMenu(cascadeNames, cascadeData)

        print(u"Preparando pestañas...")
        gui.addTab(tab_transformations, addTrans)
        print(u"'Transformaciones' lista.")
        gui.addTab(tab_fusions, addFusion)
        print(u"'Fusiones' lista.")
        gui.addTab(tab_menus, addMenusTab)
        print(u"'Menús' lista")
        print(u"Pestañas listas!")

        if len(sys.argv) > 1:
            archivito = unicode(sys.argv[1])
            print(u"\nAbriendo " + archivito + u" ...")
            parseUnkFile(archivito)
            print(u"Archivo abierto correctamente.\n")

        print(u"Iniciando interfaz")
        gui.start()

        if not gui.isRestart():
            break
