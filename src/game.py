from Environment import Env
from Agent import Agent


print("Welcome to Minesweeper")
d = int(input("Enter dimension: "))
n = int(input("Enter number of mines: "))

env = Env(d, n)
ag = Agent(d, n)
print(ag)

for _ in range(1 + d ** 2):
    row, col = [int(x) for x in input("Enter row and col values separated by comma: ").split(",")]
    try:
        ag.makeMove(env, row, col)
    except StopIteration:
        break
    except IOError:
        continue
