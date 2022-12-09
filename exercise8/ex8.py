import unittest

from common import file_utils

# man alive this is the most inefficient implementation ever!
# that's what I get for trying to do this in between meetings :)

def count_visible(visibility_grid):
    rows, cols = get_grid_dims(visibility_grid)
    count = 0
    for r in range(rows):
        for c in range(cols):
            count += visibility_grid[r][c]
    return count


def build_empty_grid(rows: int, cols: int):
    arr = []
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(0)
        arr.append(col)
    return arr


def populate_grid(lines):
    r = 0
    rows, cols = get_grid_dims(lines)
    grid = build_empty_grid(rows, cols)
    for row in lines:
        c = 0
        for col in row:
            val = int(col)
            grid[r][c] = val
            c += 1
        r += 1
    return grid


def analyze_slice(slice_to_analyze: [], reverse_flag=False):
    if reverse_flag:
        slice_to_analyze = list(reversed(slice_to_analyze))
    visibility_slice = [0] * len(slice_to_analyze)
    max_val = -1
    for idx, val in enumerate(slice_to_analyze):
        if val > max_val:
            visibility_slice[idx] = 1
            max_val = val
        else:
            visibility_slice[idx] = 0
    if reverse_flag:
        visibility_slice.reverse()
    return visibility_slice


def analyze_slice_visibility(slice_to_analyze: [], my_height: int):
    visibility_slice = [0] * len(slice_to_analyze)
    blocked = False
    for idx, val in enumerate(slice_to_analyze):
        if blocked:
            visibility_slice[idx] = 0
            continue
        if val < my_height:
            visibility_slice[idx] = 1
        else:
            visibility_slice[idx] = 1
            blocked = True
    return visibility_slice


def calculate_scenic_score(slice_to_analyze: [], pos):
    my_height = slice_to_analyze[pos]
    scenic_score = 0
    if pos == 0 or pos == len(slice_to_analyze) - 1:
        return scenic_score
    forward_slice = slice_to_analyze[pos + 1:]
    backward_slice = list(reversed(slice_to_analyze[:pos]))
    forward_visibility = analyze_slice_visibility(forward_slice, my_height)
    backward_visibility = analyze_slice_visibility(backward_slice, my_height)
    # print(f'{forward_slice}->{forward_visibility}')
    # print(f'{backward_slice}->{backward_visibility}')
    scenic_score = sum(forward_visibility) * sum(backward_visibility)
    return scenic_score


def get_slice(grid, row_or_col, row_flag=True):
    grid_slice = []
    rows, cols = get_grid_dims(grid)
    if row_flag:
        for c in range(cols):
            grid_slice.append(grid[row_or_col][c])
    else:
        for r in range(rows):
            grid_slice.append(grid[r][row_or_col])
    return grid_slice


def update_grid_visibility(grid, visibility_slice, row_or_col, row_flag=True):
    rows, cols = get_grid_dims(grid)
    if row_flag:
        for c in range(cols):
            visibility = visibility_slice[c]
            current_visibility = grid[row_or_col][c]
            grid[row_or_col][c] = visibility or current_visibility
    else:
        for r in range(rows):
            visibility = visibility_slice[r]
            current_visibility = grid[r][row_or_col]
            grid[r][row_or_col] = visibility or current_visibility


def analyze_grid(grid):
    rows, cols = get_grid_dims(grid)
    # 1 is visible, 0 is not visible
    visibility_grid = build_empty_grid(rows, cols)
    for r in range(rows):
        # look down row and then look back up row
        grid_slice = get_slice(grid=grid, row_or_col=r, row_flag=True)
        visibility = analyze_slice(grid_slice)
        update_grid_visibility(grid=visibility_grid, visibility_slice=visibility, row_or_col=r, row_flag=True)
        visibility_reversed = analyze_slice(grid_slice, reverse_flag=True)
        update_grid_visibility(grid=visibility_grid, visibility_slice=visibility_reversed, row_or_col=r, row_flag=True)
    for c in range(cols):
        grid_slice = get_slice(grid=grid, row_or_col=c, row_flag=False)
        visibility = analyze_slice(grid_slice)
        update_grid_visibility(grid=visibility_grid, visibility_slice=visibility, row_or_col=c, row_flag=False)
        visibility_reversed = analyze_slice(grid_slice, reverse_flag=True)
        update_grid_visibility(grid=visibility_grid, visibility_slice=visibility_reversed, row_or_col=c, row_flag=False)
    return visibility_grid


