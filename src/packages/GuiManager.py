import Tkinter
import ttk
import tkFileDialog
import tkMessageBox


def popUp(title, text, text2):
    # type: (str, str, str) -> None
    pop = Tkinter.Toplevel()
    pop.title(title)
    ttk.Label(pop, text=text).pack()
    ttk.Button(pop, text=text2, command=pop.destroy).pack(side=Tkinter.BOTTOM)
    return


def showPopUp(text1, text2):
    # type: (str, str) -> None
    tkMessageBox.showinfo(text1, text2)


def addMsgToText(txtWid, msg):
    # type: (Tkinter.Text, str) -> None
    txtWid["state"] = "normal"
    txtWid.insert(Tkinter.END, msg + "\n")
    txtWid.see(Tkinter.END)
    txtWid["state"] = "disabled"


class GuiManager:
    def __init__(self, title="Tk"):  # , xOffset, yOffSet):
        # type: (str) -> None
        self.gui = Tkinter.Tk()
        # self.gui.minsize(xOffset, yOffSet)
        # self.xOffset = xOffset
        # self.yOffset = yOffSet
        self.tabsWidth = 900
        self.tabsHeight = 0
        self.panelsAmmount = 0
        self.height = 0
        self.width = 210
        self.running = False
        self.title = title
        self.tabs = ttk.Notebook(self.gui)
        self.tabsData = dict()
        self.comboboxs = dict()
        self.entries = dict()
        self.checkbuttons = dict()
        self.buttons = dict()
        self.progressBar = list()
        self.restart = False

    # def addPanel(self, frameName, labels, inputs, button):
    #     # type: (str, list, list, list) -> GuiManager
    #     frame = ttk.LabelFrame(self.gui, text=frameName)
    #     frame.pack(fill="both", expand="yes", side=Tkinter.LEFT)

    #     yPos = []

    #     # inputs = [("Entry", "DefaultText")]
    #     x = 75
    #     y = 0
    #     for i in range(len(inputs)):
    #         # print inputs[i]
    #         yPos.append(y)
    #         if inputs[i][0] == "Entry":
    #             en = ttk.Entry(frame)
    #             en.insert(0, inputs[i][1])
    #             en.place(x=x, y=y)
    #             self.entries[labels[i]] = en
    #             y += 25
    #         elif inputs[i][0] == "Text":
    #             # sc = Tkinter.Scrollbar(frame)
    #             # sc.place(x=x, y=y)

    #             te = Tkinter.Text(frame, state="normal", width="38", height="12")  # , yscrollcommand = sc.set)
    #             te.insert(Tkinter.INSERT, inputs[i][1])
    #             te.place(x=x, y=y)
    #             # te.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH)
    #             self.entries[labels[i]] = te

    #             # sc.config(command = te.yview)
    #             te["state"] = "disabled"

    #             y += 200
    #             if self.width < 400:
    #                 self.width = 400

    #     # labels = ["ip", "port", "usuario"]
    #     x = 0
    #     for l in range(len(labels)):
    #         la = ttk.Label(frame, text=labels[l])
    #         la.place(x=x, y=yPos[l])
    #         # print la.winfo_width()
    #         # print la.winfo_height()
    #         # print la['width']

    #     yMax = yPos[-1] + 25

    #     # button = ["logear"]
    #     bu = ttk.Button(frame, text=button[0], command=button[1])
    #     bu.place(x=75, y=yMax+25)

    #     if yMax + 25 > self.height:
    #         self.height = yMax + 50

    #     self.panelsAmmount += 1

    #     return self

    def addTab(self, tabName, tabCallback):
        # type: (str, (ttk.Frame, dict, dict, dict, dict)) -> None
        tab = ttk.Frame(self.tabs)  # , width = self.tabsWidth, height = self.tabsHeight)
        self.tabs.add(tab, text=tabName)
        self.tabsData[tabName] = tab
        newX, newY = tabCallback(tab, self.comboboxs, self.entries, self.checkbuttons, self.buttons)

        tab["width"] = newX
        tab["height"] = newY

        if newX > self.tabsWidth:
            self.tabsWidth = newX
        if newY > self.tabsHeight:
            self.tabsHeight = newY
        return

    def addMenu(self, cascadeNames, cascadeData):
        # type: (list, list) -> None
        if len(cascadeNames) != len(cascadeData):
            return
        
        menubar = Tkinter.Menu(self.gui)

        for i in range(len(cascadeNames)):
            subMenu = Tkinter.Menu(menubar, tearoff=0)
            for optionName, callback in cascadeData[i]:
                if optionName is None:
                    subMenu.add_separator()
                else:
                    subMenu.add_command(label=optionName, command=callback)
            menubar.add_cascade(label=cascadeNames[i], menu=subMenu)

        self.gui.config(menu=menubar)

    def getEntries(self):
        # type: () -> dict
        return self.entries

    def start(self, title=None):
        # type: (str) -> None
        # if title:
            # self.title = title
        self.gui.title(self.title)
        # self.gui.minsize(self.width * self.panelsAmmount, self.height + 20 + 25)
        self.gui.minsize(self.tabsWidth, self.tabsHeight+25)
        self.running = True
        self.tabs.grid(column=0, row=0)
        print "before mainloop"
        self.gui.mainloop()

    def stop(self):
        # type: () -> None
        self.gui.destroy()
        # del self.gui
        self.entries = dict()
        self.panelsAmmount = 0
        self.height = 0
        self.gui = Tkinter.Tk()
        self.running = False

    def isClose(self):
        # type: () -> bool
        return not self.running

    def openFile(self, title, fileTypes, callback=None):
        # type: (str, tuple, (unicode, dict, dict, dict, dict)) -> unicode
        archivo = tkFileDialog.askopenfilename(initialdir="/", title=title, filetypes=fileTypes)
        try:
            print archivo
        except UnicodeEncodeError:
            pass
        if callback:
            callback(archivo, comboboxs=self.comboboxs, entries=self.entries,
                     checkbuttons=self.checkbuttons, buttons=self.buttons)
        return unicode(archivo)

    def saveFile(self, title, fileTypes, callback=None):
        # type: (str, tuple, (unicode, dict, dict, dict, dict)) -> unicode
        archivo = tkFileDialog.asksaveasfilename(initialdir="/", title=title, filetypes=fileTypes)
        try:
            print archivo
        except UnicodeEncodeError:
            pass
        if callback:
            callback(archivo, comboboxs=self.comboboxs, entries=self.entries,
                     checkbuttons=self.checkbuttons, buttons=self.buttons)
        return unicode(archivo)

    def openMultiplesFiles(self, title, fileTypes, callback=None):
        # type: (str, tuple, (unicode, dict, dict, dict, dict)) -> unicode
        archivos = tkFileDialog.askopenfilenames(initialdir="/", title=title, filetypes=fileTypes)
        try:
            print archivos
        except UnicodeEncodeError:
            pass
        if callback:
            callback(archivos, comboboxs=self.comboboxs, entries=self.entries,
                     checkbuttons=self.checkbuttons, buttons=self.buttons)
        return unicode(archivos)

    def selectFolder(self, title=None, callback=None):
        # type: (str, (unicode, dict, dict, dict, dict)) -> unicode
        carpeta = tkFileDialog.askdirectory(title=title)
        print carpeta
        if callback:
            callback(carpeta, comboboxs=self.comboboxs, entries=self.entries,
                     checkbuttons=self.checkbuttons, buttons=self.buttons)
        return unicode(carpeta)

    def putProgressBar(self, maxi):
        # type: (int) -> None
        pb = ttk.Progressbar(self.gui, orient="horizontal", length=self.tabsWidth, mode="determinate", maximum=maxi)
        pb.grid(column=0, row=1)
        self.progressBar = [pb, maxi]

    def restartProgressBar(self):
        # type: () -> None
        if self.progressBar:
            self.progressBar[0]["value"] = 0

    def updateProgressBar(self):
        # type: () -> None
        if self.progressBar is None:
            return
        if self.progressBar[0]["value"] > self.progressBar[1]:
            self.progressBar[0]["value"] = 0
        self.progressBar[0]["value"] += 1

    def isRestart(self):
        # type: () -> bool
        return self.restart

    def quit(self):
        # type: () -> None
        self.gui.quit()


class MyCheckButton(Tkinter.Checkbutton):
    def __init__(self, *args, **kwargs):
        self.var = kwargs.get('variable', Tkinter.IntVar())
        kwargs['variable'] = self.var
        Tkinter.Checkbutton.__init__(self, *args, **kwargs)

    def is_checked(self):
        return self.var.get()
