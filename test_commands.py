# tests/test_commands.py

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from commands import CommandHandler
from filesystem import VirtualFileSystem

class TestCommandHandler(unittest.TestCase):
    def setUp(self):
        self.vfs = VirtualFileSystem('test_fs.tar')
        self.command_handler = CommandHandler(self.vfs, 'testuser', 'localhost', 'test_log.csv')

    def tearDown(self):
        self.vfs.close()

    def test_ls(self):
        output = self.command_handler.execute('ls')
        self.assertIn('file.txt', output)
        self.assertIn('folder', output)

    def test_cd_valid(self):
        output = self.command_handler.execute('cd folder')
        self.assertEqual(output, '')
        self.assertEqual(self.vfs.cwd, 'folder')

    def test_cd_invalid(self):
        output = self.command_handler.execute('cd nonexistent')
        self.assertEqual(output, 'No such directory: nonexistent')

    def test_rev_existing_file(self):
        output = self.command_handler.execute('rev file.txt')
        expected_output = '.лйаф йовотсет отЭ'
        self.assertEqual(output.strip(), expected_output)

    def test_rev_nonexistent_file(self):
        output = self.command_handler.execute('rev nonexistent.txt')
        self.assertEqual(output.strip(), 'No such file: nonexistent.txt')

    def test_tac_existing_file(self):
        output = self.command_handler.execute('tac file.txt')
        expected_output = 'Это тестовый файл.'
        self.assertEqual(output.strip(), expected_output)

    def test_tac_nonexistent_file(self):
        output = self.command_handler.execute('tac nonexistent.txt')
        self.assertEqual(output.strip(), 'No such file: nonexistent.txt')

    def test_chmod(self):
        output = self.command_handler.execute('chmod 755 file.txt')
        self.assertEqual(output.strip(), 'Changed permissions of file.txt to 755')

    def test_chmod_missing_args(self):
        output = self.command_handler.execute('chmod 755')
        self.assertEqual(output.strip(), 'chmod: missing operand')

    def test_exit(self):
        output = self.command_handler.execute('exit')
        self.assertEqual(output.strip(), 'exit')

    def test_unknown_command(self):
        output = self.command_handler.execute('unknowncmd')
        self.assertEqual(output.strip(), 'Command not found: unknowncmd')

    # Добавьте дополнительные тесты для других команд и случаев

if __name__ == '__main__':
    unittest.main()
