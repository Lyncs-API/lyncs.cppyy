from itertools import product
import numpy
from lyncs_cppyy import ll, cppdef, include, gbl, set_debug, lib
from lyncs_cppyy.numpy import array_to_pointers

def test_flatten_array_to_pointers():
    shape = (10,10)
    set_debug()
    arr = numpy.random.rand(*shape)
    ptrs = array_to_pointers(arr)
    
    vec = lib.flatten(ptrs, *shape)
    assert list(vec) == list(arr)
    assert vec.size() == arr.size
    
def test_array_to_pointers():
    arr = numpy.arange((10))
    ptrs = ll.array_to_pointers(arr)
    assert (arr == list(ptrs)).all()

    arr = numpy.arange((4 * 3 * 2 * 1 * 2))
    arr = arr.reshape((4, 3, 2, 1, 2))
    ptrs = ll.array_to_pointers(arr)
    ranges = product(range(4), range(3), range(2), range(1), range(2))
    for r in ranges:
        val = ptrs
        for i in r:
            val = val[i]
        assert val == arr[r]

def test_array_to_pointers():
    arr = numpy.arange((10))
    ptrs = ll.array_to_pointers(arr)
    assert (arr == list(ptrs)).all()

    arr = numpy.arange((4 * 3 * 2 * 1 * 2))
    arr = arr.reshape((4, 3, 2, 1, 2))
    ptrs = ll.array_to_pointers(arr)
    ranges = product(range(4), range(3), range(2), range(1), range(2))
    for r in ranges:
        val = ptrs
        for i in r:
            val = val[i]
        assert val == arr[r]


def test_to_pointer():
    arr = numpy.arange(10)
    ptr = ll.to_pointer(arr.__array_interface__["data"][0], "long*", size=10)
    assert (arr == list(ptr)).all()
