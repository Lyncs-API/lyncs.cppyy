from itertools import product
import numpy
from lyncs_cppyy import ll, cppdef, include, gbl, set_debug, lib
from lyncs_cppyy.numpy import array_to_pointers


def test_to_pointer():
    arr = numpy.arange(10)
    ptr = ll.to_pointer(arr.__array_interface__["data"][0], "long*", size=10)
    assert (arr == list(ptr)).all()
