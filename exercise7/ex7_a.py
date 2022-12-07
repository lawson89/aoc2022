import unittest
from dataclasses import dataclass, field
from typing import List, Iterable, Dict

import common.file_utils


@dataclass
class DirEntry:
    children: List = field(default_factory=list)
    name: str = '/'
    is_dir: bool = True
    my_size: int = 0
    parent: 'DirEntry' = None

    @property
    def size(self) -> int:
        if not self.is_dir:
            return self.my_size
        else:
            total_size = 0
            for child in self.children:
                child: DirEntry
                total_size += child.size
        return total_size

    @property
    def my_path(self) -> str:
        if self.parent:
            if self.parent.name == '/':
                return f'/{self.name}'
            else:
                return f'{self.parent.my_path}/{self.name}'
        else:
            return self.name

    def print_tree(self, level=0):
        indent = ' ' * level
        print(f'{indent} {self.name} {self.is_dir} {len(self.children)} {self.size}')
        level += 1
        for child in self.children:
            child.print_tree(level)


CURRENT_DIR: DirEntry = DirEntry(name='/', is_dir=True, my_size=0)
DIR_ENTRY_MAP: Dict[str, DirEntry] = {'/': CURRENT_DIR}


@dataclass
class Command:
    command_name: str
    command_arg: str = ''
    buffer: [] = field(default_factory=lambda: [])


def handle_cd(command: Command):
    dir_name = command.command_arg
    global CURRENT_DIR
    if dir_name == '..':
        CURRENT_DIR = CURRENT_DIR.parent
    else:
        if dir_name == '/':
            dir_entry = DirEntry(name=dir_name, is_dir=True, my_size=0)
        else:
            dir_entry = DirEntry(name=dir_name, is_dir=True, parent=CURRENT_DIR, my_size=0)
        # is this the first time we have seen this directory?
        # if so add to the map, otherwise get the existing dir out of the map
        if dir_entry.my_path not in DIR_ENTRY_MAP:
            DIR_ENTRY_MAP[dir_entry.my_path] = dir_entry
        else:
            dir_entry = DIR_ENTRY_MAP[dir_entry.my_path]
        CURRENT_DIR = dir_entry


def handle_ls(command: Command):
    parent_entry: DirEntry = CURRENT_DIR
    child_entry: DirEntry
    listing: [] = command.buffer
    for line in listing:
        if 'dir' in line:
            name = line.split()[1].strip()
            child_entry = DirEntry(name=name, is_dir=True, parent=parent_entry, my_size=0)
        else:
            size, name = line.split()
            name = name.strip()
            size = int(size.strip())
            child_entry = DirEntry(name=name, is_dir=False, parent=parent_entry, my_size=size)
        my_path = child_entry.my_path
        if my_path not in DIR_ENTRY_MAP:
            parent_entry.children.append(child_entry)
            DIR_ENTRY_MAP[my_path] = child_entry


def build_commands(data: Iterable):
    commands = []
    current_command: Command = None
    idx = 0
    for line in data:
        idx += 1
        line: str
        line = line.strip()
        if not line:
            continue
        if '$' in line:
            # ok we have a new command so add the current command to the list
            if current_command:
                commands.append(current_command)
                current_command = None
            line = line.replace('$', '')
            if 'cd' in line:
                arg = line.split()[1]
                current_command = Command(command_name='cd', command_arg=arg)
            else:
                current_command = Command(command_name='ls')
        else:
            current_command.buffer.append(line)
    if current_command:
        commands.append(current_command)

    return commands


def play_commands(commands: List[Command]):
    for command in commands:
        if command.command_name == 'cd':
            handle_cd(command)
        else:
            handle_ls(command)


def process_file(fpath):
    with open(fpath, 'r') as in_file:
        data = common.file_utils.read_file_stripped(in_file)
        commands = build_commands(data)
        play_commands(commands)


class TestListing(unittest.TestCase):

    def test_listing(self):
        listing = '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k        '''
        commands = build_commands(listing.splitlines())
        play_commands(commands)
        root = DIR_ENTRY_MAP['/']
        root.print_tree()


if __name__ == '__main__':
    process_file('input.txt')
    root = DIR_ENTRY_MAP['/']
    root.print_tree()
    total = 0
    for path, entry in DIR_ENTRY_MAP.items():
        entry: DirEntry
        if entry.is_dir and entry.size <= 100000:
            total += entry.size
    print(total)
    space_used = root.size
    space_available = 70000000
    free_space = space_available - space_used
    print(f'{space_available} {space_used} {free_space}')
    additional_space = 30000000 - free_space
    print(f'{additional_space}')
    dirs_greater_than_needed = []
    for path, entry in DIR_ENTRY_MAP.items():
        entry: DirEntry
        if entry.is_dir and entry.size >= additional_space:
            dirs_greater_than_needed.append(entry)
    # print(dirs_greater_than_needed)
    dirs_greater_than_needed.sort(key=lambda x: x.size)
    print(dirs_greater_than_needed[0].size)
