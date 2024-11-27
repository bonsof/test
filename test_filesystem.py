# tests/test_filesystem.py

import unittest
from filesystem import VirtualFileSystem


class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        self.vfs = VirtualFileSystem('test_fs.tar')

    def test_list_dir(self):
        dirs, files = self.vfs.list_dir()
        self.assertIsInstance(dirs, list)
        self.assertIsInstance(files, list)

    def test_change_dir_invalid(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.change_dir('nonexistent')

    def tearDown(self):
        self.vfs.close()
