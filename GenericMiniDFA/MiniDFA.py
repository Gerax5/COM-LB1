
from graphviz import Digraph

class GenericMiniDFA():
    def __init__(self, dfaStates: set, acceptStates: list, noAcceptStates: list, alphabet: list, fileNumber = 0):
        self.dfaStates = dfaStates
        self.acceptStates = acceptStates
        self.noAcceptStates = noAcceptStates
        self.alphabet = alphabet
        self.fileNumber = fileNumber
        self.nStates = 0
        self.minimization()
        self.generateTree()

    def recognize(self, string: str):
        print(f"\033[32mExpresion a evaluar en Min DFA con construccion directa : {string}\033[0m")
        currentState = self.initialState()
        print(f"\033[32mEstado inicial: {self.miniStates[currentState]['name']}\033[0m")
        for letter in string:
            if letter not in self.alphabet:
                print(f"\033[31mLa letra {letter} no esta en el alfabeto\033[0m")
                return False
            if letter not in self.miniStates[currentState]["transitions"]:
                print(f"\033[31mLa letra {letter} no tiene transicion en el estado actual\033[0m")
                return False
            currentState = self.miniStates[currentState]["transitions"][letter]
            print(f"\033[32mEstado actual: {self.miniStates[currentState]['name']}\033[0m")
        return self.miniStates[currentState]["finish"]

    def getStateID(self):
        toReturn = f"s{self.nStates}"
        self.nStates += 1
        return toReturn
    
    def initialState(self):
        for state in self.miniStates:
            if self.miniStates[state]["initial"]:
                return state
    
    def generateTree(self):
        self.diagram = Digraph()
        self.diagram.node("start", "inicio", shape='point', width='0')

        for state in self.miniStates:
            shape = "circle"
            if(self.miniStates[state]["finish"]):
                shape = "doublecircle"
            self.diagram.node(self.miniStates[state]["name"], self.miniStates[state]["name"],shape=shape)

        for state in self.miniStates:
            for transition in self.miniStates[state]["transitions"]:
                node = self.miniStates[state]["transitions"][transition]
                self.diagram.edge(self.miniStates[state]["name"], self.miniStates[node]["name"], label=transition)

        self.diagram.edge("start",self.miniStates[self.initialState()]["name"])

        self.diagram.render(f'AAImageAutomataMiniDirect/MinDFA{self.fileNumber}', format='png', cleanup=False)

    def minimization(self):
        initalPartition = [self.noAcceptStates, self.acceptStates]
        newPartition = []

        table = {}
        for state in self.dfaStates:
            transicions = {}
            for letter in self.alphabet:
                transicions[letter] = self.dfaStates[state]["transitions"][letter]
            table[state] = transicions

        
        while initalPartition != newPartition:
            if newPartition:
                initalPartition = newPartition
            newPartition = []
            for part in initalPartition:
                subgroup = {}
                for state in part:
                    transition = tuple(table[state][letter] for letter in self.alphabet)
                    if transition not in subgroup:
                        subgroup[transition] = []
                    subgroup[transition].append(state)
                newPartition.extend(subgroup.values())


        self.miniStates = {}
        for part in newPartition:
            newStateName = sum(part, ())
            self.miniStates[newStateName] = {
                "name": self.getStateID(),
                "initial": any(True if "initial" in self.dfaStates[state] else False for state in part),
                "finish": any(self.dfaStates[state]["accept"] for state in part),
                "transitions": {},
                "state": newStateName
            }
        

        for part in newPartition:
            state = sum(part, ())
            for letter in self.alphabet:
                transition = table[part[0]][letter]
                for newState in self.miniStates:
                    if transition == self.miniStates[newState]["state"]:
                        self.miniStates[state]["transitions"][letter] = newState
