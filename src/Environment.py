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
            print('\n', "--" * 15, "\nOops, stepped on a mine! GAME OVER")
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