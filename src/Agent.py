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