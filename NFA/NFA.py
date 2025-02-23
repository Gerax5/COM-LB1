from graphviz import Digraph
from Models.Node import Node
from Models.AutomataNode import AutomataNode
from Models.Estados import State
import sys

class NFAD():
    def __init__(self, stack,fileNumber = 0):
        self.fileNumber = fileNumber
        self.operators = ['*']
        self.binary_operators = ['^', '|', '.']
        self.diagram = Digraph()
        self.diagram.node("start", "inicio", shape='point', width='0')
        seed = stack[0]
        self.states = []
        self.automataStack = []
        self.nodeCount = 1
        self.treeReader(seed)
        self.finishAutomata()

    def shutDownSistem(self, error):
        print(f"\033[31m{error}\033[0m")
        sys.exit(1)

    def getStates(self):
        return self.states

    def getStateByNodeNumber(self, nodeNumber):
        for state in self.states:
            state: State = state

            if state.nodeNumber == nodeNumber:
                return state
        
    def finishAutomata(self):
        n = self.getNodeCount()
        nodeNumber = "F"+n
        automata: AutomataNode = self.automataStack.pop()
        self.diagram.edge("start", automata.initialNode)

        state: State = self.getStateByNodeNumber(automata.initialNode)
        state.initial = True

        self.diagram.node(nodeNumber, n, shape='doublecircle')

        self.diagram.edge(automata.finishNode, nodeNumber, label="ε")

        state2: State = self.getStateByNodeNumber(automata.finishNode)
        fstate: State = State(nodeNumber, finish=True)
        state2.conectState("ε",fstate.nodeNumber)
        self.states.append(fstate)

        self.diagram.render(f'AAImageAutomataNFA/NFA{self.fileNumber}', format='png', cleanup=False)

    def getNodeCount(self):
        toReturn = self.nodeCount
        self.nodeCount += 1
        return str(toReturn)

    def varibale(self, node: Node, edgeName: str):
        n1 = self.getNodeCount() 
        n2 = self.getNodeCount()
        nodeNumber = "V"+n1
        nodeNumber2 = "V"+n2
        self.diagram.node(nodeNumber, n1, shape='circle')
        self.diagram.node(nodeNumber2, n2, shape='circle')
        self.diagram.edge(nodeNumber, nodeNumber2, label=edgeName)

        state: State = State(nodeNumber)
        state2: State = State(nodeNumber2)
        state.conectState(edgeName, state2.nodeNumber) 
        self.states.append(state)
        self.states.append(state2)

        automata = AutomataNode(nodeNumber, nodeNumber2)
        self.automataStack.append(automata)
        

    def kleene(self):
        n1 = self.getNodeCount()
        n2 = self.getNodeCount()
        automata: AutomataNode = self.automataStack.pop()
        nodeNumber = "k"+n1
        NodeNumber2 = "k"+n2

        self.diagram.node(nodeNumber, n1, shape='circle')
        self.diagram.node(NodeNumber2, n2, shape='circle')
        nState = State(nodeNumber)
        nState2 = State(NodeNumber2)

        self.diagram.edge(automata.finishNode, automata.initialNode, label="ε")
        state: State = self.getStateByNodeNumber(automata.finishNode)
        state2: State = self.getStateByNodeNumber(automata.initialNode)
        state.conectState("ε", state2.nodeNumber)

        self.diagram.edge(nodeNumber, NodeNumber2, label="ε")
        nState.conectState("ε", nState2.nodeNumber)

        self.diagram.edge(nodeNumber, automata.initialNode, label="ε")
        nState.conectState("ε", state2.nodeNumber)

        self.diagram.edge(automata.finishNode, NodeNumber2, label="ε")
        state.conectState("ε", NodeNumber2)

        self.states.append(nState)
        self.states.append(nState2)

        aut = AutomataNode(nodeNumber, NodeNumber2)
        self.automataStack.append(aut)

    def concat(self):
        automata: AutomataNode = self.automataStack.pop()
        automata2: AutomataNode = self.automataStack.pop()

        self.diagram.edge(automata2.finishNode, automata.initialNode, label="ε")
        state: State = self.getStateByNodeNumber(automata2.finishNode)
        state2: State = self.getStateByNodeNumber(automata.initialNode)
        state.conectState("ε", state2.nodeNumber)

        aut = AutomataNode(automata2.initialNode, automata.finishNode)
        self.automataStack.append(aut)

    def nodeOr(self):
        n1 = self.getNodeCount()
        n2 = self.getNodeCount()
        automata: AutomataNode = self.automataStack.pop()
        automata2: AutomataNode = self.automataStack.pop()
        nodeNumber = "o"+n1
        NodeNumber2 = "o"+n2

        nState = State(nodeNumber)
        nState2 = State(NodeNumber2)

        self.diagram.node(nodeNumber, n1, shape='circle')
        self.diagram.node(NodeNumber2, n2, shape='circle')

        self.diagram.edge(nodeNumber, automata.initialNode, label="ε")
        self.diagram.edge(nodeNumber, automata2.initialNode, label="ε")
        nState.conectState("ε",automata.initialNode)
        nState.conectState("ε", automata2.initialNode)

        self.diagram.edge(automata.finishNode, NodeNumber2, label="ε")
        self.diagram.edge(automata2.finishNode, NodeNumber2, label="ε")
        state: State = self.getStateByNodeNumber(automata.finishNode)
        state2: State = self.getStateByNodeNumber(automata2.finishNode)
        state.conectState("ε", NodeNumber2)
        state2.conectState("ε", NodeNumber2)

        self.states.append(nState)
        self.states.append(nState2)

        aut = AutomataNode(nodeNumber, NodeNumber2)
        self.automataStack.append(aut)


    def treeReader(self, node: Node):
        transition = "".join(node.getObject())
        # print(node)
        if node.getIsOperator():
            if transition in self.operators:
                self.treeReader(node.getChilds()[0])
                self.kleene()
            else:
                self.treeReader(node.getChilds()[0])
                self.treeReader(node.getChilds()[1])
                if transition == "|":
                    self.nodeOr()
                elif transition == ".":
                    self.concat()
        else:
            self.varibale(node, transition)
        return