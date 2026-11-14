from node import Node


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, url, metadata=None):
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
        if node is None:
            return 0

        valid_node = self.head
        while valid_node is not None and valid_node is not node:
            valid_node = valid_node.next
        if valid_node is None:
            return 0
        
        current = node.next
        removed = 0
        while current is not None:
            next_node = current.next
            current.prev = None
            current.next = None
            removed += 1
            current = next_node

        node.next = None
        self.tail = node
        self.size -= removed
        return removed

    def remove_head(self):
        if self.head is None:
            return None
        cur = self.head
        self.head = cur.next

        if self.head is not None:
            self.head.prev=None
        else:
            self.tail = None

        cur.prev=None
        cur.next=None
        self.size-=1
        return cur

    def clear(self):
        cur = self.head
        while cur is not None:
            next_node = cur.next
            cur.prev = None
            cur.next = None
            cur = next_node
        self.head = None
        self.tail = None
        self.size = 0 