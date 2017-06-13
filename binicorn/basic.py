import numpy as np
import time
import json
import os

#
#  BasicUnicorn file format
#  basename.meta: Newline delimited metadata file. First line is data row dimension, all other lines are
#                 json metadata. Each line of metadata is associated with the corresponding matrix row.
#  basename.bin: Binary representation of a single numpy matrix.
#

class BasicUnicornReader(object):
    """
    Reader for the BasicUnicorn format.
    Reads any metadata compatible with json.loads() along with corresponding matrix data.
    """
    def __init__(self, basepath, float_bytes=4):
        self._basepath = basepath
        self._float_bytes = float_bytes

        self._binf = open(basepath + ".bin", 'rb')
        self._metaf = open(basepath + ".meta", 'r')
        self._dim = int(self._metaf.readline())

    def _seek(self, index):
        """
        TODO: Implement. Easy for binary, harder for meta.
        """
        raise NotImplementedError

    def seek_reset(self):
        """
        Reset reader to first entry.
        """
        self._binf.seek(0)
        self._metaf.seek(0)

        # Read past first meta file line (only stores row dimension)
        self._metaf.readline()

    def read_entry(self):
        """
        Read a single entry from both the metadata and binary files.
        """
        line = self._metaf.readline().strip()
        if len(line) == 0:
            return None
        name = json.loads(line)
        b = self._binf.read(self._dim * self._float_bytes)
        arr = np.fromstring(b, dtype="<f" + str(self._float_bytes))
        return (name, arr)

    def generate_entries(self):
        """
        Generate entries from the unicorn files.
        """
        self.seek_reset()
        x = self.read_entry()
        while x is not None:
            yield x
            x = self.read_entry()

    def num_rows(self):
        """
        Quick, O(1) way of getting number of rows.
        """
        return int(os.path.getsize(self._basepath + ".bin") / self._dim / self._float_bytes)

    def read_all(self):
        """
        Read all metadata and binary data into memory.
        """
        meta = []
        data = np.zeros((self.num_rows(), self._dim))
        i = 0
        for entry in self.generate_entries():
            print(entry)
            meta.append(entry[0])
            data[i] = entry[1]
        return {
            "metadata": meta,
            "data": data
        }

    def close(self):
        self._binf.close()
        self._metaf.close()

class BasicUnicornWriter(object):
    """
    Writer for the BasicUnicorn format.
    Writes any metadata compatible with json.dumps() along with corresponding matrix data.
    """
    def __init__(self, basepath, append_mode=False, float_bytes=4):
        self._basepath = basepath
        self._float_bytes = float_bytes
        self._append_mode = append_mode
        mode_base = 'a' if append_mode else 'w'
        self._binf = open(basepath + ".bin", mode_base + 'b')
        self._metaf = open(basepath + ".meta", mode_base)

    def write(self, metadata, row):
        """
        Write a single entry with associated metadata to the basic unicorn files
        """
        # Write row size to metadata file if we're not appending
        if self._append_mode is False and self._metaf.tell() == 0:
            self._metaf.write(str(row.shape[0]) + "\n")
        self._metaf.write(json.dumps(metadata) + "\n")
        self._binf.write(row.tobytes())

    def close(self):
        self._binf.close()
        self._metaf.close()

def write_basic_unicorn(basename, metadata, data, verbose=True):
    """
    Export a matrix of data and associated metadata. Creates two files:
     `basename`.meta and `basename`.bin
     `metadata` consists of a list of metadata whose indices correspond to rows in `data`.
    """
    with open(basename + ".meta", 'w') as metaf:
        dim = data[0].shape[0]
        metaf.write(str(dim) + "\n")
        last_time = time.time()
        with open(basename + ".bin", 'wb') as binf:
            i = 0
            for k in metadata:
                metaf.write(json.dumps(k) + "\n")
                binf.write(data[i].tobytes())
                i += 1
                if verbose and i % 10000 == 0:
                    print("Exported total %s embeddings in %ss" % (i, time.time() - last_time))
                    last_time = time.time()
