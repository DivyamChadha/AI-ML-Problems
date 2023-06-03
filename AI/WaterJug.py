from __future__ import annotations
from queue import LifoQueue
from typing import Callable, NewType

State = NewType("State", tuple[int, int])

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
# (x, y) where x and y are both water jugs and, max(x) = 4 and max(y) = 3

# initial state
start = State((0, 0))

# goal state
goal = State((2, 0))

# operators
waterJugOperator = Callable[[State], State]

fill4gallonJug: waterJugOperator = lambda s: State((4, s[1])) if s[0]<4 else s # fill x
fill3gallonJug: waterJugOperator = lambda s: State((s[0], 3)) if s[1]<3 else s # fill y
empt4gallonJug: waterJugOperator = lambda s: State((0, s[1])) # empty x
empt3gallonJug: waterJugOperator = lambda s: State((s[0], 0)) # empty y
pourFrom3to4Full: waterJugOperator = lambda s: State((4, s[1] - (4 - s[0]))) if ((s[0]+s[1])>=4 and (s[1]>0)) else s # pour from y to x when x+y > 4
pourFrom4to3Full: waterJugOperator = lambda s: State((s[0] - (3-s[1]), 3)) if ((s[0]+s[1])>=3 and (s[0]>0)) else s # pour from x to y when x+y > 3
pourAllFrom4to3: waterJugOperator = lambda s: State((s[0]+s[1], 0)) if ((s[0]+s[1]<=4) and s[1]>0) else s # pour from y to x when x+y < 4
pourAllFrom3to4: waterJugOperator = lambda s: State((0, s[0]+s[1])) if ((s[0]+s[1]<=3) and s[0]>0) else s# pour from x to y when x+y < 3

operators = [
    fill4gallonJug,
    fill3gallonJug,
    empt4gallonJug,
    empt3gallonJug,
    pourFrom3to4Full,
    pourFrom4to3Full,
    pourAllFrom4to3,
    pourAllFrom3to4,
]

def generateAdjacent(n: Node) -> list[Node]:
    nodes = []

    if not n.explored:    
        n.explored = True
        for o in operators:
            t = Node(o(n.state))
            if t:
                nodes.append(t)

    return nodes


current = start
currentNode = Node(current)

stack: LifoQueue[Node] = LifoQueue()
path: list[State] = []

while(current != goal):
    stack.put(currentNode)
    path.append(current)

    for n in generateAdjacent(currentNode):
        stack.put(n)
    
    currentNode = stack.get()
    current = currentNode.state
    
    if stack.empty():
        break

if current == goal:
    print("Goal State Reached")
    print(path)
else:
    print("Goal State not Found")
