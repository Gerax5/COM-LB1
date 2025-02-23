
from NFA.NFA import NFAD
from DFA.DFA import DFA
from MiniDFA.MiniDFA import MiniDFA
from SintacticTree.Tree import Tree
from DirectDFA.DirectDFA import DirectDFA
from Models.Node import Node


lineas = []
with open("1.txt", "r", encoding="utf-8") as file:
    lineas = file.read().splitlines()

newLines = []
tempLine = []
for i in range(len(lineas)):
   tempLine.append(lineas[i])

   if (i+1) % 2 == 0:
      newLines.append(tempLine)
      tempLine = []


for i in range(len(newLines)):
    isAllRight = True
    line = newLines[i]
    tree = Tree(line[0], i)
    stack = tree.getStack()

    nfa = NFAD(stack, i)

    dfa = DFA(nfa.getStates(), tree.getAlphabet(), i)

    response = dfa.validateNFARegularExpression(line[1])
    print("\033[35mSe termino de validar la expression en AFN\033[0m")
    if(response):
        print("\033[32mSi\033[0m")
    else:
        print("\033[31mNo\033[0m")

    response = dfa.validaAFDRegularExpression(line[1])
    print("\033[35mSe termino de validar la expression en AFD\033[0m")
    if(response):
        print("\033[32mSi\033[0m")
    else:
        print("\033[31mNo\033[0m")

    minidfa = MiniDFA(dfa.states, dfa.acceptStates, dfa.noAcceptStates, tree.getAlphabet(), i)

    response = minidfa.validateRegularExpression(line[1])
    print("\033[35mSe termino de validar la expression en Min AFD\033[0m")
    if(response):
        print("\033[32mSi\033[0m")
    else:
        print("\033[31mNo\033[0m")

    tree = Tree(line[0], i+10, True)
    stack = tree.getStack()

    dfa = DirectDFA(stack)







