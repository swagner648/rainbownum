class Set:
    def __init__(self, set, next):
        self.data = set
        self.next = next


class SetLinkedList:
    def __init__(self):
        self.head = Set("\nSENTINEL", None)
        self.tail = self.head
        self.len = 0

    def __repr__(self):
        return recur_print(self.head)

    def add_set(self, set):
        self.tail.next = Set(set, None)
        self.tail = self.tail.next
        self.len += 1


class Coloring:
    def __init__(self, coloring, next):
        self.data = coloring
        self.next = next


class ColoringLinkedList:
    def __init__(self):
        self.head = Coloring(["SENTINEL"], None)
        self.tail = self.head
        self.len = 0
        self.maxColors = 0

    def __repr__(self):
        return recur_print(self.head)

    def add_coloring(self, coloring, colors):
        if colors < self.maxColors:
            return
        if colors > self.maxColors:
            self.new_max_coloring(list(coloring), colors)
            return
        self.tail.next = Coloring(list(coloring), None)
        self.tail = self.tail.next
        self.len += 1

    def new_max_coloring(self, coloring, colors):
        self.head = Coloring(coloring, None)
        self.tail = self.head
        self.len = 1
        self.maxColors = colors


def recur_print(node):
    try:
        if node.next is not None:
            return str(node.data) + ", " + recur_print(node.next)
        return str(node.data)
    except RecursionError:
        print("Not all colorings could be printed.")
        return str(node.data)