import unittest
import string

ALL_CHARS = []
ALL_CHARS.extend(string.ascii_lowercase)
ALL_CHARS.extend(string.ascii_uppercase)


def calc_priority(char):
    return ALL_CHARS.index(char) + 1


def split_list(a_list):
    length = len(a_list)
    middle_index = length // 2
    first_half = a_list[:middle_index]
    second_half = a_list[middle_index:]
    return first_half, second_half


def find_common_item(line):
    line = line.strip()
    first_compartment, second_compartment = split_list(line)
    common_item_list = list(set(first_compartment).intersection(second_compartment))
    return common_item_list[0]


def read_file(fpath):
    common_item_priorities = []
    with open(fpath, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if not line:
                continue
            else:
                common_item = find_common_item(line)
                priority = calc_priority(common_item)
                common_item_priorities.append(priority)
    return common_item_priorities


class TestScore(unittest.TestCase):
    def test_priority_lowercase(self):
        self.assertEqual(calc_priority('a'), 1)
        self.assertEqual(calc_priority('z'), 26)

    def test_priority_uppercase(self):
        self.assertEqual(calc_priority('A'), 27)
        self.assertEqual(calc_priority('Z'), 52)

    def test_split_list(self):
        a_list = 'vJrwpWtwJgWrhcsFMMfFFhFp'
        first, second = split_list(a_list)
        self.assertEqual(first, 'vJrwpWtwJgWr')
        self.assertEqual(second, 'hcsFMMfFFhFp')

    def test_find_common_item(self):
        common_item = find_common_item('vJrwpWtwJgWrhcsFMMfFFhFp')
        self.assertEqual(common_item, 'p')


if __name__ == '__main__':
    priorities = read_file('input.txt')
    print(sum(priorities))
