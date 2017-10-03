from . cimport TransformClass
from . cimport FusionClass
from . cimport CharacterMenu
from . cimport Constants


cdef class CharacterUnkParser:
    cdef unicode filename
    cdef bytes fullFile
    cdef public list menusList
    cdef public TransformClass.TransformClass transObj
    cdef public FusionClass.FusionClass fusionObj
    cdef bint printData

    cdef TransformClass.TransformClass __getTransformData(self)
        # type: () -> TransformClass.TransformClass

    cdef FusionClass.FusionClass __getFusionData(self)
        # type: () -> FusionClass.FusionClass

    cdef list __getMenusData(self)
        # type: () -> list

    cpdef void parse(self)
        # type: () -> None

    cdef bytes __setTransformData(self, CharacterUnkParser src)
        # type: (CharacterUnkParser) -> bytes

    cdef bytes __setFusionData(self, CharacterUnkParser src)
        # type: (CharacterUnkParser) -> bytes

    cdef bytes __setMenuData(self, CharacterUnkParser src)
        # type: (CharacterUnkParser) -> bytes

    cdef void updateFileData(self, CharacterUnkParser src)
        # type: (CharacterUnkParser) -> None

    cpdef saveFile(self, unicode filename=*, CharacterUnkParser src=*)
        # type: (unicode, CharacterUnkParser) -> None

