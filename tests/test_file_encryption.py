import unittest
import os

from file_encryption import duplicate_rename

class TestDuplicate_rename(unittest.TestCase):
    def test_path_exists(self):

        temp_file_name = "test.txt"
        expected_new_file = "test.txt1"
        directory = "./tests"

        # Create the temp file
        temp_file = open(os.path.join(directory, temp_file_name), "w")
        temp_file.close()

        # Call the function
        name = duplicate_rename(directory, temp_file_name)

        # Check that the correct file was returned
        self.assertEqual(name, expected_new_file)

        # Cleanup files if error happened
        if os.path.exists(os.path.join(directory, temp_file_name)):
            os.remove(os.path.join(directory, temp_file_name))

    def test_path_doesnt_exist(self):

        unexisting_file = "test.txt"
        directory = "./tests"

        name = duplicate_rename(directory, unexisting_file)

        self.assertEqual(name, unexisting_file)

if __name__ == '__main__':
    unittest.main()
