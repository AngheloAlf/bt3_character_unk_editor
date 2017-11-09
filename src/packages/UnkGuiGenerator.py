from __future__ import absolute_import

import functools

from . import LanguageManager
from . import GuiManager
from . import Constants
from . import OptionsManager


try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk


def comboTransUpdate(gui, event):
    # type: (GuiManager.GuiManager, tk.Event) -> None
    for i in range(4):
        if event.widget == gui.comboboxs["ani"][i]:
            if event.widget.current() == 3:
                gui.comboboxs["absor"][i]["state"] = "readonly"
            else:
                last = len(gui.comboboxs["absor"][i]["values"]) - 1
                gui.comboboxs["absor"][i].current(last)
                gui.comboboxs["absor"][i]["state"] = "disabled"
    return


def addTrans(gui, tab, conf):
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

    language = LanguageManager.LanguageManager(conf["language"])
    charactersNames = [x[1] for x in language.getCharactersNames()]
    barras = list(range(8))  # [x[1] for x in language.get()]
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

    command = functools.partial(comboTransUpdate, gui)

    for i in range(4):
        GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[0], yPoss[i], text=str(i + 1) + u": ")

        trans = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[1], yPoss[i], values=charactersNames,
                                             width=180, command=command)
        gui.comboboxs["trans"].append(trans)

        barrasKi = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[2], yPoss[i], values=barras,
                                                width=50, command=command)
        gui.comboboxs["barras"].append(barrasKi)

        ani = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[3], yPoss[i], values=animations,
                                           width=180, command=command)
        gui.comboboxs["ani"].append(ani)

        aura = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[4], yPoss[i], values=auras,
                                            width=150, command=command)
        gui.comboboxs["aura"].append(aura)

        absor = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[5], yPoss[i], values=absorbed,
                                             width=180, command=command)
        gui.comboboxs["absor"].append(absor)

    GuiManager.generateTtkWidget(u"Label", tab, u"place", 25, 180, text=trans_r3+u": ")
    comboR3 = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", 180, 180, values=r3Command,
                                           width=210, command=command)
    gui.comboboxs["R3"] = [comboR3]

    GuiManager.generateTtkWidget(u"Label", tab, u"place", 25, 210, text=trans_bonus+u": ")
    bonus = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", 180, 210, values=transformationBonus,
                                         width=210, command=command)
    gui.comboboxs["bonus"] = [bonus]

    return xPoss[-1] + 200, yPoss[-1] + 60


def comboFusUpdate(gui, event):
    # type: (GuiManager.GuiManager, tk.Event) -> None
    for i in range(3):
        if event.widget == gui.comboboxs["fusCompa"][i]:
            gui.comboboxs["fusEquipo"][i][0].current(gui.comboboxs["fusCompa"][i].current())
    return


def addFusion(gui, tab, conf):
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)
    newTabs = ttk.Notebook(tab)

    language = LanguageManager.LanguageManager(conf["language"])
    charactersNames = [x[1] for x in language.getCharactersNames()]
    barrasKi = list(range(8))
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

    command = functools.partial(comboFusUpdate, gui)

    for i in range(3):
        i += 1
        subTab = ttk.Frame(newTabs, width=900, height=yPoss[-1] + 60)
        newTabs.add(subTab, text=language.getLanguageData(u"fus_tab_fus_" + str(i)))

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[0], yPoss[0], text=fus_ki)
        fusBarras = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[0], yPoss[1],
                                                 values=barrasKi, width=50, command=command)
        gui.comboboxs["fusBarras"].append(fusBarras)

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[1], yPoss[0], text=fus_type)
        fusType = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[1], yPoss[1],
                                               values=fusionsTypes, width=110, command=command)
        gui.comboboxs["fusType"].append(fusType)

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[2], yPoss[0],
                                     text=fus_result)
        fusResul = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[2], yPoss[1],
                                                values=charactersNames, width=180, command=command)
        gui.comboboxs["fusResul"].append(fusResul)

        GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[3], yPoss[0], text=fus_ani_partner)
        fusCompa = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[3], yPoss[1],
                                                values=charactersNames, width=180, command=command)
        gui.comboboxs["fusCompa"].append(fusCompa)

        for j in range(4):
            j += 1
            GuiManager.generateTtkWidget(u"Label", subTab, u"place", xPoss[3+j], yPoss[2],
                                         text=language.getLanguageData(u"fus_character_"+str(j)))
            fusEquipo = GuiManager.generateTtkWidget(u"Combobox", subTab, u"place", xPoss[3 + j], yPoss[3],
                                                     values=charactersNames, width=180, command=command)
            gui.comboboxs["fusEquipo"][i - 1].append(fusEquipo)

    newTabs.grid(column=0, row=0)

    language.close()

    return xPoss[-1] + 200, yPoss[-1] + 60


