#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import GuiManager
import CharacterUnkParser
import StatMenu
import LanguageManager
import Tkinter
import ttk
import functools
import os
import Constants


class CharacterData:
    def __init__(self):
        self.data = None


def comboTransUpdate(event=None):
    # type: (Tkinter.Event, str) -> None
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
    # type: (Tkinter.Event) -> None
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


def menusUpdate(event=None):
    # type: (Tkinter.Event) -> None
    language = LanguageManager.LanguageManager(gui.languageFile)
    for i in range(8):
        for j in range(7):
            # print gui.entries["nombreMenu"][i][j].get()
            subMenuLoop = character.data.menusList[i].subMenus
            if j < len(subMenuLoop):
                if not subMenuLoop[j].isNone():
                    subMenuLoop[j].setMenuName(unicode(gui.entries["nombreMenu"][i][j].get()))
                    stats = subMenuLoop[j].stats
                    k0 = 0
                    for k in range(32):
                        if gui.checkbuttons["addStat"][i][j][k].is_checked():
                            nombrestat = unicode(gui.entries["nombreStat"][i][j][k].get())
                            maxPower = gui.checkbuttons["maxPower"][i][j][k].is_checked()
                            barrasKi = gui.comboboxs["barrasKiMenus"][i][j][k].get()
                            reservaKi = gui.comboboxs["reservaKi"][i][j][k].get()

                            # TODO: revisar que pasa si se quitan stats
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
    language.close()
    return


def addTrans(tab):
    # type: (ttk.Frame) -> (int, int)

    xPoss = [25, 60, 260, 330, 530, 700]
    yPoss = [30, 60, 90, 120, 180, 210]

    label = ttk.Label(tab, text="Transformacion")
    label.pack()
    label.place(x=xPoss[1], y=5)
    label = ttk.Label(tab, text="Barras")
    label.pack()
    label.place(x=xPoss[2], y=5)
    label = ttk.Label(tab, text="Animacion")
    label.pack()
    label.place(x=xPoss[3], y=5)
    label = ttk.Label(tab, text="Aura")
    label.pack()
    label.place(x=xPoss[4], y=5)
    label = ttk.Label(tab, text="Personaje Absorbido")
    label.pack()
    label.place(x=xPoss[5], y=5)

    gui.comboboxs["trans"] = list()
    gui.comboboxs["barras"] = list()
    gui.comboboxs["ani"] = list()
    gui.comboboxs["aura"] = list()
    gui.comboboxs["absor"] = list()

    language = LanguageManager.LanguageManager(gui.languageFile)

    for i in range(4):
        label = ttk.Label(tab, text=str(i + 1) + ": ")
        label.pack()
        label.place(x=xPoss[0], y=yPoss[i])

        trans = ttk.Combobox(tab, state='disabled')
        # trans['values'] = range(256)
        trans['values'] = map(lambda x: x[1], language.getCharactersNames())
        trans.bind("<<ComboboxSelected>>", comboTransUpdate)
        # trans.current(0)
        trans.pack()
        trans.place(x=xPoss[1], y=yPoss[i], width=180)
        gui.comboboxs["trans"].append(trans)

        barras = ttk.Combobox(tab, state='disabled')
        barras['values'] = range(8)
        barras.bind("<<ComboboxSelected>>", comboTransUpdate)
        # barras.current(0)
        barras.pack()
        barras.place(x=xPoss[2], y=yPoss[i], width=50)
        gui.comboboxs["barras"].append(barras)

        ani = ttk.Combobox(tab, state='disabled')
        ani['values'] = map(lambda x: x[1], language.getAnimations())
        ani.bind("<<ComboboxSelected>>", comboTransUpdate)
        # ani.current(0)
        ani.pack()
        ani.place(x=xPoss[3], y=yPoss[i], width=180)
        gui.comboboxs["ani"].append(ani)

        aura = ttk.Combobox(tab, state='disabled')
        aura['values'] = map(lambda x: x[1], language.getAuras())
        aura.bind("<<ComboboxSelected>>", comboTransUpdate)
        # aura.current(0)
        aura.pack()
        aura.place(x=xPoss[4], y=yPoss[i], width=150)
        gui.comboboxs["aura"].append(aura)

        absor = ttk.Combobox(tab, state='disabled')
        absor['values'] = map(lambda x: x[1], language.getCharactersNames())
        absor.bind("<<ComboboxSelected>>", comboTransUpdate)
        # absor.current(0)
        absor.pack()
        absor.place(x=xPoss[5], y=yPoss[i], width=180)
        gui.comboboxs["absor"].append(absor)

    label = ttk.Label(tab, text="Al apretar R3: ")
    label.pack()
    label.place(x=25, y=180)

    comboR3 = ttk.Combobox(tab, state='disabled')
    comboR3['values'] = map(lambda x: x[1], language.getR3Command())
    comboR3.bind("<<ComboboxSelected>>", comboTransUpdate)
    # comboR3.current(0)
    comboR3.pack()
    comboR3.place(x=180, y=180, width=210)
    gui.comboboxs["R3"] = comboR3

    label = ttk.Label(tab, text="Bonus de transformacion: ")
    label.pack()
    label.place(x=25, y=210)

    bonus = ttk.Combobox(tab, state='disabled')
    bonus['values'] = map(lambda x: x[1], language.getTransformationBonus())
    bonus.bind("<<ComboboxSelected>>", comboTransUpdate)
    # comboR3.current(0)
    bonus.pack()
    bonus.place(x=180, y=210, width=210)
    gui.comboboxs["bonus"] = bonus

    language.close()
    return xPoss[-1] + 200, yPoss[-1] + 60


