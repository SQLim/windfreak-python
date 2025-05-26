from serial import Serial


class SerialDevice:

    def __init__(self, devpath):
        self._devpath = devpath
        self._dev = None 
        self.open()

    def __del__(self):
        self.close()

    def open(self):
        if self._dev is not None:
            raise RuntimeError('Device has already been opened.')
        self._dev = Serial(port=self._devpath, timeout=10)

    def close(self):
        if self._dev is not None:
            self._dev.close()
            self._dev = None

    def write(self, attribute, *args):
        # unpacks triple (tuple with three elements), see self.API
        # _ is an ignored variable in Python (only useful for read function below)
        dtype, request, _ = self.API[attribute]

        # make sure dtype is a tuple, even if it was initially single 
        # (dtype in self.API['am_lookup_table'] is a tuple)
        dtype = dtype if isinstance(dtype, tuple) else (dtype,)
        
        # for write, except for am_lookup_table, len(args) = len(dtype) = 1
        # as for am_lookup_table, len(args) = len(dtype) = 2
        if len(args) != len(dtype):
            raise ValueError('Number of arguments and data-types are not equal.')
        
        # dt: datatype
        # ar: argument
        # If dt is not bool, convert ar to the specified data type dt (e.g., int(ar), float(ar), str(ar))
        args = ((int(ar) if dt is bool else dt(ar)) for dt, ar in zip(dtype, args))
        
        # formats request string with args, if any, and passes it to the write method
        self._write(request.format(*args))

    def read(self, attribute, *args):
        """Reads a value for a given attribute from the SerialDevice.

        Args:
            attribute (str): The name of the attribute to read from self.API dictionary. 
            *args: Arguments to be formatted into the request string.

        Returns:
            The read value, converted to the appropriate data type.

        Raises:
            ValueError: If the number of arguments does not match the
                expected number based on the attribute's data types, or if
                an invalid return value is received for a boolean type.
        """
        # unpacks triple (tuple with three elements), see self.API
        # _ is an ignored variable in Python (only useful for write function above)
        dtype, _, request = self.API[attribute] 

        # make sure dtype is a tuple, even if it was initially single 
        # (dtype in self.API['am_lookup_table'] is a tuple)
        dtype = dtype if isinstance(dtype, tuple) else (dtype,)

        # for read, except for am_lookup_table, len(args) = 0, len(args)+1 = len(dtype) = 1
        # as for am_lookup_table, len(args) = 1, len(args)+1 = len(dtype) = 2
        if len(args) + 1 != len(dtype):
            raise ValueError('Must have +1 more data-type than argument.')

        # dt: datatype
        # ar: argument
        # If dt is not bool, convert ar to the specified data type dt (e.g., int(ar), float(ar), str(ar))
        args = ((int(ar) if dt is bool else dt(ar)) for dt, ar in zip(dtype, args))
        
        # formats request string with args, if any, and passes it to the query method
        # the response from query is stored in ret (return data)
        ret = self._query(request.format(*args))

        # expected return dtype of read method is the last one (see self.API)
        dtype = dtype[-1]

        # converts str representation of 0 and 1 to int and checks for errors 
        if dtype is bool:
            ret = int(ret) 
            if ret not in (0, 1):
                raise ValueError('Invalid return value \'{}\' for type bool.'.format(ret))
        
        # returns datatype of query response
        return dtype(ret)

    def dev_clear(self):
        """ reset input and output buffer """
        self._dev.flush() # flush alone doesn't work
        self._dev.reset_input_buffer()
        self._dev.reset_output_buffer()

    def _write(self, data):
        """Write to device.

        Args:
            data (str): write data
        """
        self._dev.write(data.encode('utf-8'))

    def _read(self):
        """Read from device.

        Returns:
            str: data
        """
        rdata = self._dev.readline()
        if not rdata.endswith(b'\n'):
            raise TimeoutError('Expected newline terminator.')
        return rdata.decode('utf-8').strip()

    def _query(self, data):
        """Write to device and read response.

        Args:
            data (str): write data

        Returns:
            str: data
        """
        self._write(data)
        return self._read()

