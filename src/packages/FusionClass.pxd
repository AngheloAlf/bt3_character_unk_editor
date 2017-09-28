cdef class FusionClass:
    cdef bytes barras, tipoFusion, resultado, compaAni\
    cdef list compaEquipo

    cpdef list getFusionData(self, int fusionNumb)
        # type: (int) -> list

    cpdef bint setFusionData(self, int fusionNumb, list data)
        # type: (int, list) -> bool

    cpdef bytes getAsLines(self)
        # type: () -> bytes
