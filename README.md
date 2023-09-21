# VLAN Duplicate Finder

## Overview

This Python script is designed to help you find duplicate VLAN IDs (Virtual Local Area Networks) across multiple lists. The script can handle different formats for entering VLAN IDs, including separate lines formatted as seen in network switch configurations.

## Requirements

- Python 3.x

No external packages are required.

## Usage

1. Download the script.
2. Open terminal or command prompt.
3. Navigate to the directory where the script is stored.
4. Run the script by executing the command: `python find_duplicate_vlans.py` or `python3 find_duplicate_vlans.py`

### How to Enter VLAN Information

You can enter a VLAN List in multiple lines. All lines will be combined to correspond to the list. The format is as follows:

- Single VLAN IDs can be entered separated by commas (e.g., `1,2,3`).
- Ranges of VLAN IDs can also be used (e.g., `1-5` for `1,2,3,4,5`).
- Combine both methods. For example, `1,2,3,5-10` will cover `1,2,3,5,6,7,8,9,10`.

#### Special Format

You can also use the following special format that has been used in Cisco networking configuration:
```
switchport trunk allowed vlan 1-3,5,7-10
switchport trunk allowed vlan add 11-15,17,19
```
The script will remove the `switchport trunk allowed vlan` and `switchport trunk allowed vlan add` by itself and combine all vlans into one List.

Once you have entered all VLANs for one List, press Enter to move on to the next List.

When you're done entering all Lists, press Enter again to finish the input.

### Output

The program will generate two types of files:

1. `vlans-list-N.txt`: This file contains the VLAN IDs entered for the Nth list.
2. `duplicate-VLANs.txt`: This file lists the duplicate VLAN IDs across multiple lists.

For example:
```
VLAN List 1: [1, 2, 3]
VLAN List 2: [3, 4, 5]
VLAN List 3: [5, 6, 7]

Result in duplicate-VLANs.txt:
('List_1', 'List_2'):
3
('List_2', 'List_3'):
5
```

## Testing

If you are interested in running tests to verify the script is working as expected, you can do so by running the command: `python find_duplicate_vlans.py --test` or `python3 find_duplicate_vlans.py --test`

The tests are self-contained and don't require any additional setup.

## Limitations

- The script doesn't check for invalid input formats strictly. Always ensure you enter the VLAN IDs as per the recommended formats.
  
- The script assumes that you enter distinct VLAN IDs within a single list. Duplicate entries within the same list are not checked for.

## Support

If you encounter any issues or have questions, please feel free to open an issue here on GitHub.

## License

This project is open-source and available under the MIT License. See the LICENSE file for more info.
