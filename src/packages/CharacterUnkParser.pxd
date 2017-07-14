cimport TransformClass
cimport FusionClass
# cimport GuiManager

cdef tuple getTransformData(str archivo, int pointerFile)
    # type: (str, int) -> (TransformClass.TransformClass, int)

cdef tuple getFusionData(str archivo, int pointerFile)
    # type: (str, int) -> (FusionClass.FusionClass, int)

cdef tuple getMenusData(str archivo, int pointerFile)
    # type: (str, int) -> (CharacterMenu.CharacterMenu, int)

cdef tuple setTransformData(str archivo, int pointerFile, list transLines)
    # type: (str, int, list) -> (str, int)

cdef tuple setFusionData(str archivo, int pointerFile, str fusionLine)
    # type: (str, int, str) -> (str, int)

cdef class CharacterUnkParser:
    # cdef public
    # cdef readonly
    cdef unicode filename
    cdef str fullFile
    cdef bint fastMode
    cdef float fastModeStart
    cdef public list menusList
    cdef public TransformClass.TransformClass transObj
    cdef public FusionClass.FusionClass fusionObj

    # cpdef CharacterUnkParser parse(self, GuiManager.GuiManager gui=*)
        # type: (GuiManager.GuiManager) -> CharacterUnkParser

    # cdef CharacterUnkParser updateFileData(self, GuiManager.GuiManager gui=*)
        # type: (GuiManager.GuiManager) -> CharacterUnkParser

    # cpdef CharacterUnkParser saveFile(self, str filename=*, GuiManager.GuiManager gui=*)
        # type: (str, GuiManager.GuiManager) -> CharacterUnkParser

