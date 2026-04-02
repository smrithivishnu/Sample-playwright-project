import os
import json


class TestDataManager:
    TEST_DATA_FILE_PATH = os.path.abspath("../test_data.json")

    @staticmethod
    def get_test_data():
        """
        Reads the test_data.json file.
        Tries to read from the current directory first, then from the absolute path.
        """
        try:
            # Attempt to read from the current directory
            test_data = TestDataManager.read_file("test_data.json")
        except FileNotFoundError:
            # If not found, attempt to read from the absolute path
            test_data_file_path = TestDataManager.TEST_DATA_FILE_PATH
            test_data = TestDataManager.read_file(test_data_file_path)

        return test_data

    @staticmethod
    def get_common_info():
        """
        Retrieves common information from the test data.
        """
        test_data = TestDataManager.get_test_data()
        return test_data["common_info"]

    @staticmethod
    def read_file(file_path):
        with open(file_path, 'r') as f:
            file_data = json.load(f)
        return file_data
