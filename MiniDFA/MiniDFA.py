
from graphviz import Digraph


class MiniDFA():
    def __init__(self, dfaStates: set, acceptStates: list, noAcceptStates: list, alphabet: list, fileNumber = 0):
        self.dfaStates = dfaStates
        self.acceptStates = acceptStates
        self.noAcceptStates = noAcceptStates
        self.alphabet = alphabet
        self.fileNumber = fileNumber
        self.nStates = 0
        self.minimization()
        self.generateTree()

    def validateRegularExpression(self, regularExpression):
        print(f"\033[32mExpresion a evaluar en Minimo AFD: {regularExpression}\033[0m")
        stackRegular = list(regularExpression)
        stackRegular = stackRegular[::-1]

        curState = self.initialState()
        print(f"Empieza en el estado: {self.miniStates[curState][id]}")

        while stackRegular:
            curChar = stackRegular.pop()

            transitions = list(self.miniStates[curState]["transition"])

            flagCharacters = False

            while transitions:
                curTransition = transitions.pop()
                if curChar in curTransition:
                    curState = self.miniStates[curState]["transition"][curTransition]["to"]
                    print(f"Con la letra: {curChar}, se mueve: {self.miniStates[curState][id]}")
                    flagCharacters = True

                if curChar == " ":
                    flagCharacters = True
            
            if not flagCharacters:
                print(f"Entrada no valida: {curChar}")
                break
        
        if not flagCharacters:
            return False


        return self.miniStates[curState]["finish"]

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
            self.diagram.node(state, self.miniStates[state][id],shape=shape)

        for state in self.miniStates:
            for transition in self.miniStates[state]["transition"]:
                self.diagram.edge(state, self.miniStates[state]["transition"][transition]["to"], label=transition)

        self.diagram.edge("start",self.initialState())

        self.diagram.render(f'AutomataMini/MinDFA{self.fileNumber}', format='png', cleanup=False)

    def minimization(self):
        initalPartition = [self.noAcceptStates, self.acceptStates]
        newPartition = []

        table = {}
        for state in self.dfaStates:
            transicions = {}
            for letter in self.alphabet:
                transicions[letter] = self.dfaStates[state]["transition"][letter]["to"]
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
            newStateName = "".join(part)
            self.miniStates[newStateName] = {
                id: self.getStateID(),
                "initial": any(self.dfaStates[state]["initial"] for state in part),
                "finish": any(self.dfaStates[state]["finish"] for state in part),
                "originalStates": part,
                "transition": {}
            }

        for part in newPartition:
            state = "".join(part)
            for letter in self.alphabet:
                transition = table[part[0]][letter]
                for newState in self.miniStates:
                    if transition in self.miniStates[newState]["originalStates"]:
                        self.miniStates[state]["transition"][letter] = {"to": newState}

        # print(self.miniStates)