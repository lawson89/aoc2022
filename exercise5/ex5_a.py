import unittest
from dataclasses import dataclass
from typing import List
from common import file_utils


@dataclass
class Move:
    move_from: int
    move_to: int
    num_moves: int


def handle_move(m: Move, towers: List):
    tower_from = towers[m.move_from - 1]
    tower_to = towers[m.move_to - 1]
    for _ in range(m.num_moves):
        crate = tower_from.pop()
        tower_to.append(crate)


def to_int(s: str) -> int:
    s.strip()
    return int(s)


def init_towers(setup):
    tower_list = []
    for line in setup:
        # add a character to end to make each chunk 4 chars wide
        line = line + ' '
        chunks = [line[j:j + 4] for j in range(0, len(line), 4)]
        tower_num = 0
        for chunk in chunks:
            crate = chunk.strip('[] ')
            if len(tower_list) <= tower_num:
                tower_list.append([])
            tower: List = tower_list[tower_num]
            if crate:
                tower.insert(0, crate)
            tower_num += 1
    return tower_list


def parse_line(line):
    line = line.replace('move', '')
    line = line.replace('from', '')
    line = line.replace('to', '')
    line = line.replace('  ', ' ')
    num_moves_s, move_from_s, move_to_s = line.split()
    move_from: int = to_int(move_from_s)
    move_to: int = to_int(move_to_s)
    num_moves: int = to_int(num_moves_s)
    move: Move = Move(move_from, move_to, num_moves)
    return move


def process_file(fpath):
    tower_list: List
    setup_lines = []
    in_setup = True
    with open(fpath, 'r') as in_file:
        for line in file_utils.read_file_stripped(in_file):
            line: str
            if in_setup:
                if '1' in line:
                    in_setup = False
                    tower_list = init_towers(setup_lines)
                    continue
                setup_lines.append(line)
            else:
                m = parse_line(line)
                handle_move(m, tower_list)
    return tower_list


class TestScore(unittest.TestCase):

    def test_parse_line(self):
        line = 'move 1 from 2 to 3'
        m = parse_line(line)
        self.assertEqual(m.num_moves, 1)
        self.assertEqual(m.move_from, 2)
        self.assertEqual(m.move_to, 3)

    @staticmethod
    def setup_test_towers():
        setup = '''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3       
                '''
        setup_lines = [line for line in setup.splitlines() if line.strip() and '1' not in line]
        towers = init_towers(setup_lines)
        return towers

    def test_init_towers(self):
        towers = self.setup_test_towers()
        self.assertEqual(len(towers), 3)
        self.assertEqual(towers[0], ['Z', 'N'])
        self.assertEqual(towers[0], ['M', 'C', 'D'])
        self.assertEqual(towers[0], ['P'])

    def test_moves(self):
        move_lines = '''
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
        '''
        moves = []
        for line in move_lines.splitlines():
            line = line.strip()
            if not line:
                continue
            moves.append(parse_line(line))
        towers = self.setup_test_towers()
        for move in moves:
            handle_move(move, towers)
        print(towers)


if __name__ == '__main__':
    final_towers = process_file('input.txt')
    print(final_towers)
