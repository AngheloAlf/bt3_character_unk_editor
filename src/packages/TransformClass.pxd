cdef class TransformClass:
    cdef bytes unknowFirst
    cdef bytes trans, barras, aniCam, aura, abs
    cdef bytes command, bonus

    cpdef int getR3Command(self)
        # type: () -> int

    cpdef bint setR3Command(self, int command)
        # type: (int) -> bool

    cpdef list getTransformData(self, int charNumb)
        # type: (int) -> list

    cpdef bint setTransformData(self, int charNumb, list data)
        # type: (int, list) -> bool

    cpdef int getBonus(self)
        # type: () -> int

    cpdef bint setBonus(self, int bonus)
        # type: (int) -> bool

    cpdef list getAsLines(self)
        # type: () -> list

