import numpy as np
from attrs import define, field

@define
class NumpyCircularBuffer:
    maxlen : int
    dtype : np.dtype
    _head : int = 0
    _tail: int = 0
    _overflown :bool = False
    _data : np.array = field() 
    @_data.default
    def _initialize_buffer(self):
        return  np.zeros(self.maxlen, dtype = self.dtype)

    def push(self, new_data: np.array):
        '''
        Append data to the buffer, overwrite on overflow is allowed.
        '''
        if new_data.size > self.maxlen:
            raise Exception('Data input is longer than buffer size. Operation not possible.')

        if self._tail + new_data.size > self.maxlen:
            # Handle overflow
            overflow = (self._tail + new_data.size) - self.maxlen
            self._data[self._tail:self.maxlen] = new_data[:self.maxlen - self._tail]
            self._data[0:overflow] = new_data[self.maxlen - self._tail:]
            self._tail = overflow
            self._head = self._tail if self._overflown else self._head  # Update head correctly
            self._overflown = True
        else:
            self._data[self._tail:self._tail + new_data.size] = new_data
            self._tail = (self._tail + new_data.size) % self.maxlen
            if self._overflown:
                self._head = self._tail if self._tail > self._head else self._head

        # Ensure _overflown is set correctly when the buffer becomes full
        if self._tail == self._head:
            self._overflown = True

    def pop(self, num_elements: int):
        '''
        Return a desired number of elements from the buffer.
        '''
        if num_elements > self.maxlen:
            raise Exception('Elements requested are more than buffer size. Operation not possible.')

        if num_elements > self.get_length():
            raise Exception('Not enough elements in the buffer!')

        # Handle full buffer case
        if self._head == self._tail and self._overflown:
            if num_elements > self.maxlen:
                raise Exception('Cannot pop more elements than the buffer size.')

        if self._head + num_elements > self.maxlen:
            # Handle wrap-around case
            overflow = (self._head + num_elements) - self.maxlen
            current_head = self._head
            self._head = overflow
            if self._head == self._tail:
                self._overflown = False  # Reset overflow flag when buffer is emptied
            return np.concatenate(
                (self._data[current_head:self.maxlen],
                 self._data[0:overflow]),
                axis=0,
            )
        else:
            # Normal case
            current_head = self._head
            self._head = (self._head + num_elements) % self.maxlen
            if self._head == self._tail:
                self._overflown = False  # Reset overflow flag when buffer is emptied
            return self._data[current_head:self._head].copy()

    def get_data(self):
        '''
        Get data from head to tail without removing them from the buffer.
        '''
        if self._head == self._tail and not self._overflown:
            # Buffer is empty
            return np.array([], dtype=self.dtype)

        if self._tail > self._head:
            return self._data[self._head:self._tail]
        else:
            return np.concatenate(
                (self._data[self._head:], self._data[:self._tail]),
                axis=0,
            )

    def empty(self):
        '''
        Get data from head to tail removing them from the buffer.
        '''
        if self._head == self._tail and not self._overflown:
            # Buffer is empty
            return np.array([], dtype=self.dtype)

        if self._tail > self._head:
            data = self._data[self._head:self._tail]
        else:
            data = np.concatenate(
                (self._data[self._head:], self._data[:self._tail]),
                axis=0,
            )
        # Reset the buffer
        self._head = self._tail
        self._overflown = False
        return data
    
    def print_status(self):
        print(f'Maximum length: {self.maxlen}')
        print(f'Head: {self._head}')
        print(f'Tail: {self._tail}')
        print(f'Elements: {self._data}')
        
    def get_length(self):
        '''
        Get the current number of elements in the buffer.
        '''
        if self._tail == self._head:
            return self.maxlen if self._overflown else 0
        elif self._tail >= self._head:
            return self._tail - self._head
        else:
            return self.maxlen - self._head + self._tail
