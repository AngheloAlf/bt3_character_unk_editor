from . cimport TransformClass
from . cimport FusionClass
from . cimport CharacterMenu
from . cimport Constants


cdef TransformClass.TransformClass getTransformData(bytes archivo, int pointerFile, bint printData)
    # type: (str, int, bool) -> TransformClass.TransformClass

cdef FusionClass.FusionClass getFusionData(bytes archivo, int pointerFile, bint printData)
    # type: (str, int, bool) -> FusionClass.FusionClass

cdef CharacterMenu.CharacterMenu getMenusData(bytes archivo, int pointerFile)
    # type: (str, int) -> CharacterMenu.CharacterMenu

cdef bytes setTransformData(bytes archivo, int pointerFile, list transLines)
    # type: (str, int, list) -> str

cdef bytes setFusionData(bytes archivo, int pointerFile, bytes fusionLine)
    # type: (str, int, str) -> str

cdef class CharacterUnkParser:
    # cdef public
    # cdef readonly
    cdef unicode filename
    cdef bytes fullFile
    cdef public list menusList
    cdef public TransformClass.TransformClass transObj
    cdef public FusionClass.FusionClass fusionObj
    cdef bint printData

    cpdef void parse(self)
        # type: () -> None

    cdef void updateFileData(self, CharacterUnkParser src)
        # type: (CharacterUnkParser) -> None

    cpdef saveFile(self, unicode filename=*, CharacterUnkParser src=*)
        # type: (unicode, CharacterUnkParser) -> None

