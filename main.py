import random


class Env:
    def __init__(self, d, n):
        self.d = d
        self.n = n
        data = [0] * (d * d - n) + ["X"] * n
        random.shuffle(data)  # Randomly shuffle mines on the board
        self._board = [[data.pop() for _ in range(d)] for _ in range(d)]
        self.setHints()

    def checkVal(self, row, col):
        """returns the hit value"""
        return self._board[row][col]

    def setHints(self):
        """Sets the environment game board"""
        for x in range(self.d):
            for y in range(self.d):
                if self._board[x][y] == "X":
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            try:
                                if x + dx >= 0 and y + dy >= 0 and self._board[x + dx][y + dy] != "X":
                                    self._board[x + dx][y + dy] += 1
                            except IndexError:
                                continue

    def my_8_clear(self, agentBoard, row, col):
        """ If an empty cell is hit keep on clearing adjacent cells till not empty cells are hit"""
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx or dy:
                    x, y = row + dx, col + dy
                    if 0 <= x < self.d and 0 <= y < self.d and self._board[x][y] != "X" and agentBoard[x][y] == "-":
                        agentBoard[x][y] = self._board[x][y]
                        if agentBoard[x][y] == 0:
                            agentBoard = self.my_8_clear(agentBoard, x, y)
        return agentBoard

    def makeMove(self, agentBoard, row, col):
        """ Sets the necessary cells to values if mine not hit else ends game"""
        ans = self.checkVal(row, col)

        # processing result
        if ans == "X":
            print('\n', "--" * 15, "\tOops, stepped on a mine! GAME OVER")
            print(self)
            raise StopIteration
        else:
            print('\n', "Env says", ans)
            agentBoard[row][col] = ans
            if ans == 0:
                # set neighbors as clear
                agentBoard = self.my_8_clear(agentBoard, row, col)
        return agentBoard

    def __repr__(self):
        res = ''
        for i in range(self.d):
            for j in range(self.d):
                res += '{:<3}'.format(self._board[i][j])
            res += '\n'
        return res


class Agent:
    def __init__(self, d, n):
        self.d = d
        self.n = n
        self.board = [["-" for _ in range(d)] for _ in range(d)]  # - is UNKNOWN
        self.score = d ** 2

    def __repr__(self):
        print(' BOARD  \n')
        res = ''
        for i in range(self.d):
            for j in range(self.d):
                res += '{:<3}'.format(self.board[i][j])
            res += '\n'
        return res

    def anyUnknown(self):
        """Checks if the game is finished"""
        return any("-" in row for row in self.board) and sum(row.count("-") for row in self.board) > self.n

    def alreadyVisited(self, row, col):
        """Checks if the cell is already visited by the user"""
        if self.board[row][col] != "-":
            print("Already visited. Pick a new cell")
            return True
        return False

    def makeMove(self, env, row, col):
        """User makes move to discover safe cells"""
        if not(0 <= row < self.d) or not(0 <= col < self.d) or self.alreadyVisited(row, col):
            raise IOError
        self.board = env.makeMove(self.board, row, col)
        self.score -= 1
        print(self)
        if not self.anyUnknown():  # check if all is done.
            print("\n Congrats on finishing the game. \t", "Score=", self.score)
            raise StopIteration


def game():
    print("Welcome to Minesweeper")
    d = int(input("Enter dimension:"))
    n = int(input("Enter number of mines"))

    env = Env(d, n)
    ag = Agent(d, n)
    print(ag)

    for _ in range(1 + d ** 2):
        row, col = [int(x) for x in input("Enter row and col values separated by comma: ").split(",")]
        try:
            print(ag.makeMove(env, row, col))
        except StopIteration:
            break
        except IOError:
            continue


game()
