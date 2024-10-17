import unittest
from helpers import split_dict_list


class TestHelpers(unittest.TestCase):
    def test_split_dict_list(self):
        input_list = [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Alice', 'age': 28}]
        expected_output = [[{'name': 'Alice', 'age': 25}, {'name': 'Alice', 'age': 28}], [{'name': 'Bob', 'age': 30}]]
        self.assertEqual(split_dict_list(input_list, lambda x: x['name']), expected_output)

    def test_split_dict_list_2(self):
        input_list = [{'name': 'Alice', 'age': 25}, {'name': 'Megan', 'age': 25}, {'name': 'Bob', 'age': 30}, {'name': 'Alice', 'age': 28}]
        expected_output = [[{'name': 'Alice', 'age': 25}, {'name': 'Megan', 'age': 25}], [{'name': 'Alice', 'age': 28}], [{'name': 'Bob', 'age': 30}]]
        self.assertEqual(split_dict_list(input_list, lambda x: x['age']), expected_output)