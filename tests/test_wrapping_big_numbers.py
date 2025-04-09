import numpy as np
from npbuffer import NumpyCircularBuffer

b = NumpyCircularBuffer(20000,np.float32)

b.push(np.zeros(10050))
assert b.get_length() == 10050
assert b._head == 0
assert b._tail == 10050

popped_data1 = b.pop(10000)
assert b.get_length() == 50
assert popped_data1.size == 10000
assert b._head == 10000
assert b._tail == 10050

b.push(np.ones(10050))
assert b.get_length() == 10100
assert b._head == 10000
assert b._tail == 100

popped_data2 = b.pop(10000)
assert b.get_length() == 100
print(f'Actual size is {popped_data2.size}')
assert popped_data2.size == 10000
assert b._head == 0
assert b._tail == 100