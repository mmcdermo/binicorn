import unittest
import numpy as np
from binicorn.basic import BasicUnicornWriter, BasicUnicornReader, write_basic_unicorn

class TestBasicUnicorn(unittest.TestCase):
    def setUp(self):
        self._test_n_rows = 10
        self._test_dim = 4

    def gen_data(self, basepath):
        meta = []
        for i in range(self._test_n_rows):
            meta.append("corn" + str(i))

        data = np.zeros((self._test_n_rows, self._test_dim)).astype('float32')

        return (meta, data)

    def test_read_and_write(self):
        basepath = "testpath"
        (meta, data) = self.gen_data(basepath)
        write_basic_unicorn(basepath, meta, data)
        reader = BasicUnicornReader(basepath)
        res = reader.read_all()
        reader.close()

        self.assertEqual(res["data"].shape, (self._test_n_rows, self._test_dim))
        self.assertEqual(res["metadata"][3], "corn3")

    def test_writer(self):
        basepath = "testpath"
        (meta, data) = self.gen_data(basepath)
        writer = BasicUnicornWriter(basepath)
        for row in zip(meta, data):
            writer.write(row[0], row[1])
        writer.close()
        reader = BasicUnicornReader(basepath)
        res = reader.read_all()
        reader.close()

        self.assertEqual(res["data"].shape, (self._test_n_rows, self._test_dim))
        self.assertEqual(res["metadata"][3], "corn3")


    def test_read_write_metadata_with_newlines(self):
        pass

    def test_read_write_float64_data(self):
        pass

    def test_write_unserializable_json_metadata(self):
        pass

    def test_write_unsupported_numpy_datatype(self):
        pass

    def test_read_files_do_not_exist(self):
        pass

    def test_read_invalid_metadata_file_contents(self):
        pass

    def test_read_invalid_bin_file_contents(self):
        pass

    def test_read_desynced_metadata_and_binary_contents(self):
        pass

    def test_write_out_of_disk_space(self):
        pass

    def test_write_out_of_memory(self):
        pass

    def test_read_out_of_disk_space(self):
        pass

    def test_read_out_of_memory(self):
        pass
