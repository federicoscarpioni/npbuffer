import numpy as np
from npbuffer import NumpyCircularBuffer

buffer = NumpyCircularBuffer(maxlen=10, dtype=np.int16)

# Test empty buffer
assert buffer.get_length() == 0
assert buffer.get_data().size == 0
assert buffer.empty().size == 0

# Test normal push and empty
buffer.push(np.array([1, 2, 3]))
assert np.array_equal(buffer.get_data(), np.array([1, 2, 3]))
assert np.array_equal(buffer.empty(), np.array([1, 2, 3]))

# Test overflow
buffer.push(np.array([4, 5, 6, 7, 8]))
assert np.array_equal(buffer.get_data(), np.array([4, 5, 6, 7, 8]))
assert buffer.get_length() == 5
buffer.push(np.array([9, 10]))
assert np.array_equal(buffer.get_data(), np.array([4, 5, 6, 7, 8, 9, 10]))
assert buffer.get_length() == 7

# Test circular case
buffer.push(np.array([11, 12, 13]))
assert np.array_equal(buffer.get_data(), np.array([4, 5, 6, 7, 8, 9, 10, 11, 12, 13]))
assert buffer.get_length() == 10

# Test pop
buffer.pop(2)
assert np.array_equal(buffer.get_data(), np.array([6, 7, 8, 9, 10, 11, 12, 13]))
assert buffer.get_length() == 8
