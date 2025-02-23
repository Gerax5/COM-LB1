from Models.Node import Node

class DirectDFA:
    OPERATORS = ["*"]
    BINARY_OPERATORS = ["^", "|", "."]

    def __init__(self, stack: list[Node]):
        self.currentLeafNumber = 0
        self.leaves = []
        seed = stack[0]
        self.enumerateLeaves(seed)

    def enumerateLeaves(self, node: Node):
        if node.getIsOperator():
            object = "".join(node.getObject())
            if object in self.BINARY_OPERATORS: 
                self.enumerateLeaves(node.getChilds()[0])
                self.enumerateLeaves(node.getChilds()[1])
            else:
                self.enumerateLeaves(node.getChilds()[0])
        else:
            print("".join(node.getObject()))
            node.leafNumber = self.currentLeafNumber
            self.currentLeafNumber += 1
            self.leaves.append(node)

            print(node.getObject(), node.leafNumber)

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
            node.nullable = False