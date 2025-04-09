import numpy as np
from npbuffer import NumpyCircularBuffer

b = NumpyCircularBuffer(10,np.float32)

b.push(np.zeros(6))
assert b.get_length() == 6
assert b._head == 0
assert b._tail == 6

popped_data1 = b.pop(5)
assert b.get_length() == 1
assert popped_data1.size == 5
assert b._head == 5
assert b._tail == 6

b.push(np.ones(6))
assert b.get_length() == 7
assert b._head == 5
assert b._tail == 2

popped_data2 = b.pop(5)
assert b.get_length() == 2
assert popped_data2.size == 5
assert b._head == 0
assert b._tail == 2