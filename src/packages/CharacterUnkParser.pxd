cimport TransformClass
cimport FusionClass
cimport CharacterMenu
# cimport Constants


cdef TransformClass.TransformClass getTransformData(str archivo, int pointerFile, bint printData)
    # type: (str, int, bool) -> TransformClass.TransformClass

cdef FusionClass.FusionClass getFusionData(str archivo, int pointerFile, bint printData)
    # type: (str, int, bool) -> FusionClass.FusionClass

cdef CharacterMenu.CharacterMenu getMenusData(str archivo, int pointerFile)
    # type: (str, int) -> CharacterMenu.CharacterMenu

cdef str setTransformData(str archivo, int pointerFile, list transLines)
    # type: (str, int, list) -> str

cdef str setFusionData(str archivo, int pointerFile, str fusionLine)
    # type: (str, int, str) -> str

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
    cdef bint printData

    cpdef parse(self)
        # type: () -> None

    cdef updateFileData(self, CharacterUnkParser src)
        # type: (CharacterUnkParser) -> None

    cpdef saveFile(self, unicode filename=*, CharacterUnkParser src=*)
        # type: (unicode, CharacterUnkParser) -> None

