#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import ttk
import Tkinter
import functools
import os
from LanguageManager import LanguageManager
from GuiManager import MyCheckButton

def comboTransUpdate(event, languageFile="spanish.db"):
    pass
def comboFusUpdate(event, languageFile="spanish.db"):
    pass
def menusUpdate(event, languageFile="spanish.db"):
    pass

def addTrans(tab, comboboxs, entries, checkbuttons, buttons, languageFile="spanish.db"):
    # type: (ttk.Frame) -> None

    xPoss = [25, 60, 260, 330, 530, 700]
    yPoss = [30, 60, 90, 120, 180, 210]

    label = ttk.Label(tab, text="Transformacion")
    label.pack()
    label.place(x = xPoss[1], y=5)
    label = ttk.Label(tab, text="Barras")
    label.pack()
    label.place(x = xPoss[2], y=5)
    label = ttk.Label(tab, text="Animacion")
    label.pack()
    label.place(x = xPoss[3], y=5)
    label = ttk.Label(tab, text="Aura")
    label.pack()
    label.place(x = xPoss[4], y=5)
    label = ttk.Label(tab, text="Personaje Absorbido")
    label.pack()
    label.place(x = xPoss[5], y=5)

    comboboxs["trans"] = list()
    comboboxs["barras"] = list()
    comboboxs["ani"] = list()
    comboboxs["aura"] = list()
    comboboxs["absor"] = list()

    language = LanguageManager(languageFile)

    y = 30
    for i in range(4):
        label = ttk.Label(tab, text=str(i+1)+": ")
        label.pack()
        label.place(x = xPoss[0], y=yPoss[i])

        trans = ttk.Combobox(tab, state='disabled')
        #trans['values'] = range(256)
        trans['values'] = map(lambda x: x[1], language.getCharactersNames())
        trans.bind("<<ComboboxSelected>>", comboTransUpdate)
        #trans.current(0)
        trans.pack()
        trans.place(x = xPoss[1], y = yPoss[i], width = 180)
        comboboxs["trans"].append(trans)

        barras = ttk.Combobox(tab, state='disabled')
        barras['values'] = range(7)
        barras.bind("<<ComboboxSelected>>", comboTransUpdate)
        #barras.current(0)
        barras.pack()
        barras.place(x = xPoss[2], y = yPoss[i], width = 50)
        comboboxs["barras"].append(barras)

        ani = ttk.Combobox(tab, state='disabled')
        ani['values'] = map(lambda x: x[1], language.getAnimations())
        ani.bind("<<ComboboxSelected>>", comboTransUpdate)
        #ani.current(0)
        ani.pack()
        ani.place(x = xPoss[3], y = yPoss[i], width = 180)
        comboboxs["ani"].append(ani)

        aura = ttk.Combobox(tab, state='disabled')
        aura['values'] = map(lambda x: x[1], language.getAuras())
        aura.bind("<<ComboboxSelected>>", comboTransUpdate)
        #aura.current(0)
        aura.pack()
        aura.place(x = xPoss[4], y = yPoss[i], width = 150)
        comboboxs["aura"].append(aura)

        absor = ttk.Combobox(tab, state='disabled')
        absor['values'] = map(lambda x: x[1], language.getCharactersNames())
        absor.bind("<<ComboboxSelected>>", comboTransUpdate)
        #absor.current(0)
        absor.pack()
        absor.place(x = xPoss[5], y = yPoss[i], width = 180)
        comboboxs["absor"].append(absor)

    label = ttk.Label(tab, text="Al apretar R3: ")
    label.pack()
    label.place(x = 25, y = 180)

    comboR3 = ttk.Combobox(tab, state='disabled')
    comboR3['values'] = map(lambda x: x[1], language.getR3Command())
    comboR3.bind("<<ComboboxSelected>>", comboTransUpdate)
    #comboR3.current(0)
    comboR3.pack()
    comboR3.place(x = 180, y = 180, width = 210)
    comboboxs["R3"] = comboR3


    label = ttk.Label(tab, text="Bonus de transformacion: ")
    label.pack()
    label.place(x = 25, y = 210)

    bonus = ttk.Combobox(tab, state='disabled')
    bonus['values'] = map(lambda x: x[1], language.getTransformationBonus())
    bonus.bind("<<ComboboxSelected>>", comboTransUpdate)
    #comboR3.current(0)
    bonus.pack()
    bonus.place(x = 180, y = 210, width = 210)
    comboboxs["bonus"] = bonus

    language.close()
    return (xPoss[-1]+200, yPoss[-1]+60)

