class Node:
    def __init__(self, value):
        self.value = value
        self.size = 1
        self.height = 1
        self.left = None
        self.right = None
        self.duplicate = 0 # how many duplicate elements

class BST:
    def __init__(self):
        self.root = None
        pass

    def rightRotate(self, node):
        newroot = node.left
        T2 = newroot.right

        newroot.right = node
        node.left =  T2

        node.height = max(self.getHeight(node.left), self.getHeight(node.right)) + 1
        node.size = self.getSize(node.left) + self.getSize(node.right) + 1

        newroot.height = max(self.getHeight(newroot.left), self.getHeight(newroot.right)) + 1
        newroot.size = self.getSize(newroot.left) + self.getSize(newroot.right) + 1

        return newroot

    def getSize(self, node):
        if not node:
            return 0
        return node.size

    def leftRotate(self, node):
        newroot = node.right
        T2 = newroot.left

        newroot.left = node
        node.right =  T2

        node.height = max(self.getHeight(node.left), self.getHeight(node.right)) + 1
        node.size = self.getSize(node.left) + self.getSize(node.right) + 1

        newroot.height = max(self.getHeight(newroot.left), self.getHeight(newroot.right)) + 1
        newroot.size = self.getSize(newroot.left) + self.getSize(newroot.right) + 1

        return newroot

    def getHeight(self, node):
        if not node:
            return 0
        return max(self.getHeight(node.left), self.getHeight(node.right)) + 1

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    # return new root
    def insert(self, value):
        if self.root == None:
            self.root = Node(value)
            return 0

        node = self.root
        ccount = 0
        def iinsert(node, value):
            nonlocal ccount
            if not node:
                return Node(value)

            if node.value < value:
                node.right = iinsert(node.right, value)
                ccount += self.getSize(node.left) + 1
            elif node.value > value:
                node.left = iinsert(node.left, value)
            else:
                node.duplicate+=1
                return node

            node.height = max(self.getHeight(node.left), self.getHeight(node.right)) + 1
            node.size = self.getSize(node.left) + self.getSize(node.right) + 1
            index = self.getBalance(node)
            # right right
            if index < -1 and node.right.value < value:
                # left rotate
                return self.leftRotate(node)

            # left left
            if index > 1 and node.left.value > value:
                # left rotate
                return self.rightRotate(node)

            # right left
            if index < -1 and node.right.value > value:
                # left rotate
                node.right = self.rightRotate(node.right)
                return self.leftRotate(node)

            # left right
            if index > 1 and node.left.value < value:
                # left rotate
                node.left = self.leftRotate(node.left)
                return self.rightRotate(node)
            return node

        self.root = iinsert(node, value)
        #print (self.root, ccount)
        #print ("count: ",ccount)
        return ccount
    
    def getMin(self, node):
        if not node:
            return None
        while node and node.left:
            node = node.left
        return node

    def getMax(self, node):
        if not node:
            return None
        while node and node.right:
            node = node.right
        return node

    def delete(self, value):
        node = self.root
        if not node:
            return None
        def ddelete(node, value):
            if not node:
                return
            if node.value > value:
                node.left = ddelete(node.left, value)
            elif node.value < value:
                node.right = ddelete(node.right, value)
            else:
                # found
                if node.duplicate > 0:
                    node.duplicate -= 1
                    return node
                else:
                    # delete node 
                    if node.left == None:
                        temp = node.right
                        node = None 
                        return temp
                    elif node.right == None:
                        temp = node.left
                        node = None
                        return temp
                    else:
                        minNode = self.getMin(node.right)
                        node.value = minNode.value
                        node.size -= 1
                        node.right = ddelete(node.right, minNode.value)
                        
            node.height = max(self.getHeight(node.left), self.getHeight(node.right)) + 1
            node.size = self.getSize(node.left) + self.getSize(node.right) + 1
            index = self.getBalance(node)

            # right right
            if index < -1 and self.getbalance(node.right) <= 0:
                # left rotate
                return self.leftRotate(node)

            # left left
            if index > 1 and self.getBalance(node.left) >= 0:
                # left rotate
                return self.rightRotate(node)

            # right left
            if index < -1 and self.getBalance(node.right) >= 0:
                # left rotate
                node.right = self.rightRotate(node.right)
                return self.leftRotate(node)

            # left right
            if index > 1 and self.getBalance(node.left) <= 0:
                # left rotate
                node.left = self.leftRotate(node.left)
                return self.leftRight(node)
            return node
        self.root = ddelete(node, value)
        return self.root
    
    def preorder(self):
        node = self.root
        def dfs(node):
            if not node:
                return
            print (node.value, end=" ")
            dfs(node.left)
            dfs(node.right)
        dfs(node)
        print ()

class Plane:
    def __init__(self):
        self.x = BST()
        self.y = BST()
        self.rectangle = [None, None]
        self.q = []
    
    def push(self, point):
        self.q += [point]
        self.x.insert(point[0])
        self.y.insert(point[1])
        
        xroot = self.x.root 
        yroot = self.y.root 
        leftBottom = [self.x.getMin(xroot), self.y.getMin(yroot)]
        rightUp = [self.x.getMax(xroot), self.y.getMax(yroot)]
        self.rectangle = [leftBottom, rightUp]
   
    def pop(self):
        p = self.q.pop(0)
        print ("delete ", p)
        self.x.delete(p[0])
        self.y.delete(p[1])

        xroot = self.x.root 
        yroot = self.y.root 
        self.x.preorder()
        self.y.preorder()
        leftBottom = [self.x.getMin(xroot), self.y.getMin(yroot)]
        rightUp = [self.x.getMax(xroot), self.y.getMax(yroot)]
        self.rectangle = [leftBottom, rightUp]

    def getRectangle(self):
        result = []
        for each in self.rectangle:
            if each[0]:
                result.append([each[0].value, each[1].value])
        return result


plane = Plane()
string = [[2,3],[0,0],[1,1],[4,5],[0,5]]

for point in string:
    plane.push(point)
    print (plane.getRectangle())

print ("----")

for point in string:
    plane.pop()
    print (plane.getRectangle())
