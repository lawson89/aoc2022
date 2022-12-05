import string
import unittest
from typing import Tuple

ALL_CHARS = []
ALL_CHARS.extend(string.ascii_lowercase)
ALL_CHARS.extend(string.ascii_uppercase)


# tuple of ints
def range_subset_of(range1: Tuple[int, int], range2: Tuple[int, int]):
    return range2[0] >= range1[0] and range2[1] <= range1[1]


def range_overlaps(range1: Tuple[int, int], range2: Tuple[int, int]):
    return range1[0] <= range2[0] <= range1[1]


def either_overlaps(range1: Tuple[int, int], range2: Tuple[int, int]):
    return range_overlaps(range1, range2) or range_overlaps(range2, range1)


def either_subset(range1, range2):
    return range_subset_of(range1, range2) or range_subset_of(range2, range1)


def parse_line(line):
    line = line.strip()
    r1, r2 = line.split(',')
    r1x, r1y = r1.split('-')
    r2x, r2y = r2.split('-')
    return (int(r1x.strip()), int(r1y.strip())), (int(r2x.strip()), int(r2y.strip()))


def read_file(fpath):
    overlaps = []
    with open(fpath, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if not line:
                continue
            else:
                range1, range2 = parse_line(line)
                print(line)
                if either_overlaps(range1, range2):
                    overlaps.append((range1, range2))
    return overlaps


class TestScore(unittest.TestCase):
    def test_range_subset(self):
        self.assertEqual(either_subset((2, 8), (3, 7)), True)
        self.assertEqual(either_subset((3, 7), (3, 7)), True)
        self.assertEqual(either_subset((22, 81), (57, 82)), False)

    def test_range_overlap(self):
        self.assertEqual(either_overlaps((0, 10), (8, 11)), True)
        self.assertEqual(either_overlaps((8, 11), (0, 10)), True)
        self.assertEqual(either_overlaps((8, 11), (0, 5)), False)

    def test_parse_line(self):
        line = '61-78,61-77'
        range1, range2 = parse_line(line)
        self.assertEqual(range1[0], 61)
        self.assertEqual(range1[1], 78)
        self.assertEqual(range2[0], 61)
        self.assertEqual(range2[1], 77)
        self.assertEqual(either_subset(range2, range1), True)


if __name__ == '__main__':
    overlaps = read_file('input.txt')
    print(overlaps)
    print(len(overlaps))