def addFusion(tab, comboboxs, entries, checkbuttons, buttons, languageFile="spanish.db"):
    # type: (ttk.Frame) -> tuple
    newTabs = ttk.Notebook(tab)


    xPoss = [40, 110, 240, 440, 40, 240, 440, 640]
    yPoss = [10, 35, 75, 100]
    language = LanguageManager(languageFile)

    comboboxs["fusBarras"] = list()
    comboboxs["fusType"] = list()
    comboboxs["fusResul"] = list()
    comboboxs["fusCompa"] = list()
    comboboxs["fusEquipo"] = [list(), list(), list()]

    charactersNames = map(lambda x: x[1], language.getCharactersNames())

    for i in range(3):
        i += 1
        subTab = ttk.Frame(newTabs, width = 900, height = yPoss[-1]+60)
        newTabs.add(subTab, text="Fusion " + str(i))


        label = ttk.Label(subTab, text="Barras")
        label.pack()
        label.place(x = xPoss[0], y=yPoss[0])

        fusBarras = ttk.Combobox(subTab, state='disabled')
        fusBarras['values'] = range(7)
        fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusBarras.pack()
        fusBarras.place(x = xPoss[0], y = yPoss[1], width = 50)
        comboboxs["fusBarras"].append(fusBarras)



        label = ttk.Label(subTab, text="Tipo de fusion")
        label.pack()
        label.place(x = xPoss[1], y=yPoss[0])

        fusType = ttk.Combobox(subTab, state='disabled')
        fusType['values'] = map(lambda x: x[1], language.getFusionsTypes())
        fusType.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusType.pack()
        fusType.place(x = xPoss[1], y = yPoss[1], width = 110)
        comboboxs["fusType"].append(fusType)



        label = ttk.Label(subTab, text="Personaje resultante de la fusion")
        label.pack()
        label.place(x = xPoss[2], y=yPoss[0])

        fusResul = ttk.Combobox(subTab, state='disabled')
        fusResul['values'] = charactersNames
        fusResul.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusResul.pack()
        fusResul.place(x = xPoss[2], y = yPoss[1], width = 180)
        comboboxs["fusResul"].append(fusResul)



        label = ttk.Label(subTab, text="Compañero en la animacion")
        label.pack()
        label.place(x = xPoss[3], y=yPoss[0])

        fusCompa = ttk.Combobox(subTab, state='disabled')
        fusCompa['values'] = charactersNames
        fusCompa.bind("<<ComboboxSelected>>", comboFusUpdate)
        fusCompa.pack()
        fusCompa.place(x = xPoss[3], y = yPoss[1], width = 180)
        comboboxs["fusCompa"].append(fusCompa)


        for j in range(4):
            j += 1
            label = ttk.Label(subTab, text="Compañero " + str(j) + " en el equipo ")
            label.pack()
            label.place(x = xPoss[3+j], y=yPoss[2])

            fusEquipo = ttk.Combobox(subTab, state='disabled')
            fusEquipo['values'] = charactersNames
            fusEquipo.bind("<<ComboboxSelected>>", comboFusUpdate)
            fusEquipo.pack()
            fusEquipo.place(x = xPoss[3+j], y = yPoss[3], width = 180)
            comboboxs["fusEquipo"][i-1].append(fusEquipo)

    language.close()

    newTabs.grid(column=0, row=0)

    return (xPoss[-1]+200, yPoss[-1]+60)

def updateScrollbar(canvas, event, width=200, height=100):
    canvas.configure(scrollregion=canvas.bbox("all"),width=width,height=height)

