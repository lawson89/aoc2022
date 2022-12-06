import unittest
from collections import deque
from typing import List, Iterable

from common import file_utils

# part a
MARKER_LENGTH = 4
# part b
MESSAGE_LENGTH = 14


def is_marker(buffer: Iterable, marker_length: int):
    if len(buffer) != marker_length:
        return False
    char_set = set()
    for char in buffer:
        if char in char_set:
            return False
        else:
            char_set.add(char)
    return True


def find_first_marker(s: str, marker_length: int):
    deq = deque(maxlen=marker_length)
    for idx, char in enumerate(s):
        deq.append(char)
        if is_marker(deq, marker_length):
            return idx + 1
    return 0


def parse_line(line):
    pass


def process_file(fpath):
    with open(fpath, 'r') as in_file:
        data = in_file.read()
        return find_first_marker(data, MESSAGE_LENGTH)


class TestScore(unittest.TestCase):

    def test_is_marker(self):
        self.assertFalse(is_marker('aaaa', MARKER_LENGTH))
        self.assertTrue(is_marker('abcd', MARKER_LENGTH))
        deq = deque(maxlen=MARKER_LENGTH)
        deq.extend('aaaa')
        self.assertFalse(is_marker(deq, MARKER_LENGTH))
        deq.extend('abcd')
        self.assertTrue(is_marker(deq, MARKER_LENGTH))

    def test_find_first_marker(self):
        self.assertEqual(find_first_marker('bvwbjplbgvbhsrlpgdmjqwftvncz', MARKER_LENGTH), 5)
        self.assertEqual(find_first_marker('nppdvjthqldpwncqszvftbrmjlhg', MARKER_LENGTH), 6)
        self.assertEqual(find_first_marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', MARKER_LENGTH), 10)
        self.assertEqual(find_first_marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', MARKER_LENGTH), 11)
        self.assertEqual(find_first_marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', MESSAGE_LENGTH), 19)


if __name__ == '__main__':
    pos = process_file('input.txt')
    print(pos)