def addFusion(tab):
    # type: (ttk.Frame) -> tuple
    newTabs = ttk.Notebook(tab)

    xPoss = [40, 110, 240, 440, 40, 240, 440, 640]
    yPoss = [10, 35, 75, 100]
    language = LanguageManager.LanguageManager(gui.languageFile)

    gui.comboboxs["fusBarras"] = list()
    gui.comboboxs["fusType"] = list()
    gui.comboboxs["fusResul"] = list()
    gui.comboboxs["fusCompa"] = list()
    gui.comboboxs["fusEquipo"] = [list(), list(), list()]

    charactersNames = map(lambda x: x[1], language.getCharactersNames())

    for i in range(3):
        i += 1
        subTab = ttk.Frame(newTabs, width=900, height=yPoss[-1] + 60)
        newTabs.add(subTab, text="Fusion " + str(i))

        label = ttk.Label(subTab, text="Barras")
        label.pack()
        label.place(x=xPoss[0], y=yPoss[0])

        fusBarras = ttk.Combobox(subTab, state='disabled')
        fusBarras['values'] = range(8)
        fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusBarras.pack()
        fusBarras.place(x=xPoss[0], y=yPoss[1], width=50)
        gui.comboboxs["fusBarras"].append(fusBarras)

        label = ttk.Label(subTab, text="Tipo de fusion")
        label.pack()
        label.place(x=xPoss[1], y=yPoss[0])

        fusType = ttk.Combobox(subTab, state='disabled')
        fusType['values'] = map(lambda x: x[1], language.getFusionsTypes())
        fusType.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusType.pack()
        fusType.place(x=xPoss[1], y=yPoss[1], width=110)
        gui.comboboxs["fusType"].append(fusType)

        label = ttk.Label(subTab, text="Personaje resultante de la fusion")
        label.pack()
        label.place(x=xPoss[2], y=yPoss[0])

        fusResul = ttk.Combobox(subTab, state='disabled')
        fusResul['values'] = charactersNames
        fusResul.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusResul.pack()
        fusResul.place(x=xPoss[2], y=yPoss[1], width=180)
        gui.comboboxs["fusResul"].append(fusResul)

        label = ttk.Label(subTab, text="Compañero en la animacion")
        label.pack()
        label.place(x=xPoss[3], y=yPoss[0])

        fusCompa = ttk.Combobox(subTab, state='disabled')
        fusCompa['values'] = charactersNames
        fusCompa.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusCompa.pack()
        fusCompa.place(x=xPoss[3], y=yPoss[1], width=180)
        gui.comboboxs["fusCompa"].append(fusCompa)

        for j in range(4):
            j += 1
            label = ttk.Label(subTab, text="Compañero " + str(j) + " en el equipo ")
            label.pack()
            label.place(x=xPoss[3 + j], y=yPoss[2])

            fusEquipo = ttk.Combobox(subTab, state='disabled')
            fusEquipo['values'] = charactersNames
            fusEquipo.bind("<<ComboboxSelected>>", comboFusUpdate)
            fusEquipo.pack()
            fusEquipo.place(x=xPoss[3 + j], y=yPoss[3], width=180)
            gui.comboboxs["fusEquipo"][i - 1].append(fusEquipo)

    language.close()

    newTabs.grid(column=0, row=0)

    return xPoss[-1] + 200, yPoss[-1] + 60


