
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def add(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head
        while current.next:
            current = current.next

        current.next = new_node

    def delete_at_beginning(self):
        if self.head is None:
            return None

        data = self.head.data
        self.head = self.head.next
        return data

    def delete(self, data):
        current = self.head
        previous = None

        while current:
            if current.data == data:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True

            previous = current
            current = current.next

        return False

    def search(self, data):
        current = self.head
        position = 1

        while current:
            if current.data == data:
                return position

            current = current.next
            position += 1

        return None

    def get_elements(self):
        elements = []
        current = self.head

        while current:
            elements.append(current.data)
            current = current.next

        return elements
