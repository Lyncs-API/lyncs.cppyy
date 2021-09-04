import numpy
from lyncs_cppyy import ll, cppdef, include, gbl, lib
from lyncs_cppyy.numpy import dtype_map, char_map
from lyncs_cppyy.numpy import *


def test_get_ctype():
    for dtype, ctype in char_map.items():
        assert get_ctype(dtype) == ctype


def test_get_numpy_pointer():
    for dtype in char_map:
        print(dtype)
        arr = numpy.zeros((10,), dtype=dtype)
        assert (numpy.array(get_numpy_pointer(arr)) == arr).all()


def test_flatten_array_to_pointers():
    for shape in [(10,), (10, 10), (10, 10, 10), (10, 10, 10, 10)]:  #
        arr = numpy.random.rand(*shape)
        ptrs = array_to_pointers(arr)
        vec = lib.flatten(ptrs, *shape)

        assert vec.size() == arr.size
        assert numpy.allclose(arr.flatten(), numpy.array(vec))
