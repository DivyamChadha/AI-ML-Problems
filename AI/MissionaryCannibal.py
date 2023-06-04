from __future__ import annotations
from queue import LifoQueue
from typing import Callable, NewType

State = NewType("State", tuple[int, int, bool])

class Node:
    __nodes__: set[State] = set()
    def __new__(cls, state: State) -> Node | None:
        if state in cls.__nodes__:
            return
        cls.__nodes__.add(state)
        return super().__new__(cls)
    
    def __init__(self, state: State) -> None:
        self.state = state
        self.explored: bool = False

    def __repr__(self) -> str:
        return f"Node<{self.state}>"

# representation
# (m, c, b) where m and x are number of missionaries and cannibals on the left bank and b is a boolean flag representing the bank where the boat is present
# b = False left bank, b = True right bank

# initial state
start = State((3, 3, False))

# goal state
goal = State((0, 0, True))


boatOnLeftBank = lambda s: s[2] == False
boatOnRightBank = lambda s: s[2]
mcOperator = Callable[[State], State]

# operators
lToR1M: mcOperator = lambda s: State((s[0]-1, s[1], True)) if (boatOnLeftBank(s) and s[0]>0) else s # 1 missionary left to right
lToR2M: mcOperator = lambda s: State((s[0]-2, s[1], True)) if (boatOnLeftBank(s) and s[0]>1) else s # 2 missionary left to right
lToR1C: mcOperator = lambda s: State((s[0], s[1]-1, True)) if (boatOnLeftBank(s) and s[1]>0) else s # 1 cannibal left to right
lToR2C: mcOperator = lambda s: State((s[0], s[1]-2, True)) if (boatOnLeftBank(s) and s[1]>1) else s # 2 cannibal left to right
lToR1M1C: mcOperator = lambda s: State((s[0]-1, s[1]-1, True)) if (boatOnLeftBank(s) and s[0]>0 and s[1]>0) else s # 1 missionary and 1 cannibal left to right

rToL1M: mcOperator = lambda s: State((s[0]+1, s[1], False)) if (boatOnRightBank(s) and s[0]<3) else s # 1 missionary right to left
rToL2M: mcOperator = lambda s: State((s[0]+2, s[1], False)) if (boatOnRightBank(s) and s[0]<2) else s # 2 missionary right to left
rToL1C: mcOperator = lambda s: State((s[0], s[1]+1, False)) if (boatOnRightBank(s) and s[1]<3) else s # 1 cannibal right to left
rToL2C: mcOperator = lambda s: State((s[0], s[1]+2, False)) if (boatOnRightBank(s) and s[1]<2) else s # 2 cannibal right to left
rToL1M1C: mcOperator = lambda s: State((s[0]+1, s[1]+1, False)) if (boatOnRightBank(s) and s[0]<3 and s[1]<3) else s # 1 missionary and 1 cannibal right to left

operators = [
    lToR1M,
    lToR2M,
    lToR1C,
    lToR2C,
    lToR1M1C,
    rToL1M,
    rToL2M,
    rToL1C,
    rToL2C,
    rToL1M1C,
]

def generateAdjacent(n: Node) -> list[Node]:
    nodes = []

    if not n.explored:    
        n.explored = True
        for o in operators:
            t = Node(o(n.state))
            if t and t.state != n.state:

                # control statement
                if (t.state[0] >= t.state[1] or t.state[0] == 0) and (3 - t.state[0] >= 3 - t.state[1] or 3 - t.state[0] == 0):
                    nodes.append(t)

    return nodes


currentNode = Node(start)

stack: LifoQueue[Node] = LifoQueue()
path: list[State] = []

i = 0
while(currentNode.state != goal):
    stack.put(currentNode)
    path.append(currentNode.state)

    for n in generateAdjacent(currentNode):
        stack.put(n)

    if stack.empty():
        break
    
    currentNode = stack.get()
    stack.task_done()

if currentNode.state == goal:
    path.append(currentNode.state)
    print("Goal State Reached")
    print(path)
else:
    print("Goal State not Found")
