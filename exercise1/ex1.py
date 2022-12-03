from dataclasses import dataclass

from typing import List


@dataclass
class Elf:
    number: int
    packets: List[int]

    @property
    def total_calories(self):
        return sum(self.packets)


def read_file(fpath):
    elfs = []
    elf_number = 0
    elf = Elf(number=elf_number, packets=[])
    with open(fpath, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if not line:
                elfs.append(elf)
                elf_number += 1
                elf = Elf(number=elf_number, packets=[])
            else:
                elf.packets.append(int(line))
    return elfs


if __name__ == '__main__':
    elfs = read_file('input.txt')
    elfs.sort(key=lambda x: x.total_calories, reverse=True)
    print(elfs[0].total_calories)
    top_three = elfs[0:3]
    total_three = sum(x.total_calories for x in top_three)
    print(total_three)

