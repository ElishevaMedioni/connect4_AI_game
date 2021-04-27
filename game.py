import copy

VIC = 10 ** 20  # The value of a winning board (for max) 
LOSS = -VIC  # The value of a losing board (for max)
TIE = 0  # The value of a tie
SIZE = 4  # The length of a winning sequence
COMPUTER = SIZE + 1  # Marks the computer's cells on the board
HUMAN = 1  # Marks the human's cells on the board
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
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
    # Prints the board. The empty cells are printed as numbers = the cells name(for input)
    # If the game ended prins who won.
    for r in range(len(s[0])):
        print("\n -- -- -- -- -- -- --\n|", end="")
        for c in range(len(s[0][0])):
            if s[0][r][c] == AI_PIECE:
                print("X |", end="")
            elif s[0][r][c] == PLAYER_PIECE:
                print("O |", end="")
            else:
                print(0, "|", end="")
    print("\n -- -- -- -- -- -- --\n")
    if value(s) == VIC:
        print("Ha ha ha I won!")
    elif value(s) == LOSS:
        print("You did it!")
    elif value(s) == TIE:
        print("It's a TIE")


# def isFinished(s):
#     # Seturns True iff the game ended
#     return s[1] in [LOSS, VIC, TIE]


def isFinished(s):
    return winning_move(s, PLAYER_PIECE) or winning_move(s, AI_PIECE) or len(getNext(s)) == 0


def isHumTurn(s):
    # Returns True iff it the human's turn to play
    return s[2] == HUMAN


def whoIsFirst(s):
    # The user decides who plays first
    if int(input("Who plays first? 1-me / anything else-you. : ")) == 1:
        s[2] = COMPUTER
    else:
        s[2] = HUMAN


def drop_piece(s, row, col, piece):
    s[0][row][col] = piece


# def checkSeq(s, r1, c1, r2, c2):
#     # r1, c1 are in the board. if r2,c2 not on board returns 0.
#     # Checks the seq. from r1,c1 to r2,c2. If all X returns VIC. If all O returns LOSS.
#     # If no Os returns 1. If no Xs returns -1, Othewise returns 0.
#     if r2 < 0 or c2 < 0 or r2 >= len(s[0]) or c2 >= len(s[0][0]):
#         return 0  # r2, c2 are illegal
#     dr = (r2 - r1) // (SIZE - 1)  # the horizontal step from cell to cell
#     dc = (c2 - c1) // (SIZE - 1)  # the vertical step from cell to cell
#     sum = 0
#     for i in range(SIZE):  # summing the values in the seq.
#         sum += s[0][r1 + i * dr][c1 + i * dc]
#     if sum == COMPUTER * SIZE:
#         return VIC
#     if sum == HUMAN * SIZE:
#         return LOSS
#     if sum > 0 and sum < COMPUTER:
#         return -1
#     if sum > 0 and sum % COMPUTER == 0:
#         return 1
#     return 0


# def makeMove(s, r, c):
#     # Puts mark (for huma. or comp.) in r,c
#     # switches turns
#     # and re-evaluates the heuristic value.
#     # Assumes the move is legal.
#     s[0][r][c] = s[2]  # marks the board
#     s[3] -= 1  # one less empty cell
#     s[2] = COMPUTER + HUMAN - s[2]  # switches turns
#     dr = [-SIZE + 1, -SIZE + 1, 0, SIZE - 1]  # the next lines compute the heuristic val.
#     dc = [0, SIZE - 1, SIZE - 1, SIZE - 1]
#     s[1] = 0.00001
#     for row in range(len(s[0])):
#         for col in range(len(s[0][0])):
#             for i in range(len(dr)):
#                 t = checkSeq(s, row, col, row + dr[i], col + dc[i])
#                 if t in [LOSS, VIC]:
#                     s[1] = t
#                     return
#                 else:
#                     s[1] += t
#     if s[3] == 0:
#         s[1] = TIE


