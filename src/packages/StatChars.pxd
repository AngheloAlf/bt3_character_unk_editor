cimport Constants


cdef class StatChars:
    cdef str type
    cdef str textType
    cdef str text

    cpdef list getUnicodeList(self)
        # type: () -> list

    cpdef str getAsLine(self)
        # type: () -> str
