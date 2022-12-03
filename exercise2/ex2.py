import unittest

ROCK_ENCRYPTED = ('A', 'X')
PAPER_ENCRYPTED = ('B', 'Y')
SCISSORS_ENCRYPTED = ('C', 'Z')

ROCK = 'R'
PAPER = 'P'
SCISSORS = 'S'

CHOICE_MAP = {ROCK: ROCK_ENCRYPTED, PAPER: PAPER_ENCRYPTED, SCISSORS: SCISSORS_ENCRYPTED}

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
    me = unencrypt(me)
    score = BASE_SCORE[me] + GAME_SCORE[(opp, me)]
    return score


def read_file(fpath):
    scores = []
    with open(fpath, 'r') as in_file:
        for line in in_file:
            line = line.strip()
            if not line:
                continue
            else:
                opp, me = line.split(' ')
                score = calculate_score(opp, me)
                scores.append(score)
    return scores


class TestScore(unittest.TestCase):
    def test_score_calc1(self):
        opp = 'A'
        me = 'Y'
        score = calculate_score(opp, me)
        expected = 8
        self.assertEqual(score, expected)

    def test_score_calc2(self):
        opp = 'B'
        me = 'X'
        score = calculate_score(opp, me)
        expected = 1
        self.assertEqual(score, expected)

    def test_score_calc3(self):
        opp = 'C'
        me = 'Z'
        score = calculate_score(opp, me)
        expected = 6
        self.assertEqual(score, expected)


if __name__ == '__main__':
    scores = read_file('input.txt')
    print(sum(scores))