def addMenusTab(tab, comboboxs, entries, checkbuttons, buttons, languageFile="spanish.db"):
    newTabs = ttk.Notebook(tab)

    # xPoss = [20, 110, 240, 440, 40, 240, 440, 640]
    # yPoss = [10, 30, 75, 100]
    xPoss = [5, 20, 180, 240, 440, 40, 240, 440, 640]
    yPoss = [0, 20, 50, 100, 200]
    language = LanguageManager(languageFile)

    entries["nombreMenu"] = list()
    entries["nombreStat"] = list()
    checkbuttons["addStat"] = list()
    comboboxs["dragonballIcon"] = list()

    checkbuttons["maxPower"] = list()
    comboboxs["barrasKiMenus"] = list()
    comboboxs["reservaKi"] = list()

    buttons["showData"] = list()

    for i in range(8):
        i += 1

        subTab = ttk.Frame(newTabs, width = 900, height = yPoss[-1]+60)
        newTabs.add(subTab, text="Idioma " + str(i))

        menuNameTab = ttk.Notebook(subTab)
        entries["nombreMenu"].append(list())
        entries["nombreStat"].append(list())
        checkbuttons["addStat"].append(list())
        comboboxs["dragonballIcon"].append(list())

        checkbuttons["maxPower"].append(list())
        comboboxs["barrasKiMenus"].append(list())
        comboboxs["reservaKi"].append(list())

        buttons["showData"].append(list())


        for j in range(7):
            j += 1
            menuTab = ttk.Frame(newTabs, width = 900, height = yPoss[-1]+60)
            menuNameTab.add(menuTab, text="Menu " + str(j))


            nameTab = ttk.LabelFrame(menuTab, width=880, height=70)
            nameTab.pack()
            nameTab.place(x=10, y=0)

            label = ttk.Label(nameTab, text="Nombre del menú")
            label.pack()
            label.place(x = xPoss[1], y=yPoss[0])

            nombreMenu = ttk.Entry(nameTab, state="disabled")
            #fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
            nombreMenu.pack()
            nombreMenu.place(x = xPoss[1], y = yPoss[1], width = 150)
            #comboboxs["fusBarras"].append(fusBarras)
            entries["nombreMenu"][-1].append(nombreMenu)



            label = ttk.Label(nameTab, text="Icono esfera dragon")
            label.pack()
            label.place(x = xPoss[2], y=yPoss[0])

            dragonballIcon = ttk.Combobox(nameTab, state="disabled")
            dragonballIcon["values"] = range(7)
            #fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
            dragonballIcon.pack()
            dragonballIcon.place(x = xPoss[2], y = yPoss[1], width = 150)
            comboboxs["dragonballIcon"][-1].append(dragonballIcon)
            


            entries["nombreStat"][-1].append(list())
            checkbuttons["addStat"][-1].append(list())

            checkbuttons["maxPower"][-1].append(list())
            comboboxs["barrasKiMenus"][-1].append(list())
            comboboxs["reservaKi"][-1].append(list())


            buttons["showData"][-1].append(list())

            myframe=ttk.Frame(menuTab,width=880,height=200)
            myframe.place(x=10,y=80)

            canvas=Tkinter.Canvas(myframe)
            frame=ttk.Frame(canvas)
            myscrollbar=ttk.Scrollbar(myframe,orient="vertical",command=canvas.yview)
            canvas.configure(yscrollcommand=myscrollbar.set)

            myscrollbar.pack(side="right",fill="y")
            myscrollbar.config( command = canvas.yview )
            canvas.pack(side="left")
            canvas.create_window((0,1),window=frame,anchor='nw')


            ttk.Label(frame, text="Activo").grid(row=0, column=0)
            ttk.Label(frame, text="Nombre").grid(row=0, column=1)
            ttk.Label(frame, text="Max. Power").grid(row=0, column=2)
            ttk.Label(frame, text="Barras de Ki ocupadas").grid(row=0, column=3)
            ttk.Label(frame, text="Reservas de Ki ocupadas").grid(row=0, column=4)

            for k in range(24):
                checkbutton = MyCheckButton(frame, text = str(k+1), onvalue = 1, offvalue = 0, state="disabled")
                checkbutton.deselect()
                #label = ttk.Label(frame, text=str(k+1))
                #label.pack()
                #label.place(x = xPoss[0], y=yPoss[2] + k*23)
                #label.grid(row=k, column=0)
                checkbutton.grid(row=k+1, column=0)
                checkbuttons["addStat"][-1][-1].append(checkbutton)

                nombreStat = ttk.Entry(frame, state="disabled")
                ##fusBarras.bind("<<ComboboxSelected>>", comboFusUpdate)
                #nombreStat.pack()
                #nombreStat.place(x = xPoss[1], y = yPoss[2] + k*23, width = 150)
                nombreStat.grid(row=k+1, column=1)
                ##comboboxs["fusBarras"].append(fusBarras)
                entries["nombreStat"][-1][-1].append(nombreStat)


                maxPower = MyCheckButton(frame, onvalue = 1, offvalue = 0, state="disabled")
                maxPower.deselect()
                maxPower.grid(row=k+1, column=2)
                checkbuttons["maxPower"][-1][-1].append(maxPower)

                barrasKiMenus = ttk.Combobox(frame, state="disabled")
                barrasKiMenus["values"] = range(6)
                barrasKiMenus.grid(row=k+1, column=3)
                comboboxs["barrasKiMenus"][-1][-1].append(barrasKiMenus)

                reservaKi = ttk.Combobox(frame, state="disabled")
                reservaKi["values"] = range(7)
                reservaKi.grid(row=k+1, column=4)
                comboboxs["reservaKi"][-1][-1].append(reservaKi)

                showData = ttk.Button(frame, text ="Ver data "+str(k+1), state="disabled")#, command = functools.partial(popData, stat.getStatChars()))
                showData.grid(row=k+1, column=5)
                buttons["showData"][-1][-1].append(showData)

            frame.bind("<Configure>", functools.partial(updateScrollbar, canvas, width=860, height=160))

        menuNameTab.grid(column=0, row=0)

    language.close()

    newTabs.grid(column=0, row=0)

    return (900, yPoss[-1]+60)
