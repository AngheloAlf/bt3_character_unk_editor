cdef void writeDefaultOptions(openFile)
    # type: (file) -> None


cdef class OptionsManager:
    cdef unicode name
    cdef dict options

    cpdef bint checkOptions(self)
        # type: () -> bool

    cpdef void updateFile(self)
        # type: () -> None
