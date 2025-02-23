#Muy mal optimizado hay varios fors que puedo hacer con un while, basicamente pierdo milisegundos pero de que sirve sirve jeje
import sys
class InfixToPostfix():

    def __init__(self, isDirectDFA = False):
        self.isDirectDFA  = isDirectDFA

    def shutDownSistem(self, error):
        print(f"\033[31m{error}\033[0m")
        sys.exit(1)
    
    def get_precedence(self, c):
        precedence = {
            '(': 1,
            '|': 2,
            '.': 3,
            '?': 4,
            '*': 4,
            '+': 4,
            '^': 5
        }
        return precedence.get(c,6)

    def getAlphabet(self):
        return self.alphabet

    def format_reg_ex(self, regex):
        self.AllRight = True
        all_operators = ['|', '?', '+', '*', '^']
        binary_operators = ['^', '|']
        res = []
        self.alphabet = []
        
        length = len(regex)
        i = 0
        while i < length:
            c1 = regex[i]
            
            if c1 == '\\':  
                if i + 1 < length:
                    isSpace = f"\{regex[i + 1]}"
                    #print(r"\\n")
                    #if(isSpace == "\\n"):
                        #print("a")
                    res.append(f"\{regex[i + 1]}")
                    self.alphabet.append(f"\{regex[i + 1]}")
                    if i + 2 < len(regex):
                        if(regex[i + 2] not in ")]" and regex[i + 2] not in binary_operators and regex[i + 2] not in all_operators):
                            res.append(".")
                    i += 1  
            elif c1 == "+":
                tempRegex = ["*"]
                tempRegex.append(")")  
                flag = True
                
                openCount = 0
                closeCount = 0
                
                for c in range(1, len(res)+1):
                    currentChar = res[-c]

                    if currentChar == ")":
                        closeCount += 1
                    elif currentChar == "(":
                        openCount += 1

                    if flag:
                        tempRegex.append(currentChar)
                        
                    if openCount == closeCount and openCount > 0:   
                        flag = False
                
                tempRegex.append("(")
                tempRegex.append(".")
                tempRegex.reverse()

                if i + 1  < length:
                    if regex[i+1] not in ")]":
                        tempRegex.append(".")
                for c in tempRegex:
                    res.append(c)
                
            elif c1 == "?":
                tempRegex = ["|","ε",")"]

                if regex[i - 1] in ")]":
                    flag = True
                    pos = 0

                    openCount = 0
                    closeCount = 0

                    for c in range(1, len(res)+1):
                        current_char = res[-c]

                        if current_char == ')':
                            closeCount += 1
                        elif current_char == '(':
                            openCount += 1

                        if flag:
                            pos = -c

                        if openCount == closeCount and openCount > 0:
                            flag = False                 
                    
                    res.insert(pos, "(")
                else:
                    res.insert(-1, "(")

                if i + 1 < length:
                    if regex[i+1] not in ")]":
                        tempRegex.append(".")

                for c in tempRegex:
                    res.append(c)
                
            else:
                if i + 1 < length:
                    if (regex[i] in "[" ):
                        j = i
                        res.append("(")
                        while regex[j+1] != "]":
                            res.append(regex[j+1])
                            self.alphabet.append(regex[j+1])
                            if regex[j + 2] != "]":
                                res.append("|")
                            j += 1
                        res.append(")")
                            
                        i = j + 1
                    else:
                        if(regex[i] == "."):
                            c1 = "\\"+c1
                        c2 = regex[i + 1]
                        res.append(c1)
                        if c1 not in all_operators and c1 not in binary_operators and c1 not in '([' and c1 not in ')]':
                            self.alphabet.append(c1)
                    
                    if (
                        c1 not in '([' and
                        c2 not in ')]' and
                        c2 not in all_operators and
                        c1 not in binary_operators 
                    ):
                        if res and res[-1] != ".":
                            res.append('.')
                    
                        
                else:
                    res.append(c1)

                    if c1 not in all_operators and c1 not in binary_operators and c1 not in '([' and c1 not in ")]":
                        self.alphabet.append(c1)
                    #self.alphabet.append(c1)
            
            i += 1
        ##print("".join(res))
    
        return res

    def isBalance(self, regex):
        stack = []
        i = 0
        algo = ""
        for char in regex:
            if char == "(":
                stack.append(char)
                if(i+1 < len(regex)):
                    if regex[i+1] == ")":
                        self.error = "No es valido parentesis vacios"
                        return False
            elif char == ")":
                if stack and stack[-1] == "(":
                    stack.pop()
                else:
                    return False
            
            i+= 1

        return len(stack) == 0


    def infix_to_postfix(self, regex):
        postfix = []
        stack = []
        
        self.error = ""

        if(not self.isBalance(regex)):
            error = "Esta mal Balanceada la expresion"
            if (self.error):
                error = self.error
            self.shutDownSistem(error)
        
        if self.isDirectDFA:
            regex = f"{regex}#"

        postformat = self.format_reg_ex(regex)


        for c in postformat:
            if c == '(':
                stack.append(c)
                #print(f"Encountered '(': Stack: {stack}")
            elif c == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                    ##print(f"Encountered ')': Popped from Stack to Postfix: {''.join(postfix)}, Stack: {stack}")
                if stack:
                    stack.pop() 
                #print(f"Discarded '(': Stack: {stack}")
            else:
                while (stack and stack[-1] != '(' and 
                       self.get_precedence(stack[-1]) >= self.get_precedence(c)):
                    postfix.append(stack.pop())
                    #print(f"While Loop: Popped from Stack to Postfix: {''.join(postfix)}, Stack: {stack}")
                stack.append(c)
                #print(f"Added '{c}' to Stack: {stack}")
        
        while stack:
            postfix.append(stack.pop())
            #print(f"Final Stack Popped to Postfix: {''.join(postfix)}")
        
        return postfix

 
