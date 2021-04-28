
import copy
from termcolor import colored

VIC = 10 ** 20  # The value of a winning board (for max)
LOSS = -VIC  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # The length of a winning sequence
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board
EMPTY = 0
ROW_COUNT = 6
COLUMN_COUNT = 7

'''
The state of the game is represented by a list of 4 items:
0. The game board - a matrix (list of lists) of ints. Empty cells = 0,
   the comp's cells = COMPUTER and the human's = HUMAN
1. The heuristic value of the state.
2. Who's turn is it: HUMAN or COMPUTER
3. number of empty cells
'''


def create():
    # Returns an empty board. The human plays first.
    board = []
    for i in range(6):
        board = board + [7 * [0]]
    return [board, 0.00001, HUMAN, 42]


def value(s):
    # Returns the heuristic value of s
    return s[1]


def printState(s):
    # Prints the board. The empty cells are printed with 0
    # If the game ended prints who won.
    for r in range(len(s[0])):
        print("\n -- -- -- -- -- -- --\n|", end="")
        for c in range(len(s[0][0])):
            if s[0][r][c] == COMPUTER:
                print(colored("Y", 'yellow'), "|", end="")
            elif s[0][r][c] == HUMAN:
                print(colored("R", 'red'), "|", end="")
            else:
                print(0, "|", end="")
    print("\n -- -- -- -- -- -- --\n")
    if value(s) == VIC:
        print("Ha ha ha I won!")
    elif value(s) == LOSS:
        print("You did it!")
    elif value(s) == TIE:
        print("It's a TIE")


def isFinished(s):
    # returns True if the game ended
    return winning_move(s, HUMAN) or winning_move(s, COMPUTER) or len(getNext(s)) == 0


def isHumTurn(s):
    # Returns True if it the human's turn to play
    return s[2] == HUMAN


def whoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you. : ")) == 1:
        s[2] = COMPUTER
    else:
        s[2] = HUMAN


def makeMove(s, r, c):
    s[0][r][c] = s[2]  # marks the board
    s[3] -= 1  # one less empty cell
    s[2] = COMPUTER + HUMAN - s[2]  # switches turns
    if winning_move(s, HUMAN):
        s[1] = LOSS  # computer loss, human win
        return
    if winning_move(s, COMPUTER):
        s[1] = VIC  # computer win, human loss
        return
    else:
        # my heuristic
        # heuristic value = # of 3 streaks + # of 2 streaks - # of 3 streaks opp (computer) - # of 2 streaks opp
        threes_h = check_threes(s, HUMAN) * 1000
        twos_h = check_twos(s, HUMAN) * 10
        threes_c = check_threes(s, COMPUTER) * 1000
        twos_c = check_twos(s, COMPUTER) * 10
        scores = threes_h + twos_h - threes_c - twos_c
        s[1] += scores
    if s[3] == 0:
        s[1] = TIE


def inputMove(s):
    printState(s)
    flag = True
    while flag:
        col = int(input("Enter your next move (column number, range from 0 to 6): "))
        if col > 6 or s[0][0][col] != 0:
            print("Illegal move.")
        else:
            flag = False
            row = get_next_open_row(s, col)
            makeMove(s, row, col)


def get_next_open_row(s, col):  # return the lowest place to put the piece
    for r in range(ROW_COUNT - 1, -1, -1):
        if s[0][r][col] == 0:
            return r


def is_valid_location(s, col):  # check if the column isn't full
    return s[0][0][col] == 0


def getNext(s):  # returns a list of the next states of s
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(s, col):
            tmp = copy.deepcopy(s)
            r = get_next_open_row(s, col)
            makeMove(tmp, r, col)
            valid_locations += [tmp]
    return valid_locations


def winning_move(s, piece):  # return True if it finds 4 in a row/column/diagonal
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if s[0][r][c] == piece and s[0][r][c + 1] == piece and s[0][r][c + 2] == piece and s[0][r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if s[0][r][c] == piece and s[0][r + 1][c] == piece and s[0][r + 2][c] == piece and s[0][r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if s[0][r][c] == piece and s[0][r + 1][c + 1] == piece and s[0][r + 2][c + 2] == piece and s[0][r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if s[0][r][c] == piece and s[0][r - 1][c + 1] == piece and s[0][r - 2][c + 2] == piece and s[0][r - 3][
                c + 3] == piece:
                return True


def check_threes(board, piece):  # count how many 3 in a row/column/diagonal (for the heuristic)
    num = 0
    # Check horizontal locations with 3 pieces
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT):
            if board[0][r][c] == piece and board[0][r][c + 1] == piece and board[0][r][c + 2] == piece:
                num += 1

    # Check vertical locations with 3 pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if board[0][r][c] == piece and board[0][r + 1][c] == piece and board[0][r + 2][c] == piece:
                num += 1

    # Check positively sloped diagonals with 3 pieces
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT - 2):
            if board[0][r][c] == piece and board[0][r + 1][c + 1] == piece and board[0][r + 2][c + 2] == piece:
                num += 1

    # Check negatively sloped diagonals with 3 pieces
    for c in range(COLUMN_COUNT - 2):
        for r in range(2, ROW_COUNT):
            if board[0][r][c] == piece and board[0][r - 1][c + 1] == piece and board[0][r - 2][c + 2] == piece:
                num += 1

    return num


def check_twos(board, piece):  # count how many 3 in a row/column/diagonal (for the heuristic)
    num = 0
    # Check horizontal locations with 2 pieces
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT):
            if board[0][r][c] == piece and board[0][r][c + 1] == piece:
                num += 1

    # Check vertical locations with 2 pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 1):
            if board[0][r][c] == piece and board[0][r + 1][c] == piece:
                num += 1

    # Check positively sloped diagonals with 2 pieces
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT - 1):
            if board[0][r][c] == piece and board[0][r + 1][c + 1] == piece:
                num += 1

    # Check negatively sloped diagonals with 2 pieces
    for c in range(COLUMN_COUNT - 1):
        for r in range(1, ROW_COUNT):
            if board[0][r][c] == piece and board[0][r - 1][c + 1] == piece:
                num += 1

    return num
