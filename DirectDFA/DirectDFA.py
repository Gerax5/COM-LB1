from Models.Node import Node
from graphviz import Digraph

class DirectDFA:
    OPERATORS = ["*"]
    BINARY_OPERATORS = ["^", "|", "."]

    def __init__(self, stack: list[Node], alphabet: list[str], fileNumber = 0):
        self.fileNumber = fileNumber
        self.alphabet = alphabet
        self.currentLeafNumber = 0
        self.leaves = {}
        seed = stack[0]
        self.enumerateLeaves(seed)
        self.setNullable(seed)
        self.setFirstPosition(seed)
        self.setLastPosition(seed)
        self.setFollowPosition(seed)

        self.transitions = {}
        self.stateNumber = 0
        self.generateTransitionTable(seed)
        self.setAcceptStates()
        self.createGraph()

        print(self.transitions)

    def enumerateLeaves(self, node: Node):
        if node.getIsOperator():
            object = "".join(node.getObject())
            if object in self.BINARY_OPERATORS: 
                self.enumerateLeaves(node.getChilds()[0])
                self.enumerateLeaves(node.getChilds()[1])
            else:
                self.enumerateLeaves(node.getChilds()[0])
        else:
            leaf = "".join(node.getObject())
            if leaf != "ε":
                node.leafNumber = self.currentLeafNumber
                self.currentLeafNumber += 1
                if leaf == "#":
                    self.leaves[leaf] = node.leafNumber
                else:
                    self.leaves[node.leafNumber] = {
                        "letter": leaf,
                        "followPosition": set()
                    }

            # print(node.getObject(), node.leafNumber)

    def setNullable(self, node: Node):
        if node.getIsOperator():
            object = "".join(node.getObject())
            if object in self.BINARY_OPERATORS:
                self.setNullable(node.getChilds()[0])
                self.setNullable(node.getChilds()[1])
                if object == "|":
                    node.nullable = node.getChilds()[0].nullable or node.getChilds()[1].nullable
                elif object == ".":
                    node.nullable = node.getChilds()[0].nullable and node.getChilds()[1].nullable
            elif object in self.OPERATORS:
                self.setNullable(node.getChilds()[0])
                node.nullable = True
        else:
            if "".join(node.getObject()) == "ε":
                node.nullable = True
            else:
                node.nullable = False

        # print("Nullable", node.getObject(), node.nullable, node.leafNumber)

    def setFirstPosition(self, node: Node):
        if node.getIsOperator():
            object = "".join(node.getObject())
            if object in self.BINARY_OPERATORS:
                self.setFirstPosition(node.getChilds()[0])
                self.setFirstPosition(node.getChilds()[1])
                if object == "|":
                    node.firstPosition = node.getChilds()[0].firstPosition.union(node.getChilds()[1].firstPosition)
                elif object == ".":
                    if node.getChilds()[0].nullable:
                        node.firstPosition = node.getChilds()[0].firstPosition.union(node.getChilds()[1].firstPosition)
                    else:
                        node.firstPosition = node.getChilds()[0].firstPosition
            elif object in self.OPERATORS:
                self.setFirstPosition(node.getChilds()[0])
                node.firstPosition = node.getChilds()[0].firstPosition
        else:
            if "".join(node.getObject()) == "ε":
                node.firstPosition = set()
            else:
                node.firstPosition = {node.leafNumber}

        # print("first", node.getObject(), node.firstPosition ,node.nullable, node.leafNumber)

    def setLastPosition(self, node: Node):
        if node.getIsOperator():
            object = "".join(node.getObject())
            if object in self.BINARY_OPERATORS:
                self.setLastPosition(node.getChilds()[0])
                self.setLastPosition(node.getChilds()[1])
                if object == "|":
                    node.lastPosition = node.getChilds()[0].lastPosition.union(node.getChilds()[1].lastPosition)
                elif object == ".":
                    if node.getChilds()[1].nullable:
                        node.lastPosition = node.getChilds()[0].lastPosition.union(node.getChilds()[1].lastPosition)
                    else:
                        node.lastPosition = node.getChilds()[1].lastPosition
            elif object in self.OPERATORS:
                self.setLastPosition(node.getChilds()[0])
                node.lastPosition = node.getChilds()[0].lastPosition
        else:
            if "".join(node.getObject()) == "ε":
                node.lastPosition = set()
            else:
                node.lastPosition = {node.leafNumber}


        # print("last", node.getObject(), node.firstPosition, node.lastPosition,node.nullable, node.leafNumber)

    def setFollowPosition(self, node: Node):
        if node.getIsOperator():
            object = "".join(node.getObject())
            if object in self.BINARY_OPERATORS:
                self.setFollowPosition(node.getChilds()[0])
                self.setFollowPosition(node.getChilds()[1])
                if object == ".":
                    for i in node.getChilds()[0].lastPosition:
                        self.leaves[i]["followPosition"] =  self.leaves[i]["followPosition"].union(node.getChilds()[1].firstPosition)
            elif object in self.OPERATORS:
                self.setFollowPosition(node.getChilds()[0])
                for i in node.getChilds()[0].lastPosition:
                    self.leaves[i]["followPosition"] = self.leaves[i]["followPosition"].union(node.firstPosition)

    def getStateName(self):
        state = f"S{self.stateNumber}"
        self.stateNumber += 1
        return state

    def generateTransitionTable(self, seed: Node):
        firstState = tuple(seed.firstPosition)
        self.transitions[firstState] = {
            "name": self.getStateName(),
            "state": firstState,
            "initial": True,
            "accept": False,
            "transitions": {}
        }

        stack = [firstState]

        while len(stack) > 0:
            currentState = stack.pop()
            transitions = self.transitions[currentState]["transitions"]
            for letter in self.alphabet:
                nextState = set()
                for i in currentState:
                    if i in self.leaves:
                        if letter in self.leaves[i]["letter"]:
                            nextState = nextState.union(self.leaves[i]["followPosition"])
                nextState = tuple(nextState)
                if nextState not in self.transitions:
                    self.transitions[nextState] = {
                        "name": self.getStateName(),
                        "state": nextState,
                        "accept": False,
                        "transitions": {}
                    }
                    stack.append(nextState)
                transitions[letter] = self.transitions[nextState]["state"]

        print(self.transitions)

    def setAcceptStates(self):
        for i in self.transitions:
            state = self.transitions[i]
            for j in state["state"]:
                if j == self.leaves["#"]:
                    state["accept"] = True
                    break

    def getInitialState(self):
        for i in self.transitions:
            if self.transitions[i]["initial"]:
                return self.transitions[i]["state"]
            
    def createGraph(self):
        self.diagram = Digraph()
        self.diagram.node("start", "inicio", shape='point', width='0')

        for state in self.transitions:
            if state != ():
                if self.transitions[state]["accept"]:
                    self.diagram.node(self.transitions[state]["name"], self.transitions[state]["name"], shape='doublecircle')
                else:
                    self.diagram.node(self.transitions[state]["name"], self.transitions[state]["name"], shape='circle')

        for state in self.transitions:
            if state != ():
                for letter in self.alphabet:
                    nextState = self.transitions[state]["transitions"][letter]
                    if nextState != ():
                        self.diagram.edge(self.transitions[state]["name"], self.transitions[nextState]["name"], label=letter)

        self.diagram.edge("start",self.transitions[self.getInitialState()]["name"])

        self.diagram.render(f'AutomataDirectDFA/DirectDFA{self.fileNumber}', format='png', cleanup=False)

    def recognize(self, string: str):
        currentState = self.getInitialState()
        for letter in string:
            currentState = self.transitions[currentState]["transitions"][letter]
        return self.transitions[currentState]["accept"]
            
    

        
        
