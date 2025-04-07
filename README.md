# npbuffer
A simple module for using a Numpy array as circular buffer.

This package consist of only one class object 'NumpyCircularBuffer' with the following
methods:
- push(), to add elements to the buffer in the form of 1D Numpy array
- pop(), to remove some of the element from the buffer 
- get_data(), to copy the elements in the buffer without altering the head/tail positions
- empty(), to remove all the element from the buffer

The implementation follows the FIFO (first in, first out) approach with a 1D array and it is not
possible to push from left, resize or any fancy remanaging. Overflow is alwasy 
active by design as well as overwriting of data not read.

This implementation was written for buffering data generated from an instrument into computer memory and periodically read (pop) and copied to another location for processing. This
approach is not efficient beacuse copying is an O(N) operation but good enough for
my projects (ex. [DEIStool](https://github.com/federicoscarpioni/DEIStools)).
For more information on the topic of implementing circualr buffers in Python I suggest
reading this threads:
[Thread 1](https://stackoverflow.com/questions/42771110/fastest-way-to-left-cycle-a-numpy-array-like-pop-push-for-a-queue/66406793#66406793),
[Thread 2](https://stackoverflow.com/questions/73342003/performant-circular-buffer-for-frames-ndarrays-of-data-samples),
[Thread 3](https://stackoverflow.com/questions/8908998/ring-buffer-with-numpy-ctypes).

For more advanced features, already exist much more complete Python packages:
- [Numpy Read Write Buffer](https://github.com/justengel/np_rw_buffer) : it is was my favorite choice but for a short time was not supporting py>3.9 so I created my simple version of it;
- [python-dvg-ringbuffer][https://github.com/Dennis-van-Gils/python-dvg-ringbuffer]: it looks complete but I didn't try it (but wanted to me mentioned in the list anyway);
- [ringbuf](https://github.com/elijahr/ringbuf?tab=readme-ov-file) : it is probably
the most mature and optimize but require installing 'Boost' (not so easy if you
work with corporate computers, I couldn't test it);
- [numpy_ringbuffer](https://github.com/eric-wieser/numpy_ringbuffer) : unfortunalty 
appends only one element at the time, not suitable for writing block of data (signals).

See also [Streaming Recording Buffer](https://github.com/mcorrig4/python-recording-buffer/tree/main).


## Example of use
```python
b = NumpyCircularBuffer(10)
    b.push(np.array([1,2,3,4,5,6,7,8,9,10]))
    print(b.get_lenght())
    b.print_status()
    b.push(np.array([11]))
    b.print_status()
    b.push(np.array([12,13,14,15,16,17]))
    print(b.get_lenght())
    b.print_status()
    print(f'Buffered data: {b.get_data()}')
```
