import math
import random
import sys
import time

CONNECT = 3
COLS = 4
ROWS = 3
EMPTY = ' '
TIE = 'TIE'


class Connect3Board:

    def __init__(self, string=None):
        if string is not None:
            self.b = [list(line) for line in string.split('|')]
        else:
            self.b = [list(EMPTY * ROWS) for i in range(COLS)]

    def compact_string(self):
        return '|'.join([''.join(row) for row in self.b])

    def clone(self):
        return Connect3Board(self.compact_string())

    def get(self, i, j):
        return self.b[i][j] if i >= 0 and i < COLS and j >= 0 and j < ROWS else None

    def row(self, j):
        return [self.get(i, j) for i in range(COLS)]

    def put(self, i, j, val):
        self.b[i][j] = val
        return self

    def empties(self):
        return self.compact_string().count(EMPTY)

    def first_empty(self, i):
        j = ROWS - 1
        if self.get(i, j) != EMPTY:
            return None
        while j >= 0 and self.get(i, j) == EMPTY:
            j -= 1
        return j + 1

    def place(self, i, label):
        j = self.first_empty(i)
        if j is not None:
            self.put(i, j, label)
        return self

    def equals(self, board):
        return self.compact_string() == board.compact_string()

    def next(self, label):
        boards = []
        for i in range(COLS):
            j = self.first_empty(i)
            if j is not None:
                board = self.clone()
                board.put(i, j, label)
                boards.append(board)
        return boards

    def _winner_test(self, label, i, j, di, dj):
        for _ in range(CONNECT - 1):
            i += di
            j += dj
            if self.get(i, j) != label:
                return False
        return True

    def winner(self):
        for i in range(COLS):
            for j in range(ROWS):
                label = self.get(i, j)
                if label != EMPTY:
                    if self._winner_test(label, i, j, +1, 0) \
                            or self._winner_test(label, i, j, 0, +1) \
                            or self._winner_test(label, i, j, +1, +1) \
                            or self._winner_test(label, i, j, -1, +1):
                        return label
        return TIE if self.empties() == 0 else None

    def __str__(self):
        return stringify_boards([self])


def stringify_boards(boards):
    if len(boards) > 6:
        return stringify_boards(boards[0:6]) + '\n' + stringify_boards(boards[6:])
    else:
        s = ' '.join([' ' + ('-' * COLS) + ' '] * len(boards)) + '\n'
        for j in range(ROWS):
            rows = []
            for board in boards:
                rows.append('|' + ''.join(board.row(ROWS - 1 - j)) + '|')
            s += ' '.join(rows) + '\n'
        s += ' '.join([' ' + ('-' * COLS) + ' '] * len(boards))
        return s


class Player:
    def __init__(self, label):
        self.label = label


class Game:
    def __init__(self, board):
        self.board = Connect3Board(board)
        if cmd == "random":
            self.player1 = RandomPlayer("X")
            self.player2 = RandomPlayer("O")
        elif cmd == "minimax":
            self.player1 = RandomPlayer("X")
            self.player2 = MinimaxPlayer("O")
        elif cmd == "alphabeta":
            self.player1 = RandomPlayer("X")
            self.player2 = MinimaxAlphaBetaPlayer("O")

    def game(self):
        board = self.board
        gameList = [board]
        player = self.player1
        winR = []
        while ((board.winner() != "O") and (board.winner() != "X") and (board.winner() != "TIE")):
            # call random/minimax/alphabeta to make the next move
            nextMove = player.nextMove(board)
            board = nextMove
            gameList.append(nextMove)
            if player.label == "X":
                player = self.player2
            else:
                player = self.player1

        return gameList



#This is the Random player for the game
class RandomPlayer(Player):
    def __init__(self, label):
        super().__init__(label)

    def nextMove(self, board=None):
        nextBoard = board.next(self.label)
        lenNextBoard = len(nextBoard)
        randomIndex = random.randint(0, lenNextBoard - 1)
        b = nextBoard[randomIndex]
        return (b)


#This is the Minimax player for the game
class MinimaxPlayer(Player):
    def __init__(self, label):
        super().__init__(label)

#maxValue maximizes the chance of O winning
    def maxValue(self, board):
        maxResult = []
        if board.winner() == "O":
            utility = 1
            return utility
        if board.winner() == "X":
            utility = -1
            return utility
        if board.winner() == "TIE":
            utility = 0
            return utility

        nextBoard = board.next("O")

        for eachBoard in nextBoard:
            maxResult.append((self.minValue(eachBoard) * 0.9))
        return max(maxResult)

