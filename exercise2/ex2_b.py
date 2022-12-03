import unittest

ROCK_ENCRYPTED = ('A',)
PAPER_ENCRYPTED = ('B',)
SCISSORS_ENCRYPTED = ('C',)

ROCK = 'R'
PAPER = 'P'
SCISSORS = 'S'

CHOICE_MAP = {ROCK: ROCK_ENCRYPTED, PAPER: PAPER_ENCRYPTED, SCISSORS: SCISSORS_ENCRYPTED}

SCORE_MAP = {
    'X': 0,
    'Y': 3,
    'Z': 6
}

# format is (opponent, me)
# result is score
GAME_SCORE = {
    (ROCK, ROCK): 3,
    (ROCK, PAPER): 6,
    (ROCK, SCISSORS): 0,
    (PAPER, ROCK): 0,
    (PAPER, PAPER): 3,
    (PAPER, SCISSORS): 6,
    (SCISSORS, ROCK): 6,
    (SCISSORS, PAPER): 0,
    (SCISSORS, SCISSORS): 3,
}

BASE_SCORE = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
}


def unencrypt(encrypted):
    retval = None
    for k, v in CHOICE_MAP.items():
        if encrypted in v:
            retval = k
    if not retval:
        raise ValueError('Not able to decrypt')
    return retval


def calculate_score(opp, me):
    opp = unencrypt(opp)
    score = BASE_SCORE[me] + GAME_SCORE[(opp, me)]
    return score


def get_my_move(opp, winlosetie):
    opp = unencrypt(opp)
    my_score = SCORE_MAP[winlosetie]
    retval = None
    for k, v in GAME_SCORE.items():
        if opp == k[0] and v == my_score:
            retval = k[1]
    if not retval:
        raise ValueError('Not able to calculate move')
    return retval


def read_file(fpath):
    scores = []
    with open(fpath, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if not line:
                continue
            else:
                opp, winlosetie = line.split(' ')
                me = get_my_move(opp, winlosetie)
                score = calculate_score(opp, me)
                scores.append(score)
    return scores


class TestScore(unittest.TestCase):
    def test_score_calc1(self):
        opp = 'A'
        me = 'P'
        score = calculate_score(opp, me)
        expected = 8
        self.assertEqual(score, expected)

    def test_score_calc2(self):
        opp = 'B'
        me = 'R'
        score = calculate_score(opp, me)
        expected = 1
        self.assertEqual(score, expected)

    def test_score_calc3(self):
        opp = 'C'
        me = 'S'
        score = calculate_score(opp, me)
        expected = 6
        self.assertEqual(score, expected)

    def test_my_move1(self):
        opp = 'A'
        winlosetie = 'Y'
        me = get_my_move(opp, winlosetie)
        score = calculate_score(opp, me)
        expected = 4
        self.assertEqual(score, expected)

    def test_my_move2(self):
        opp = 'B'
        winlosetie = 'X'
        me = get_my_move(opp, winlosetie)
        score = calculate_score(opp, me)
        expected = 1
        self.assertEqual(score, expected)

    def test_my_move3(self):
        opp = 'C'
        winlosetie = 'Z'
        me = get_my_move(opp, winlosetie)
        score = calculate_score(opp, me)
        expected = 7
        self.assertEqual(score, expected)


if __name__ == '__main__':
    scores = read_file('input.txt')
    print(sum(scores))