def calculate_scenic_score_grid(grid, row=0, col=0):
    horizontal_slice = get_slice(grid, row_or_col=row, row_flag=True)
    vertical_slice = get_slice(grid, row_or_col=col, row_flag=False)
    scenic_score_horizontal = calculate_scenic_score(horizontal_slice, pos=col)
    scenic_score_vertical = calculate_scenic_score(vertical_slice, pos=row)
    return scenic_score_vertical * scenic_score_horizontal


def calculate_max_scenic_score(grid):
    max_score = 0
    rows, cols = get_grid_dims(grid)
    for r in range(rows):
        for c in range(cols):
            score = calculate_scenic_score_grid(grid, r, c)
            max_score = max(score, max_score)
            print(f'{r}, {c} = {score}')
    return max_score


def dump_grid(grid):
    for row in grid:
        row_str: str = ''
        for val in row:
            row_str += str(val)
        print(row_str)


def get_grid_dims(grid) -> (int, int):
    rows = len(grid)
    cols = len(grid[0])
    return rows, cols


def process_file(fpath):
    lines = []
    with open(fpath, 'r') as in_file:
        for line in file_utils.read_file_stripped(in_file):
            lines.append(line)
        grid = populate_grid(lines)
        dump_grid(grid)
        rows, cols = get_grid_dims(grid)
        print(f'grid size: ({rows}, {cols}) ')
        visibility_grid = analyze_grid(grid)
        print('visibility')
        dump_grid(visibility_grid)
        visible_count = count_visible(visibility_grid)
        print(f'visible = {visible_count}')
        max_scenic = calculate_max_scenic_score(grid)
        print(f'max_scenic = {max_scenic}')


class TestListing(unittest.TestCase):

    def test_empty_grid(self):
        grid = build_empty_grid(5, 5)
        dump_grid(grid)

    def build_test_grid(self):
        data: str = '''
30373
25512
65332
33549
35390        
                '''
        lines = []
        for row in data.splitlines():
            row = row.strip()
            if row:
                lines.append(row)
        grid = populate_grid(lines)
        return grid

    def test_build_grid(self):
        grid = self.build_test_grid()
        dump_grid(grid)

    def test_grid_dims(self):
        grid = self.build_test_grid()
        rows, cols = get_grid_dims(grid)
        self.assertEqual(rows, 5)
        self.assertEqual(cols, 5)

    def test_get_slice(self):
        grid = self.build_test_grid()
        dump_grid(grid)
        grid_slice = get_slice(grid, 2, True)
        print(grid_slice)
        self.assertEqual(grid_slice, [6, 5, 3, 3, 2])
        grid_slice = get_slice(grid, 2, False)
        print(grid_slice)
        self.assertEqual(grid_slice, [3, 5, 3, 5, 3])

    def test_analyze(self):
        grid = self.build_test_grid()
        print('grid')
        dump_grid(grid)
        visibility_grid = analyze_grid(grid)
        print('visibility')
        dump_grid(visibility_grid)
        visible_count = count_visible(visibility_grid)
        self.assertEqual(visible_count, 21)

    def test_scenic_score(self):
        slice_to_analyze = [3, 3, 5, 4, 9]
        scenic_score_horizontal = calculate_scenic_score(slice_to_analyze, pos=2)
        self.assertEqual(scenic_score_horizontal, 4)
        slice_to_analyze = [3, 5, 3, 5, 3]
        scenic_score_vertical = calculate_scenic_score(slice_to_analyze, pos=3)
        self.assertEqual(scenic_score_vertical, 2)
        self.assertEqual(calculate_scenic_score(slice_to_analyze, pos=0), 0)
        self.assertEqual(calculate_scenic_score(slice_to_analyze, pos=4), 0)

    def test_calculate_scenic_score_grid(self):
        grid = self.build_test_grid()
        score = calculate_scenic_score_grid(grid, 1, 2)
        self.assertEqual(score, 4)
        score = calculate_scenic_score_grid(grid, 3, 2)
        self.assertEqual(score, 8)

    def test_calculate_max_scenic_score_grid(self):
        grid = self.build_test_grid()
        max_score = calculate_max_scenic_score(grid)
        print(max_score)


if __name__ == '__main__':
    process_file('input.txt')
