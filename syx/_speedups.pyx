from libc.math cimport abs, round

cpdef bankers_round(double value, ndigits=None):
    cdef bint return_int = 0
    if ndigits is None:
        ndigits = 0
        return_int = 1
    cdef double multiplier = 10 ** int(ndigits)
    cdef double large_value = value * multiplier
    cdef double remainder = large_value - (<int>large_value)
    if abs(remainder) == 0.5:
        large_value = ((<int>large_value % 2) * ((value > 0) - (value < 0))) + (<int>large_value)

    cdef double result = round(large_value) / multiplier
    if return_int:
        return int(result)
    return result
