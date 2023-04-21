from typing import TypeVar
from ride import Ride

T = TypeVar('T', bound='Node')

# Node creation
class Node():
    next_id = 0

    def __init__(self: T, item: Ride) -> None:
        self.id = Node.next_id
        Node.next_id += 1
        self.item = item
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1
        self.value = None

    def __eq__(self: T, other: T) -> bool:
        return self.id == other.id

    def __repr__(self: T) -> str:
        return "ID: " + str(self.id) + " Value: " + str(self.item)

    def GetColor(self: T) -> str:
        return "black" if self.color == 0 else "red"

    def SetColor(self: T, color: str) -> None:
        if color == "black":
            self.color = 0
        elif color == "red":
            self.color = 1
        else:
            raise Exception("Unknown color")

    def RedNode(self: T) -> bool:
        return self.color == 1

    def BlackNode(self: T) -> bool:
        return self.color == 0

    def IsNull(self: T) -> bool:
        return self.id == -1

T = TypeVar('T', bound='RedBlackTree')

# Red Black Tree Creation
class RedBlackTree():
    def __init__(self: T) -> None:
        self.TNULL = Node(Ride(-1, -1, -1))
        self.TNULL.id = -1
        self.TNULL.SetColor("black")
        self.root = self.TNULL
        self.size = 0

    searchRes = ""

    # Searches the tree for a given range of rides between a start and end
    def RideRangeSearcher(self: T, node: Node, rangeStart: int, rangeEnd: int):
        if node.IsNull():
            return
        if node.item.rideNumber >= rangeStart:
            self.RideRangeSearcher(node.left, rangeStart, rangeEnd)
        if node.item.rideNumber >= rangeStart and node.item.rideNumber <= rangeEnd:
            self.searchRes += str(node.item) + ","
        if node.item.rideNumber <= rangeEnd:
            self.RideRangeSearcher(node.right, rangeStart, rangeEnd)
    
    
    # Search the tree
    def TreeSearcher(self: T, node: Node, key: int) -> Node:
        if node.IsNull() or key == node.item.rideNumber:
            return node

        if key < node.item.rideNumber:
            return self.TreeSearcher(node.left, key)
        return self.TreeSearcher(node.right, key)

    # Balancing the tree after deletion
    def FixDelete(self: T, x: Node) -> None:
        while x != self.root and x.BlackNode():
            if x == x.parent.left:
                s = x.parent.right
                if s.RedNode():
                    s.SetColor("black")
                    x.parent.SetColor("red")
                    self.RotateLeft(x.parent)
                    s = x.parent.right

                if s.left.BlackNode() and s.right.BlackNode():
                    s.SetColor("red")
                    x = x.parent
                else:
                    if s.right.BlackNode():
                        s.left.SetColor("black")
                        s.SetColor("red")
                        self.RotateRight(s)
                        s = x.parent.right

                    s.SetColor(x.parent.GetColor())
                    x.parent.SetColor("black")
                    s.right.SetColor("black")
                    self.RotateLeft(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.RedNode():
                    s.SetColor("black")
                    x.parent.SetColor("red")
                    self.RotateRight(x.parent)
                    s = x.parent.left

                if s.left.BlackNode() and s.right.BlackNode():
                    s.SetColor("red")
                    x = x.parent
                else:
                    if s.left.BlackNode():
                        s.right.SetColor("black")
                        s.SetColor("red")
                        self.RotateLeft(s)
                        s = x.parent.left

                    s.SetColor(x.parent.GetColor())
                    x.parent.SetColor("black")
                    s.left.SetColor("black")
                    self.RotateRight(x.parent)
                    x = self.root
        x.SetColor("black")

    # Switches the Red and Black Node to maintain RBTree properties
    def RedBlackSwitch(self: T, u: Node, v: Node) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Node deletion
    def NodeDeleter(self: T, node: Node, key: int) -> None:
        z = self.TNULL
        while not node.IsNull():
            if node.item.rideNumber == key:
                z = node

            if node.item.rideNumber <= key:
                node = node.right
            else:
                node = node.left

        if z.IsNull():
            # print("Cannot find key in the tree")
            return

        y = z
        y_original_color = y.GetColor()
        if z.left.IsNull():
            # If no left child, just scoot the right subtree up
            x = z.right
            self.RedBlackSwitch(z, z.right)
        elif (z.right.IsNull()):
            # If no right child, just scoot the left subtree up
            x = z.left
            self.RedBlackSwitch(z, z.left)
        else:
            y = self.Minimum(z.right)
            y_original_color = y.GetColor()
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.RedBlackSwitch(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.RedBlackSwitch(z, y)
            y.left = z.left
            y.left.parent = y
            y.SetColor(z.GetColor())
        if y_original_color == "black":
            self.FixDelete(x)

        self.size -= 1

    # Balance the tree after Insertion
    def InsertFix(self: T, k: Node) -> None:
        while k.parent.RedNode():
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.RedNode():
                    u.SetColor("black")
                    k.parent.SetColor("black")
                    k.parent.parent.SetColor("red")
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.RotateRight(k)
                    k.parent.SetColor("black")
                    k.parent.parent.SetColor("red")
                    self.RotateLeft(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u.RedNode():
                    u.SetColor("black")
                    k.parent.SetColor("black")
                    k.parent.parent.SetColor("red")
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.RotateLeft(k)
                    k.parent.SetColor("black")
                    k.parent.parent.SetColor("red")
                    self.RotateRight(k.parent.parent)
            if k == self.root:
                break
        self.root.SetColor("black")

    def RangeSearch(self: T, s: int, e: int):
        self.searchRes = ""
        self.RideRangeSearcher(self.root, s, e)
        if self.searchRes == "":
            self.searchRes = "(0,0,0)"
        else:
            self.searchRes = self.searchRes[0:-1]
        return self.searchRes

    def Search(self: T, rideNumber: int) -> Node:
        return self.TreeSearcher(self.root, rideNumber)

    def Minimum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.IsNull():
            return self.TNULL
        while not node.left.IsNull():
            node = node.left
        return node

    def RotateLeft(self: T, x: Node) -> None:
        y = x.right
        x.right = y.left
        if not y.left.IsNull():
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def RotateRight(self: T, x: Node) -> None:
        y = x.left
        x.left = y.right
        if not y.right.IsNull():
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def Insert(self: T, ride: Ride) -> None:
        node = Node(ride)
        node.parent = None
        node.item = ride
        node.left = self.TNULL
        node.right = self.TNULL
        node.SetColor("red")

        y = None
        x = self.root

        while not x.IsNull():
            y = x
            if node.item.rideNumber < x.item.rideNumber:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.item.rideNumber < y.item.rideNumber:
            y.left = node
        else:
            y.right = node

        self.size += 1

        if node.parent is None:
            node.SetColor("black")
            return

        if node.parent.parent is None:
            return

        self.InsertFix(node)

    def Delete(self: T, item: Ride) -> None:
        self.NodeDeleter(self.root, item.rideNumber)

    def __getitem__(self: T, key: int) -> int:
        return self.Search(key).value

    def __setitem__(self: T, key: int, value: int) -> None:
        self.Search(key).value = value
