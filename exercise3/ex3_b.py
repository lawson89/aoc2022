import unittest
import string

ALL_CHARS = []
ALL_CHARS.extend(string.ascii_lowercase)
ALL_CHARS.extend(string.ascii_uppercase)


def calc_priority(char):
    return ALL_CHARS.index(char) + 1


def chunks(xs, n):
    n = max(1, n)
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def find_common_item(list_of_lines):
    common = set(list_of_lines[0]).intersection(list_of_lines[1])
    common = common.intersection(list_of_lines[2])
    common_item_list = list(common)
    return common_item_list[0]


def read_file(fpath):
    common_item_priorities = []
    all_lines = []
    with open(fpath, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if not line:
                continue
            else:
                all_lines.append(line)
    grouped_lists = chunks(all_lines, 3)
    for group in grouped_lists:
        common_item = find_common_item(group)
        common_item_priorities.append(calc_priority(common_item))
    return common_item_priorities


class TestScore(unittest.TestCase):
    def test_priority_lowercase(self):
        self.assertEqual(calc_priority('a'), 1)
        self.assertEqual(calc_priority('z'), 26)

    def test_priority_uppercase(self):
        self.assertEqual(calc_priority('A'), 27)
        self.assertEqual(calc_priority('Z'), 52)

    def test_chunks(self):
        a_list = [1, 2, 3, 4, 5, 6]
        chunked_lists = chunks(a_list, 3)
        self.assertEqual(chunked_lists[0], [1, 2, 3])

    def test_find_common_item(self):
        line1 = 'vJrwpWtwJgWrhcsFMMfFFhFp'
        line2 = 'jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL'
        line3 = 'PmmdzqPrVvPwwTWBwg'
        self.assertEqual(find_common_item([line1, line2, line3]), 'r')


if __name__ == '__main__':
    priorities = read_file('input.txt')
    print(sum(priorities))
