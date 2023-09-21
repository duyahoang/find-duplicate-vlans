from collections import defaultdict
import unittest
from unittest.mock import patch
import argparse

def parse_vlans(vlan_string):
    if '-' in vlan_string:
        start, end = vlan_string.split('-')
        return list(range(int(start), int(end) + 1))
    else:
        return [int(vlan_string)]

def convert_vlan_range(n):
    lines = []
    vlan_ids = []
    while True:
        line = input(f'\nEnter VLAN ranges - List {n}:\n')
        if not line or line == '\n' or line == ' ':  # Stop when an empty line is entered
            break
        lines.append(line)

    if len(lines) == 0:
        return vlan_ids
    
    for line in lines:
        line = line.replace('switchport trunk allowed vlan add', '').replace('switchport trunk allowed vlan', '').replace('\n', '').strip()
        for item in line.split(','):
            vlan_ids.extend(parse_vlans(item))

    with open(f'vlans-list-{n}.txt', 'w') as file:
        for vlan in vlan_ids:
            file.write(str(vlan) + '\n')

    print(f"VLAN IDs written to vlans-list-{n}.txt")
    
    return vlan_ids

def find_duplicates(vlan_dict):
    duplicate_dict = defaultdict(list)
    keys = list(vlan_dict.keys())
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            duplicates = sorted(list(set(vlan_dict[keys[i]]) & set(vlan_dict[keys[j]])))
            if duplicates:
                duplicate_dict[(keys[i], keys[j])] = duplicates
    return duplicate_dict

def main():
    vlan_dict = {}
    list_num = 1
    
    while True:
        vlan_ids = convert_vlan_range(str(list_num))
        if not vlan_ids:
            break
        vlan_dict[f"List_{list_num}"] = vlan_ids
        list_num = list_num + 1
    
    duplicate_dict = find_duplicates(vlan_dict)
    
    if duplicate_dict:
        with open(f'duplicate-VLANs.txt', 'w') as file:
            
                print("\nDuplicate VLANs found are written to duplicate-VLANs.txt")
                for pair, vlans in duplicate_dict.items():
                    file.write(f"{pair}:" + '\n')
                    for vlan in vlans:
                        file.write(str(vlan) + '\n')
    else:
        print("\nNo duplicates found.")


class TestParseVlans(unittest.TestCase):

    def test_single_vlan(self):
        self.assertEqual(parse_vlans("1"), [1])
    
    def test_vlan_range(self):
        self.assertEqual(parse_vlans("1-3"), [1, 2, 3])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            parse_vlans("a-b")


class TestConvertVlanRange(unittest.TestCase):

    @patch('builtins.input', side_effect=['1-3,5', '6', ''])
    def test_convert_vlan_range(self, mock_input):
        self.assertEqual(convert_vlan_range("1"), [1, 2, 3, 5, 6])

    @patch('builtins.input', side_effect=['', ''])
    def test_empty_input(self, mock_input):
        self.assertEqual(convert_vlan_range("1"), [])


class TestFindDuplicates(unittest.TestCase):

    def test_no_duplicates(self):
        test_dict = {"List_1": [1, 2, 3], "List_2": [4, 5, 6]}
        self.assertEqual(find_duplicates(test_dict), {})

    def test_with_duplicates(self):
        test_dict = {"List_1": [1, 2, 3], "List_2": [3, 4, 5], "List_3": [5, 6, 7]}
        self.assertEqual(find_duplicates(test_dict), {("List_1", "List_2"): [3], ("List_2", "List_3"): [5]})

    def test_empty_dict(self):
        test_dict = {}
        self.assertEqual(find_duplicates(test_dict), {})

def parse_args():
    parser = argparse.ArgumentParser(description='Run the script with or without unittest.')
    parser.add_argument('--test', help='Run unittests', action='store_true')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        main()