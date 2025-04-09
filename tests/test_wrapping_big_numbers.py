import numpy as np
from npbuffer import NumpyCircularBuffer

b = NumpyCircularBuffer(100000,np.float32)

b.push(np.ones(60000))
assert b.get_length() == 60000

popped_data1 = b.pop(50000)
assert b.get_length() == 10000
assert popped_data1.size == 50000

b.push(np.ones(60000))
assert b.get_length() == 70000

popped_data2 = b.pop(50000)
assert b.get_length() == 20000
assert popped_data1.size == 50000