def updateScrollbar(canvas, event, width=200, height=100):
    # type: (tk.Canvas, tk.Event, int, int) -> None
    if event:
        canvas.configure(scrollregion=canvas.bbox("all"), width=width, height=height)
    return


def onActiveRowClick(gui, button, pos):
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, (int, int, int)) -> None
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
    return


def onActiveMenuOn(gui, button, pos):
    # type: (GuiManager.GuiManager, GuiManager.CheckButton, (int, int, int)) -> None
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
    return


def comboMenusUpdate(gui, event):
    # type: (GuiManager.GuiManager, tk.Event) -> None
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


def addMenusTab(gui, tab, conf):
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

    language = LanguageManager.LanguageManager(conf["language"])

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
    yPoss = [0, 20, 50, 100, 200, 270]

    gui.entries["nombreMenu"] = list()

    gui.entries["nombreStat"] = list()
    gui.checkbuttons["menuOn"] = list()
    gui.checkbuttons["addStat"] = list()

    gui.checkbuttons["maxPower"] = list()
    gui.comboboxs["barrasKiMenus"] = list()
    gui.comboboxs["reservaKi"] = list()

    gui.buttons["showData"] = list()

    commandCombo = functools.partial(comboMenusUpdate, gui)

    for i in range(Constants.AmountConst().languagesAmount):
        subTab = ttk.Frame(newTabs, width=900, height=yPoss[-1])

        newTabs.add(subTab, text=language.getLanguageData(u"menus_lang_"+str(i+1)))

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
            menuTab = ttk.Frame(newTabs, width=900, height=yPoss[-1])
            menuNameTab.add(menuTab, text=language.getLanguageData(u"menus_menu_" + str(j+1)))

            nameTab = ttk.LabelFrame(menuTab, width=880, height=70)
            nameTab.pack()
            nameTab.place(x=10, y=0)

            GuiManager.generateTtkWidget(u"Label", nameTab, u"place", xPoss[1], yPoss[0], text=menus_name)

            nombreMenu = GuiManager.generateTtkWidget(u"Entry", nameTab, u"place", xPoss[1], yPoss[1], width=150)
            gui.entries["nombreMenu"][-1].append(nombreMenu)

            checkbutton = GuiManager.generateTtkWidget(u"CheckButton", nameTab, u"place", xPoss[3], yPoss[1]-5,
                                                       text=menus_activate)
            checkbutton["command"] = functools.partial(onActiveMenuOn, gui, checkbutton, (i, j))
            gui.checkbuttons["menuOn"][-1].append(checkbutton)

            gui.entries["nombreStat"][-1].append(list())
            gui.checkbuttons["addStat"][-1].append(list())

            gui.checkbuttons["maxPower"][-1].append(list())
            gui.comboboxs["barrasKiMenus"][-1].append(list())
            gui.comboboxs["reservaKi"][-1].append(list())

            gui.buttons["showData"][-1].append(list())

            myframe = ttk.LabelFrame(menuTab, width=880, height=yPoss[-1])
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
                checkbutton = GuiManager.generateTtkWidget(u"CheckButton", frame, u"grid", k+1, 0, text=str(k+1))
                checkbutton["command"] = functools.partial(onActiveRowClick, gui, checkbutton, (i, j, k))
                gui.checkbuttons["addStat"][-1][-1].append(checkbutton)

                nombreStat = GuiManager.generateTtkWidget(u"Entry", frame, u"grid", k+1, 1, width=50)
                gui.entries["nombreStat"][-1][-1].append(nombreStat)

                maxPower = GuiManager.generateTtkWidget(u"CheckButton", frame, u"grid", k+1, 2)
                gui.checkbuttons["maxPower"][-1][-1].append(maxPower)

                barrasKiMenus = GuiManager.generateTtkWidget(u"Combobox", frame, u"grid", k+1, 3, values=list(range(6)),
                                                             current=0, command=commandCombo)
                gui.comboboxs["barrasKiMenus"][-1][-1].append(barrasKiMenus)

                reservaKi = GuiManager.generateTtkWidget(u"Combobox", frame, u"grid", k+1, 4, values=list(range(8)),
                                                         current=0, command=commandCombo)
                gui.comboboxs["reservaKi"][-1][-1].append(reservaKi)

                showData = GuiManager.generateTtkWidget(u"Button", frame, u"grid", k+1, 5,
                                                        text=u"[WIP]" + menus_data + u" " + str(k + 1))
                gui.buttons["showData"][-1][-1].append(showData)

            frame.bind("<Configure>", functools.partial(updateScrollbar, canvas, width=860, height=yPoss[-1]-100))

        menuNameTab.grid(column=0, row=0)

    newTabs.grid(column=0, row=0)

    language.close()

    return 900, yPoss[-1]