def updateScrollbar(canvas, event, width=200, height=100):
    canvas.configure(scrollregion=canvas.bbox("all"), width=width, height=height)


def onActiveRowClick(button, pos):
    # type: (GuiManager.MyCheckButton, tuple) -> None
    i, j, k = pos
    if button.is_checked():
        gui.entries["nombreStat"][i][j][k]["state"] = "normal"
        gui.checkbuttons["maxPower"][i][j][k]["state"] = "normal"
        gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "readonly"
        gui.comboboxs["reservaKi"][i][j][k]["state"] = "readonly"
        gui.buttons["showData"][i][j][k]["state"] = "normal"
    else:
        gui.entries["nombreStat"][i][j][k]["state"] = "disabled"
        gui.checkbuttons["maxPower"][i][j][k]["state"] = "disabled"
        gui.comboboxs["barrasKiMenus"][i][j][k]["state"] = "disabled"
        gui.comboboxs["reservaKi"][i][j][k]["state"] = "disabled"
        gui.buttons["showData"][i][j][k]["state"] = "disabled"


def addMenusTab(tab):
    # type: (ttk.Frame, str) -> (int, int)
    newTabs = ttk.Notebook(tab)

    # xPoss = [20, 110, 240, 440, 40, 240, 440, 640]
    # yPoss = [10, 30, 75, 100]
    xPoss = [5, 20, 180, 240, 440, 40, 240, 440, 640]
    yPoss = [0, 20, 50, 100, 200]
    language = LanguageManager.LanguageManager(gui.languageFile)

    gui.entries["nombreMenu"] = list()
    gui.entries["nombreStat"] = list()
    gui.checkbuttons["addStat"] = list()
    gui.comboboxs["dragonballIcon"] = list()

    gui.checkbuttons["maxPower"] = list()
    gui.comboboxs["barrasKiMenus"] = list()
    gui.comboboxs["reservaKi"] = list()

    gui.buttons["showData"] = list()

    for i in range(8):
        subTab = ttk.Frame(newTabs, width=900, height=yPoss[-1] + 60)
        newTabs.add(subTab, text=u"Idioma " + unicode(i+1))

        menuNameTab = ttk.Notebook(subTab)
        gui.entries["nombreMenu"].append(list())
        gui.entries["nombreStat"].append(list())
        gui.checkbuttons["addStat"].append(list())
        gui.comboboxs["dragonballIcon"].append(list())

        gui.checkbuttons["maxPower"].append(list())
        gui.comboboxs["barrasKiMenus"].append(list())
        gui.comboboxs["reservaKi"].append(list())

        gui.buttons["showData"].append(list())

        for j in range(7):
            menuTab = ttk.Frame(newTabs, width=900, height=yPoss[-1] + 60)
            menuNameTab.add(menuTab, text=u"Menu " + unicode(j+1))

            nameTab = ttk.LabelFrame(menuTab, width=880, height=70)
            nameTab.pack()
            nameTab.place(x=10, y=0)

            label = ttk.Label(nameTab, text=u"Nombre del menú")
            label.pack()
            label.place(x=xPoss[1], y=yPoss[0])

            nombreMenu = ttk.Entry(nameTab, state="disabled")
            # fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
            nombreMenu.pack()
            nombreMenu.place(x=xPoss[1], y=yPoss[1], width=150)
            # comboboxs["fusBarras"].append(fusBarras)
            gui.entries["nombreMenu"][-1].append(nombreMenu)

            # label = ttk.Label(nameTab, text="Icono esfera dragon")
            # label.pack()
            # label.place(x=xPoss[2], y=yPoss[0])

            # dragonballIcon = ttk.Combobox(nameTab, state="disabled")
            # dragonballIcon["values"] = range(7)
            # fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
            # dragonballIcon.pack()
            # dragonballIcon.place(x=xPoss[2], y=yPoss[1], width=150)
            # gui.comboboxs["dragonballIcon"][-1].append(dragonballIcon)

            gui.entries["nombreStat"][-1].append(list())
            gui.checkbuttons["addStat"][-1].append(list())

            gui.checkbuttons["maxPower"][-1].append(list())
            gui.comboboxs["barrasKiMenus"][-1].append(list())
            gui.comboboxs["reservaKi"][-1].append(list())

            gui.buttons["showData"][-1].append(list())

            myframe = ttk.Frame(menuTab, width=880, height=200)
            myframe.place(x=10, y=80)

            canvas = Tkinter.Canvas(myframe)
            frame = ttk.Frame(canvas)
            myscrollbar = ttk.Scrollbar(myframe, orient="vertical", command=canvas.yview)
            canvas.configure(yscrollcommand=myscrollbar.set)

            myscrollbar.pack(side="right", fill="y")
            myscrollbar.config(command=canvas.yview)
            canvas.pack(side="left")
            canvas.create_window((0, 1), window=frame, anchor='nw')

            ttk.Label(frame, text="Activo").grid(row=0, column=0)
            ttk.Label(frame, text="Nombre").grid(row=0, column=1)
            ttk.Label(frame, text="Max. Power").grid(row=0, column=2)
            ttk.Label(frame, text="Barras de Ki ocupadas").grid(row=0, column=3)
            ttk.Label(frame, text="Reservas de Ki ocupadas").grid(row=0, column=4)

            for k in range(32):
                checkbutton = GuiManager.MyCheckButton(frame, text=str(k + 1), onvalue=1, offvalue=0) # , state="disabled")
                checkbutton.deselect()
                # label = ttk.Label(frame, text=str(k+1))
                # label.pack()
                # label.place(x = xPoss[0], y=yPoss[2] + k*23)
                # label.grid(row=k, column=0)
                checkbutton.grid(row=k + 1, column=0)
                checkbutton["command"] = functools.partial(onActiveRowClick, checkbutton, (i, j, k))
                gui.checkbuttons["addStat"][-1][-1].append(checkbutton)

                nombreStat = ttk.Entry(frame, state="disabled", width=50)
                # fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
                # nombreStat.pack()
                # nombreStat.place(x = xPoss[1], y = yPoss[2] + k*23, width = 150)
                nombreStat.grid(row=k + 1, column=1)
                # comboboxs["fusBarras"].append(fusBarras)
                gui.entries["nombreStat"][-1][-1].append(nombreStat)

                maxPower = GuiManager.MyCheckButton(frame, onvalue=1, offvalue=0, state="disabled")
                maxPower.deselect()
                maxPower.grid(row=k + 1, column=2)
                gui.checkbuttons["maxPower"][-1][-1].append(maxPower)

                barrasKiMenus = ttk.Combobox(frame, state="disabled")
                barrasKiMenus["values"] = range(6)
                barrasKiMenus.grid(row=k + 1, column=3)
                barrasKiMenus.current(0)
                gui.comboboxs["barrasKiMenus"][-1][-1].append(barrasKiMenus)

                reservaKi = ttk.Combobox(frame, state="disabled")
                reservaKi["values"] = range(8)
                reservaKi.grid(row=k + 1, column=4)
                reservaKi.current(0)
                gui.comboboxs["reservaKi"][-1][-1].append(reservaKi)

                showData = ttk.Button(frame, text="[WIP]Ver data " + str(k + 1), state="disabled")
                showData.grid(row=k + 1, column=5)
                gui.buttons["showData"][-1][-1].append(showData)

            frame.bind("<Configure>", functools.partial(updateScrollbar, canvas, width=860, height=160))

        menuNameTab.grid(column=0, row=0)

    language.close()

    newTabs.grid(column=0, row=0)

    return 900, yPoss[-1] + 60


