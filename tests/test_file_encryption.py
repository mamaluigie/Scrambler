import unittest
import os

from ../file_encryption.py import duplicate_rename

class TestDuplicate_rename(unittest.TestCase):
    def test_path_exists():

        temp_file_name = "test.txt"
        expected_new_file = "test.txt1"
        directory = "."

        try:

            # Create the temp file
            temp_file = open(temp_file_name, "w")
            temp_file.close()

            # Call the function
            name = duplicate_rename(directory, temp_file_name)

            # Check that the things happened correctly
            self.assert_equal(os.path.exists(expected_new_file), True)

            # Check that the correct file was returned
            self.assert_equal(name, expected_new_file)

        except:
            # Cleanup both files if error happened
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)

            if os.path.exists(expected_new_file):
                os.remove(expected_new_file)

        # Cleanup both files after tests complete successfully
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)

        if os.path.exists(expected_new_file):
            os.remove(expected_new_file)

    def test_path_doesnt_exist():
        pass

if __name__ == '__main__':
    unittest.main()