def optionsTab(gui, tab, conf):
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

    language = LanguageManager.LanguageManager(conf["language"])
    general_language = language.getLanguageData("general_language")
    general_confirm = language.getLanguageData("general_confirm")
    general_cancel = language.getLanguageData("general_cancel")
    general_undo = language.getLanguageData("general_undo")
    language.close()

    xPoss = [x*150 + 30 for x in range(0, 10)]
    yPoss = [y*30 + 25 for y in range(0, 10)]

    gui.comboboxs["lang"] = list()
    gui.buttons["optionsConfirm"] = list()

    GuiManager.generateTtkWidget(u"Label", tab, u"place", xPoss[0], yPoss[0], text=general_language)

    langCombo = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[0], yPoss[1], width=150)
    gui.comboboxs["lang"].append(langCombo)

    confirmOptions = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[4], width=150,
                                                  text=general_confirm)
    confirmOptions["state"] = "normal"
    gui.buttons["optionsConfirm"].append(confirmOptions)

    confirmOptions = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[5], width=150,
                                                  text=general_cancel)
    confirmOptions["state"] = "normal"
    gui.buttons["optionsConfirm"].append(confirmOptions)

    confirmOptions = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[6], width=150,
                                                  text=general_undo)
    confirmOptions["state"] = "normal"
    gui.buttons["optionsConfirm"].append(confirmOptions)

    return xPoss[1] + 30, yPoss[8]


def statCharsTab(gui, tab, conf):
    # type: (GuiManager.GuiManager, ttk.Frame, OptionsManager.OptionsManager) -> (int, int)

    # language = LanguageManager.LanguageManager(conf["language"])
    # general_language = language.getLanguageData("general_language")
    # general_confirm = language.getLanguageData("general_confirm")
    # general_cancel = language.getLanguageData("general_cancel")
    # general_undo = language.getLanguageData("general_undo")
    statChars_enableCheck = "Activar"
    statChars_statType = ["Texto", '!1#', '!2#', '!8#', '!4#', '!D#']
    statChars_checkText = "Letras rojas"
    statChars_updateButton = "Actualizar datos"
    statChars_closeButton = "Cancelar"
    # language.close()

    xPoss = [x*120 + 30 for x in range(10)]
    yPoss = [y*30 + 25 for y in range(10)]

    gui.checkbuttons["statCharsEnable"] = list()
    gui.comboboxs["statChars"] = list()
    gui.checkbuttons["statChars"] = list()
    gui.entries["statChars"] = list()
    gui.buttons["statChars"] = list()

    for i in range(8):
        checkActivo = GuiManager.generateTtkWidget(u"CheckButton", tab, u"place", xPoss[0], yPoss[i],
                                                   text=statChars_enableCheck)
        gui.checkbuttons["statCharsEnable"].append(checkActivo)

        tipoEntrada = GuiManager.generateTtkWidget(u"Combobox", tab, u"place", xPoss[1], yPoss[i],
                                                   values=statChars_statType, width=100)
        gui.comboboxs["statChars"].append(tipoEntrada)

        checkEntrada = GuiManager.generateTtkWidget(u"CheckButton", tab, u"place", xPoss[2], yPoss[i],
                                                   text=statChars_checkText)
        gui.checkbuttons["statChars"].append(checkEntrada)

        entrada = GuiManager.generateTtkWidget(u"Entry", tab, u"place", xPoss[3], yPoss[i], width=200)
        gui.entries["statChars"].append(entrada)

    acceptButton = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[0], yPoss[8],
                                                text=statChars_updateButton)
    gui.buttons["statChars"].append(acceptButton)

    cancelButton = GuiManager.generateTtkWidget(u"Button", tab, u"place", xPoss[2], yPoss[8],
                                                text=statChars_closeButton)
    gui.buttons["statChars"].append(cancelButton)

    return xPoss[5], yPoss[-1] + 25