def parseUnkFile(fileName):
    # type: (unicode) -> None
    if not fileName:
        return
    character.data = CharacterUnkParser.CharacterUnkParser(fileName, True)
    # threading.Thread(target=updateGui, args=[languageFile]).start()
    # updateGui(languageFile)

    try:
        character.data.parse()
        updateTransformations()
        updateFusions()
        updateMenus()
    except Exception as err:
        print err
        GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado.\n")
        raise

    # trans = threading.Thread(target=updateTransformations)
    # fus = threading.Thread(target=updateFusions)
    # men = threading.Thread(target=updateMenus)
    # trans.start()
    # fus.start()
    # men.start()
    # threading.Thread(target=threadsStop, args=[trans, fus, men]).start()
    # if comboboxs or entries or checkbuttons or buttons:
    # character.data.parse(gui)
    # language = LanguageManager(languageFile)
    # trans = threading.Thread(target=updateTransformations, args=[comboboxs, entries, checkbuttons, buttons])
    # fus = threading.Thread(target=updateFusions, args=[comboboxs, entries, checkbuttons, buttons])
    # men = threading.Thread(target=updateMenus, args=[comboboxs, entries, checkbuttons, buttons])
    # trans.start()
    # fus.start()
    # men.start()
    # threading.Thread(target=threadsStop, args=[trans, fus, men]).start()


