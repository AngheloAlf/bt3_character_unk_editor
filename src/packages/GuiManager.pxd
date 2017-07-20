cpdef popupInfo(unicode title, unicode text)
    # type: (unicode, unicode) -> None

cpdef popupWarning(title, text)
    # type: (unicode, unicode) -> None

cpdef popupError(title, text)
    # type: (unicode, unicode) -> None

cpdef addMsgToText(txtWid, str msg)
    # type: (Tkinter.Text, str) -> None

cdef class GuiManager:
    cdef gui
    # gui = Tkinter.Tk()
    cdef int tabsWidth
    cdef int tabsHeight
    cdef int panelsAmmount
    cdef int height
    cdef int width
    cdef bint running
    cdef unicode title
    cdef tabs
    # tabs = ttk.Notebook(self.gui)
    cdef dict tabsData
    cpdef public dict entries
    cpdef public dict comboboxs
    cpdef public dict checkbuttons
    cpdef public dict buttons
    cdef list progressBar
    cdef bint restart
    cpdef public unicode languageFile
    cdef unicode icon

    cpdef addTab(self, unicode tabName, tabCallback)
        # type: (unicode, (ttk.Frame, dict, dict, dict, dict)) -> None

    cpdef addMenu(self, list cascadeNames, list cascadeData)
        # type: (list, list) -> None

    cpdef dict getEntries(self)
        # type: () -> dict

    cpdef start(self, unicode title=*, unicode icon=*)
        # type: (unicode, unicode) -> None

    cpdef stop(self)
        # type: () -> None

    cpdef bint isClose(self)
        # type: () -> bool

    cpdef unicode openFile(self, unicode title, tuple fileTypes, callback=*)
        # type: (unicode, tuple, (unicode, )) -> unicode

    cpdef unicode saveFile(self, unicode title, tuple fileTypes, callback=*)
        # type: (unicode, tuple, (unicode, )) -> unicode

    cpdef list selectMultiplesFiles(self, unicode title, tuple fileTypes, callback=*)
        # type: (unicode, tuple, (unicode, )) -> list[unicode]

    cpdef unicode selectFolder(self, unicode title=*, callback=*)
        # type: (unicode, (unicode, )) -> unicode

    cpdef putProgressBar(self, int maxi)
        # type: (int) -> None

    cpdef restartProgressBar(self)
        # type: () -> None

    cpdef updateProgressBar(self)
        # type: () -> None

    cpdef bint isRestart(self)
        # type: () -> bool

    cpdef quit(self)
        # type: () -> None
