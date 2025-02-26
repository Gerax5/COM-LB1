from NFA.NFA import NFAD
from DFA.DFA import DFA
from MiniDFA.MiniDFA import MiniDFA
from SintacticTree.Tree import Tree
from DirectDFA.DirectDFA import DirectDFA
from Models.Node import Node
from GenericMiniDFA.MiniDFA import GenericMiniDFA


flag = True

while flag:

    exp = input("\033[35mIngre su expresion regular: \033[0m")
    if (exp != ""):
        flag = False

# Arbol sintactico
tree = Tree(exp, 0)
stack = tree.getStack()
alphabet = tree.getAlphabet()

# NFA
nfa = NFAD(stack, 0)

# DFA
dfa = DFA(nfa.getStates(), alphabet, 0)

# MinDFA
minidfa = MiniDFA(dfa.states, dfa.acceptStates, dfa.noAcceptStates, tree.getAlphabet(), 0)

# DirectDFA
tree = Tree(exp, 1, True)
stack = tree.getStack()
alphabet = set(alphabet)
alphabet = list(alphabet)
ddfa = DirectDFA(stack, alphabet)


v = input("Quiere minimizar el DFA Directo? (y/n): ")
if v == "y":
    print("Minimizando DFA Directo")
    ddfa = GenericMiniDFA(ddfa.transitions, ddfa.acceptStates, ddfa.noAcceptStates, alphabet, 0)


flag = True
while flag:
    print("\033[32mPara poder salir del programa ingrese 'exit'\033[0m")
    word = input("\033[35mIngre su palabra a validar: \033[0m")

    if (word == "exit" or word == ""):
        break

    response = dfa.validateNFARegularExpression(word)
    print("\033[35mSe termino de validar la expression en AFN\033[0m")
    if(response):
        print("\033[32mSi\033[0m")
    else:
        print("\033[31mNo\033[0m")

    response = dfa.validaAFDRegularExpression(word)
    print("\033[35mSe termino de validar la expression en AFD\033[0m")
    if(response):
        print("\033[32mSi\033[0m")
    else:
        print("\033[31mNo\033[0m")

    response = minidfa.validateRegularExpression(word)
    print("\033[35mSe termino de validar la expression en Min AFD\033[0m")
    if(response):
        print("\033[32mSi\033[0m")
    else:
        print("\033[31mNo\033[0m")

    response = ddfa.recognize(word)
    print("\033[35mSe termino de validar la expression en el DFA con el metodo directo\033[0m")
    if(response):
        print("\033[32mSi\033[0m")
    else:
        print("\033[31mNo\033[0m")