def threadsStop(*args):
    while True:
        a = 0
        for i in args:
            if not i.isAlive():
                a += 1
        if a == len(args):
            break
    print "t ready"


def popData(data):
    # type: (list) -> None
    pop = Tkinter.Toplevel()
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
    print "trans ready"


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
    print "fus ready"


def updateMenus():
    language = LanguageManager.LanguageManager(gui.languageFile)
    i = 0
    for menu in character.data.menusList:
        if menu.isKnow():
            # print unicode(menu.getAsLine(), "utf-16")
            if i >= len(gui.entries["nombreMenu"]):
                print "ERROR: Mas idiomas de lo esperado"
                break

            j = 0
            for submenu in menu.subMenus:
                if not submenu.isNone():
                    if j >= len(gui.entries["nombreMenu"][i]):
                        print "ERROR: Mas menus de lo esperado"
                        break

                    # menuNum = int(submenu.getMenuNum())
                    menuName = submenu.getMenuName()
                    # print unicode(submenu.getAsLine(), "utf-16")

                    # print menuNum, menuName

                    gui.entries["nombreMenu"][i][j]["state"] = "normal"
                    gui.entries["nombreMenu"][i][j].delete(0, "end")
                    gui.entries["nombreMenu"][i][j].insert("end", menuName)
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
                        # print unicode(stat.getAsLine(), "utf-16")
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
                        # for debugeando in stat.getStatChars():
                        #    if debugeando[0] not in debug:
                        #        debug[debugeando[0]] = set()
                        #    debug[debugeando[0]].add(debugeando[1][0])
                        # print len(stat.getStatChars())
                        # if len(stat.getStatChars())>5:
                        #    print "WEA"

                        k += 1
                        k0 += 1
                    while k0 < 32:
                        # gui.checkbuttons["addStat"][i][j][k0]["state"] = "normal"
                        gui.checkbuttons["addStat"][i][j][k0].deselect()
                        gui.checkbuttons["maxPower"][i][j][k0].deselect()
                        gui.buttons["showData"][i][j][k0]["state"] = "disabled"
                        gui.checkbuttons["maxPower"][i][j][k0]["state"] = "disabled"
                        gui.buttons["showData"][i][j][k0]["command"] = functools.partial(popData, list())
                        gui.buttons["showData"][i][j][k0]["state"] = "disabled"
                        k0 += 1
                    if statsInesperados:
                        print "Error: Mas stats que los esperados:", k
                    j += 1
            i += 1
    language.close()
    print "menus ready"