#minValue minimizes the chance of X winning
    def minValue(self, board):
        minResult = []

        if board.winner() == "O":
            utility = 1
            return utility
        if board.winner() == "X":
            utility = -1
            return utility
        if board.winner() == "TIE":
            utility = 0
            return utility

        nextBoard = board.next("X")
        for eachBoard in nextBoard:
            minResult.append( self.maxValue(eachBoard))
        return min(minResult)

#Finds the next possible board for given board
    # nextMove is Minimax-Decision for Minimax Player
    def nextMove(self, board=None):
        nextBoard = board.next(self.label)
        maxUtility = -1000
        for eachBoard in nextBoard:
            returnUtility = (self.minValue(eachBoard))
            if returnUtility > maxUtility:
                maxUtility = returnUtility
                maxBoard = eachBoard
        return maxBoard


#This is the alpha beta player for the game
class MinimaxAlphaBetaPlayer(Player):
    def __init__(self, label):
        super().__init__(label)

#maxValue maximizes the chance of O winning
    def maxValue(self, board, a, b):
        maxResult = []
        if board.winner() == "O":
            utility = 1
            return utility
        if board.winner() == "X":
            utility = -1
            return utility
        if board.winner() == "TIE":
            utility = 0
            return utility
        nextBoard = board.next("O")
        for eachBoard in nextBoard:
            maxResult.append(self.minValue(eachBoard,a,b)*0.9)
            v = max(maxResult)
            if v >= a:
                return v
            a = max(a, v)
            return a

#minValue minimizes the chance of X winning
    def minValue(self, board, a, b):
        minResult = []
        if board.winner() == "O":
            utility = 1
            return utility
        if board.winner() == "X":
            utility = -1
            return utility
        if board.winner() == "TIE":
            utility = 0
            return utility

        nextBoard = board.next("X")
        for eachBoard in nextBoard:
            minResult.append(self.maxValue(eachBoard,a,b))
            v = min(minResult)
            if v <= b:
                return v
            b = min(b, v)
            return b


#Finds the next possible board for given board
    # nextMove is Minimax-Decision for Minimax Player
    def nextMove(self, board=None):
        a = -1000
        b = 1000
        nextBoard = board.next(self.label)
        maxUtility = -1000

        for eachBoard in nextBoard:
            returnUtility = (self.minValue(eachBoard, a, b))
            if returnUtility > maxUtility:
                maxUtility = returnUtility
                maxBoard = eachBoard
        return maxBoard


if __name__ == "__main__":
    if len(sys.argv)==3:
        board = Connect3Board(sys.argv[2])
    else:
        board = Connect3Board()
    cmd = sys.argv[1]
    if cmd == 'print':
        print(board)
    if cmd == 'next':
        board= board.next("X")
        boards = stringify_boards(board)
        print(boards)
    if cmd == 'random':
        g = Game(sys.argv[2] if len(sys.argv) > 2 else None)
        rando = g.game()
        print(stringify_boards(rando))
    if cmd == 'minimax':
        g = Game(sys.argv[2] if len(sys.argv) > 2 else None)
        rando = g.game()
        print(stringify_boards(rando))
    if cmd == 'alphabeta':
        g = Game(sys.argv[2] if len(sys.argv) > 2 else None)
        rando = g.game()
        print(stringify_boards(rando))


# cmd="random"
#
# t0 = time.time()
# cmd = "minimax"
# g = Game(sys.argv[2] if len(sys.argv) > 2 else None)
# rando = g.game()
# t1 = time.time()
# total = t1 - t0
# print(stringify_boards(rando))
# print(total)
# t0 = time.time()
#
# cmd = "minimaxAlphaBeta"
# g = Game(sys.argv[2] if len(sys.argv) > 2 else None)
# rando = g.game()
# t1 = time.time()
# total = t1 - t0
# print(stringify_boards(rando))
# print(total)
# # x = 0
# o = 0

# for i in range(300):
#     print(stringify_boards(Game(sys.argv[2] if len(sys.argv) > 2 else None).game()[0]))
#     if(Game(sys.argv[2] if len(sys.argv) > 2 else None).game()[1] == "O"):
#         o += 1
#     elif(Game(sys.argv[2] if len(sys.argv) > 2 else None).game()[1] == "X"):
#         x += 1
# print("x:"+ str(x))
# print("o:"+ str(o))
