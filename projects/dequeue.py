class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class DeQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, data):
        new_node = Node(data)

        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

        return data

    def dequeue(self):
        if self.is_empty():
            return None

        removed_data = self.front.data
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return removed_data

    def display(self):
        elements = []
        current = self.front

        while current:
            elements.append(current.data)
            current = current.next

        return elements