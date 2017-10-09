from . cimport Constants


cdef class StatChars:
    cdef bytes type
    cdef bytes textType
    cdef bytes text
    cdef bint printData

    cpdef list getUnicodeList(self)
        # type: () -> list

    cpdef bytes getAsLine(self)
        # type: () -> str
