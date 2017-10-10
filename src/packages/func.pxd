from . cimport GuiManager
from . cimport CharacterUnkParser
from . cimport SubMenu
from . cimport StatMenu
from . cimport LanguageManager
from . cimport Constants
from . cimport UnkGuiGenerator
from . cimport OptionsManager


cpdef void WIP()
    # type: () -> None


cdef class UnkEditor:
    cdef unicode title
    cdef CharacterUnkParser.CharacterUnkParser unkData
    cdef OptionsManager.OptionsManager conf
    cdef unicode icon
    # cdef GuiManager.GuiManager gui
    cdef gui
    # cdef GuiManager.GuiManager subGui
    cdef subGui

    cpdef bint start(self)
        # type: () -> bool

    cpdef void startLoop(self)
        # type: () -> None

    cdef void updateTransTab(self)
        # type: () -> None

    cdef void updateFusionsTab(self)
        # type: () -> None

    cdef void updateMenusTab(self)
        # type: () -> None

    cdef void updateTransObject(self)
        # type: () -> None

    cdef void updateFusObject(self)
        # type: () -> None

    cdef void updateMenusObject(self)
        # type: () -> None

    cdef void parseUnkFile(self, unicode fileName)
        # type: (str) -> None

    cdef void saveFile(self)
        # type () -> None

    cdef void saveAsUnkFile(self, unicode fileName)
        # type: (str) -> None

    cdef void updateMultiplesUnkFiles(self, list archivos)
        # type: (list) -> None

    # TODO: Make this a class
    cdef void logData(self)
        # type: () -> None

    cdef void openFileCaller(self)
        # type: () -> None

    cdef void saveAsUnkFileCaller(self)
        # type: () -> None

    cdef void updateMultiplesUnkFilesCaller(self)
        # type: () -> None


    cdef void openFolderCaller(self)
        # type: () -> None

    cdef void undoOptionsChange(self)
        # type: () -> None

    cdef void acceptOptionsChange(self)
        # type: () -> None

    cdef void onOptionsOpen(self)
        # type: () -> None

    cdef void optionsCaller(self)
        # type: () -> None

    cdef void about(self)
        # type: () -> None

    cdef void onMainClose(self)
        # type: () -> None

    cdef void debugMain(self)
        # type: () -> None