def make_move(s, r, c):
    s[0][r][c] = s[2]  # marks the board
    s[3] -= 1  # one less empty cell
    s[2] = COMPUTER + HUMAN - s[2]  # switches turns
    if winning_move(s, PLAYER_PIECE):
        s[1] = LOSS
        return
    if winning_move(s, AI_PIECE):
        s[1] = VIC
        return
    else:
        # my heuristic
        threesH = check_threes(s, PLAYER_PIECE) * 1000
        twosH = check_twos(s, PLAYER_PIECE) * 10
        threesC = check_threes(s, AI_PIECE) * 1000
        twosC = check_twos(s, AI_PIECE) * 10
        scores = threesH + twosH - threesC - twosC
        s[1] += scores
    if s[3] == 0:
        s[1] = TIE


# def inputMove(s):
#     # Reads, enforces legality and executes the user's move.
#     printState(s)
#     flag = True
#     while flag:
#         move = int(input("Enter your next move: "))
#         r = move // 3
#         c = move % 3
#         if r < 0 or r >= len(s[0]) or c < 0 or c >= len(s[0][0]) or s[0][r][c] != 0:
#             print("Ilegal move.")
#         else:
#             flag = False
#             makeMove(s, r, c)

def inputMove(s):
    printState(s)
    flag = True
    while flag:
        col = int(input("Enter your next move: "))
        if not is_valid_location(s, col) and col > 6:
            print("Illegal move.")
        else:
            flag = False
            row = get_next_open_row(s, col)
            drop_piece(s, row, col, PLAYER_PIECE)
            make_move(s, row, col)


# def getNext(s):
#     # returns a list of the next states of s
#     ns = []
#     for r in range(len(s[0])):
#         for c in range(len(s[0][0])):
#             if s[0][r][c] == 0:
#                 tmp = copy.deepcopy(s)
#                 makeMove(tmp, r, c)
#                 ns += [tmp]
#     return ns


def get_next_open_row(s, col):
    for r in range(ROW_COUNT):
        if s[0][r][col] == 0:
            return r


def is_valid_location(s, col): # check if the column isn't full
    return s[0][ROW_COUNT - 1][col] == 0


def getNext(s): #get_valid_location
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(s, col):
            valid_locations.append(col)
    return valid_locations


def winning_move(s, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if s[0][r][c] == piece and s[0][r][c+1] == piece and s[0][r][c+2] == piece and s[0][r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if s[0][r][c] == piece and s[0][r+1][c] == piece and s[0][r+2][c] == piece and s[0][r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if s[0][r][c] == piece and s[0][r+1][c+1] == piece and s[0][r+2][c+2] == piece and s[0][r+3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if s[0][r][c] == piece and s[0][r-1][c+1] == piece and s[0][r-2][c+2] == piece and s[0][r-3][c+3] == piece:
                return True


def check_threes(board, piece):
    num = 0
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT):
            if board[0][r][c] == piece and board[0][r][c + 1] == piece and board[0][r][c + 2] == piece:
                num += 1

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 2):
            if board[0][r][c] == piece and board[0][r + 1][c] == piece and board[0][r + 2][c] == piece:
                num += 1

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 2):
        for r in range(ROW_COUNT - 2):
            if board[0][r][c] == piece and board[0][r + 1][c + 1] == piece and board[0][r + 2][c + 2] == piece:
                num += 1

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 2):
        for r in range(2, ROW_COUNT):
            if board[0][r][c] == piece and board[0][r - 1][c + 1] == piece and board[0][r - 2][c + 2] == piece:
                num += 1

    return num


def check_twos(board, piece):
    num = 0
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT):
            if board[0][r][c] == piece and board[0][r][c + 1] == piece:
                num += 1

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 1):
            if board[0][r][c] == piece and board[0][r + 1][c] == piece:
                num += 1

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 1):
        for r in range(ROW_COUNT - 1):
            if board[0][r][c] == piece and board[0][r + 1][c + 1] == piece:
                num += 1

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 1):
        for r in range(1, ROW_COUNT):
            if board[0][r][c] == piece and board[0][r - 1][c + 1] == piece:
                num += 1

    return num
