cimport TransformClass
cimport FusionClass
cimport CharacterMenu
# cimport Constants

cdef tuple getTransformData(str archivo, int pointerFile)
    # type: (str, int) -> (TransformClass.TransformClass, int)

cdef tuple getFusionData(str archivo, int pointerFile)
    # type: (str, int) -> (FusionClass.FusionClass, int)

cdef CharacterMenu.CharacterMenu getMenusData(str archivo, int pointerFile)
    # type: (str, int) -> CharacterMenu.CharacterMenu

cdef tuple setTransformData(str archivo, int pointerFile, list transLines)
    # type: (str, int, list) -> (str, int)

cdef tuple setFusionData(str archivo, int pointerFile, str fusionLine)
    # type: (str, int, str) -> (str, int)

cdef list findDataPos(str archivo, str data, int maxi)
    # type: (str, str, int) -> list

cdef class CharacterUnkParser:
    # cdef public
    # cdef readonly
    cdef unicode filename
    cdef str fullFile
    cdef public list menusList
    cdef public TransformClass.TransformClass transObj
    cdef public FusionClass.FusionClass fusionObj

    cpdef parse(self)
        # type: () -> None

    cdef updateFileData(self, CharacterUnkParser src)
        # type: (CharacterUnkParser) -> None

    cpdef saveFile(self, unicode filename=*, CharacterUnkParser src=*)
        # type: (unicode, CharacterUnkParser) -> None

