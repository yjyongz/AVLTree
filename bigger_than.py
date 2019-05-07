class Node:
    def __init__(self, value):
        self.value = value
        self.size = 1
        self.height = 1
        self.left = None
        self.right = None 

class BST:
    def __init__(self):
        self.root = None
        pass
    # return new root 
    def insert(self, value):
        def rightRotate(node):
            newroot = node.left
            T2 = newroot.right

            newroot.right = node
            node.left =  T2

            node.height = max(getHeight(node.left), getHeight(node.right)) + 1 
            node.size = getSize(node.left) + getSize(node.right) + 1

            newroot.height = max(getHeight(newroot.left), getHeight(newroot.right)) + 1 
            newroot.size = getSize(newroot.left) + getSize(newroot.right) + 1

            return newroot

        def getSize(node):
            if not node:
                return 0
            return node.size

        def leftRotate(node):
            newroot = node.right
            T2 = newroot.left

            newroot.left = node
            node.right =  T2

            node.height = max(getHeight(node.left), getHeight(node.right)) + 1 
            node.size = getSize(node.left) + getSize(node.right) + 1

            newroot.height = max(getHeight(newroot.left), getHeight(newroot.right)) + 1 
            newroot.size = getSize(newroot.left) + getSize(newroot.right) + 1

            return newroot

        def getHeight(node): 
            if not node:
                return 0
            return node.height 
    
        def getBalance(node):
            if not node:
                return 0
            return getHeight(node.left) - getHeight(node.right)

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
                ccount += getSize(node.left) + 1
            elif node.value > value:
                node.left = iinsert(node.left, value)
            
            node.height = max(getHeight(node.left), getHeight(node.right)) + 1 
            node.size = getSize(node.left) + getSize(node.right) + 1 
            index = getBalance(node)
            # right right
            if index < -1 and node.right.value < value:
                # left rotate
                return leftRotate(node)

            # left left
            if index > 1 and node.left.value > value:
                # left rotate
                return rightRotate(node)
            
            # right left
            if index < -1 and node.right.value > value:
                # left rotate
                node.right = rightRotate(node.right)
                return leftRotate(node)

            # left right
            if index > 1 and node.left.value < value:
                # left rotate
                node.left = leftRotate(node.left)
                return leftRight(node)
            return node

        self.root = iinsert(node, value)
        #print (self.root, ccount)
        #print ("count: ",ccount)
        return ccount

arr = [12, 1, 2, 3, 0, 11, 4]
tree = BST()

ans = []
jdx = 0
for idx in range(len(arr)-1, -1, -1):
    c = tree.insert(arr[idx])
    #print (c)
    #print (item,c)
    ans.insert(0, jdx-c)
    jdx+=1

print (ans)
