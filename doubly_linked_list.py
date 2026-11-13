class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, url, metadata):
        new_node = Node(url, metadata)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

        self.size +=1
        return new_node

    def unlink(self, node):
        if node is None:
            return None

        valid_node = self.head
        while valid_node is not None and valid_node is not node:
            valid_node = valid_node.next
        if valid_node is None:
            return None
            
        if node.prev is not None:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next is not None:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None

        self.size -=1
        return node

    def cut_after(self, node):
        if self.head is None or node is None:
            return None

        valid_node = self.head
        while valid_node is not None and valid_node is not node:
            valid_node = valid_node.next
        if valid_node is None:
            return None
        
        current = node.next
        if current is None:
            return None

        removed = 0
        while current is not None:
            next = current.next
            current.prev = None
            current.next = None
            removed +=1
            current = next

        node.next = None
        self.tail = node
        self.size-=removed
        return removed