#
# def updateGui(languageFile="spanish.db"):
#     # type: (str) -> None
#     character.data.parse()
#     trans = threading.Thread(target=updateTransformations)
#     fus = threading.Thread(target=updateFusions)
#     men = threading.Thread(target=updateMenus)
#     trans.start()
#     fus.start()
#     men.start()
#     threading.Thread(target=threadsStop, args=[trans, fus, men]).start()
#     print "Ready"
#     return


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
            print err
            GuiManager.popupError(u"Acción fallida.", u"Ha ocurrido un error inesperado.\n")
            raise
        # threading.Thread(character.data.saveFile, args=[]).start()
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
        print err
        GuiManager.popupError(u"Acción fallida", u"Ha ocurrido un error inesperado.\nSu archivo no ha sido guardado.")
        raise
    # threading.Thread(target=character.data.saveFile, args=[fileName]).start()


def saveAsUnkFileCaller():
    if character.data:
        gui.saveFile(u"Guardar archivo", fileTypes, saveAsUnkFile)
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
            print (arch, )
            personaje = CharacterUnkParser.CharacterUnkParser(arch)
            personaje.parse()
            personaje.saveFile(src=character.data)
        GuiManager.popupInfo(u"Acción completada", u"Archivos actualizados satisfactoriamente")
    except Exception as err:
        print err
        texto = u"Ha ocurrido un error inesperado.\nQuizas intentaste actualizar un archivo que no es de personaje."
        GuiManager.popupError(u"Acción fallida", texto)
        # raise


def updateMultiplesUnkFilesCaller():
    # type: () -> None
    if character.data:
        gui.selectMultiplesFiles(u"Seleccionar archivos", fileTypes, updateMultiplesUnkFiles)
    else:
        GuiManager.popupWarning(u"Acción fallida", u"Debe abrir un archivo primero.")


def acercaDe():
    # type: () -> None
    titulo = u"Acerca de"
    texto = u"BT3 Character 'unk' Editor v" + Constants.Version + u".\nCreado por AngheloAlf"
    GuiManager.popupInfo(titulo, texto)


character = CharacterData()
title = u"BT3 Character 'unk' Editor v"+Constants.Version
gui = GuiManager.GuiManager(title, icon=os.path.join(u"resources", u"icon.ico"))
fileTypes = ((u"Archivos 'unk' de personajes", u"*.unk"), (u"Todos los archivos", u"*.*"))


def main():
    while True:
        menuAbrir = functools.partial(gui.openFile, u"Abrir archivo", fileTypes, parseUnkFile)
        menuCarpeta = functools.partial(gui.selectFolder, u"Selecciona carpeta de archivos 'unk' de personajes.")

        print 3
        gui.addMenu(["Archivo", "Opciones", "Ayuda"],
                    [
                        [("Abrir", menuAbrir),
                         ("Guardar", saveFile),
                         ("Guardar como...", saveAsUnkFileCaller),
                         ("Aplicar cambios a muchos '.unk'", updateMultiplesUnkFilesCaller),
                         ("[WIP]Aplicar a todos los '.unk' en capeta", menuCarpeta),
                         (None, None),
                         ("Salir", gui.quit)],
                        [("[WIP]Idioma", None)],
                        [("Acerca de", acercaDe)]
                    ])

        print 4
        gui.addTab(u"Transformaciones", addTrans)
        gui.addTab(u"Fusiones", addFusion)
        gui.addTab(u"Menus", addMenusTab)
        # gui.putProgressBar(20)
        print 5
        gui.start()

        if not gui.isRestart():
            break
