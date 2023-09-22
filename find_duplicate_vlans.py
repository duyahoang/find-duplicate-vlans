from collections import defaultdict
import unittest
from unittest.mock import patch
import argparse

def parse_vlans(vlan_string):
    """Parses a VLAN string into a list of VLAN IDs."""
    if '-' in vlan_string:
        start, end = map(int, vlan_string.split('-'))
        return list(range(start, end + 1))
    return [int(vlan_string)]

def read_vlan_ranges(n):
    """Reads VLAN ranges from the user."""
    lines = []
    while True:
        line = input(f'\nEnter VLAN ranges - List {n}:\n').strip()
        if not line:
            break
        lines.append(line)
    return lines

def process_vlan_ranges(lines, n):
    """Processes VLAN ranges and writes them to a file."""
    vlan_ids = []
    for line in lines:
        cleaned_line = line.replace('switchport trunk allowed vlan add', '').replace('switchport trunk allowed vlan', '')
        for item in cleaned_line.split(','):
            vlan_ids.extend(parse_vlans(item))
    
    with open(f'vlans-list-{n}.txt', 'w') as file:
        file.writelines(f"{vlan}\n" for vlan in vlan_ids)
    
    print(f"VLAN IDs written to vlans-list-{n}.txt")
    return vlan_ids

def find_duplicates(vlan_dict):
    """Finds duplicate VLANs across different lists."""
    duplicate_dict = defaultdict(list)
    keys = list(vlan_dict.keys())
    
    for i, key1 in enumerate(keys):
        for key2 in keys[i+1:]:
            duplicates = sorted(set(vlan_dict[key1]) & set(vlan_dict[key2]))
            if duplicates:
                duplicate_dict[(key1, key2)] = duplicates
                
    return duplicate_dict

def main():
    """Main function."""
    vlan_dict = {}
    list_num = 1
    
    while True:
        lines = read_vlan_ranges(str(list_num))
        if not lines:
            break
        vlan_dict[f"List_{list_num}"] = process_vlan_ranges(lines, str(list_num))
        list_num += 1
    
    duplicate_dict = find_duplicates(vlan_dict)
    
    if duplicate_dict:
        with open(f'duplicate-VLANs.txt', 'w') as file:
            print("\nDuplicate VLANs found are written to duplicate-VLANs.txt")
            for pair, vlans in duplicate_dict.items():
                file.write(f"{pair}:\n")
                file.writelines(f"{vlan}\n" for vlan in vlans)
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


class TestProcessVlanRanges(unittest.TestCase):

    def test_process_vlan_ranges(self):
        self.assertEqual(process_vlan_ranges(['switchport trunk allowed vlan 1,2,3,5-8','switchport trunk allowed vlan add 10-13,15,16', '18,19,21-23'],"1"), [1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23])

    def test_empty_input(self):
        self.assertEqual(process_vlan_ranges([],"1"), [])


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
