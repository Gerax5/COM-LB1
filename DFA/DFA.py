from graphviz import Digraph
from Models.Estados import State
class DFA():
    def __init__(self, states, alphabet, fileNumber = 0):
        self.alphabet = alphabet
        self.nfaStats = states
        self.fileNumber = fileNumber
        self.nStates = 0
        self.states = {}
        self.acceptStates = []
        self.noAcceptStates = []
        self.convertToDFA()
        self.generateTree()

    def getInitialState(self):
        for state in self.nfaStats:
            state: State = state
            if state.initial:
                return state
            
    def getStateByNodeNumber(self, nodeNumber):
        for state in self.nfaStats:
            state: State = state

            if state.nodeNumber == nodeNumber:
                return state
            
    # Re f python no aguanto la recursividad JAJAJAJ
    # def eClosure(self, state, eclouse):
    #     state: State = state
    #     eclouse.append(state.nodeNumber)
    #     for i in range(len(state.transitions)):
    #         if state.transitions[i] == "ε":
    #             self.eClosure(self.getStateByNodeNumber(state.states[i]),eclouse)
    #     return eclouse

    def eClosure(self, start_state, eclouse):
        stack = [start_state]  
        eclouse = set()        

        while stack:
            state = stack.pop()
            if state.nodeNumber not in eclouse:
                eclouse.add(state.nodeNumber)
                
                for i in range(len(state.transitions)):
                    if state.transitions[i] == "ε":
                        nextState = self.getStateByNodeNumber(state.states[i])
                        if nextState.nodeNumber not in eclouse:
                            stack.append(nextState)

        return list(eclouse)
    
    def getStateID(self):
        toReturn = f"s{self.nStates}"
        self.nStates += 1
        return toReturn
    
    def hasAcceptState(self, state):
        for value in state:
            stat: State = self.getStateByNodeNumber(value)
            if stat.finish:
                return True
        return False
    
    def move(self, state, letter, afnTest = False):
        newState = []
        for nodeNumber in state:
            st: State = self.getStateByNodeNumber(nodeNumber)
            #print(st.transitions)
            for i in range(len(st.transitions)):
                if letter in st.transitions[i]:
                    # print(f"\033[32mCon la letra se movio a: {st.states[i]}\033[0m")
                    newState.append(st.states[i])

        stateName = "".join(state)
        newStateName = "".join(newState)


        # if newState != []:
        #     print("Se movio a estos estados: ")
        # else:
        #     print("No se movio a nada")
        
        # for i in newState:
        #     print(f"->{i}")

        # print("Aplicando eClosure se movio a:")

        eClosure = []
        if newStateName != "":
            if len(newState) > 1:
                tempEclosure = {}
                for nState in newState:
                    eClosure = self.eClosure(self.getStateByNodeNumber(nState), eClosure)
                    for closure in eClosure:
                        if closure not in tempEclosure:
                            tempEclosure[closure] = ""
                eClosure = list(tempEclosure.keys())
            else:
                eClosure = self.eClosure(self.getStateByNodeNumber(newStateName), eClosure)

        # for i in eClosure:
        #     print(f"->{i}")

        if afnTest:
            return eClosure

        # Todo lo que esta abjo es para el dfa

        newStateName = "".join(eClosure)
        
        self.states[stateName].setdefault("transition", {})[letter] = {"to": newStateName}

        if newState == []:
           newState = ["vacio"]
        #print(newState)
        newState = tuple(newState)


        if newStateName not in self.states:
            newID = self.getStateID()
            self.states[newStateName] = {id: newID, "initial": False, "finish": False, "originalState": eClosure}
            self.states[newStateName]["finish"] = self.hasAcceptState(eClosure)

            self.statesToProcess.append(newStateName)

    def validaAFDRegularExpression(self, regularExpression: str):
        print(f"\033[32mExpresion a evaluar en AFD: {regularExpression}\033[0m")
        stackRegular = list(regularExpression)
        stackRegular = stackRegular[::-1]

        curState = self.initialStateDFA()
        print(f"Empieza en el estado: {self.states[curState][id]}")

        while stackRegular:
            curChar = stackRegular.pop()

            transitions = list(self.states[curState]["transition"])

            flagCharacters = False

            while transitions:
                curTransition = transitions.pop()
                if curChar in curTransition:
                    curState = self.states[curState]["transition"][curTransition]["to"]
                    print(f"Con la letra: {curChar}, se mueve: {self.states[curState][id]}")
                    flagCharacters = True
            
            if not flagCharacters:
                print(f"Entrada no valida: {curChar}")
                break
        
        if not flagCharacters:
            return False

        return self.states[curState]["finish"]
            
            




    def validateNFARegularExpression(self, regularExpression):
        print("\033[35mAntes de empezar hay que tomar en cuenta:\n 1) Los estados tienen una letra ignorar esa letra\n 2) Revisar con la imagen generada dependiendo del automata \033[0m")
        print(f"\033[32mExpresion a evaluar en AFN: {regularExpression}\033[0m")
        initialState: State = self.getInitialState()
        eCloasure = []
        estadoActual = self.eClosure(initialState, eCloasure)
        print("Entro la expresion regular se encuentra en estos estados: ")
        for i in estadoActual:
            print(f"->{i}")

        #print(self.move(s0, regularExpression[0]))
        
        for letter in regularExpression:
            print(f"Entro la letra: {letter}")
            estadoActual = self.move(estadoActual, letter, True)
            if estadoActual == []:
                print(f"\033[31mEntrada no valida {letter}\033[0m")
                return False

        for state in estadoActual:
            st: State = self.getStateByNodeNumber(state)
            if st.finish:
                return True
            
        return False

        #print(estadoActual)





    def convertToDFA(self):
        #Aun no
        initialState: State = self.getInitialState()
        eCloasure = []
        s0 = self.eClosure(initialState, eCloasure)
        stateName = "".join(s0)
        newID = self.getStateID()
        self.states[stateName] = {id: newID, "initial": True, "finish": False, "originalState": s0}
        self.states[stateName]["finish"] = self.hasAcceptState(s0)
        
        
        self.statesToProcess= [stateName]

        while self.statesToProcess:
            currenState = self.statesToProcess.pop()
            currenState = self.states[currenState]["originalState"]
            for letter in self.alphabet:
                self.move(currenState, letter)

            print

        # for key in self.states.keys():
        #     print(key)


         
        # for i in self.states:
        #     print(i)
        #     print(self.states[i])


    def initialStateDFA(self):
        for state in self.states:
            if self.states[state]["initial"]:
                return state

    def generateTree(self):
        self.diagram = Digraph()
        self.diagram.node("start", "inicio", shape='point', width='0')


        for state in self.states:
            shape = "circle"
            if(self.states[state]["finish"]):
                self.acceptStates.append(state)
                shape = "doublecircle"
            else:
                self.noAcceptStates.append(state)
            self.diagram.node(state, self.states[state][id],shape=shape)

        for state in self.states:
            for transition in self.states[state]["transition"]:
                self.diagram.edge(state, self.states[state]["transition"][transition]["to"], label=transition)

        self.diagram.edge("start",self.initialStateDFA())

        self.diagram.render(f'AAImageAutomataDFA/DFA{self.fileNumber}', format='png', cleanup=False)
