cdef class FusionClass:
    cdef list barras, tipoFusion, resultado, compaAni, compaEquipo

    cpdef list getFusionData(self, int fusionNumb, bint asOrd=*)
        # type: (int, bool) -> list

    cpdef bint setFusionData(self, int fusionNumb, list data, bint asOrd=*)
        # type: (int, list, bool) -> bool

    cpdef str getAsLines(self)
        # type: () -> str
