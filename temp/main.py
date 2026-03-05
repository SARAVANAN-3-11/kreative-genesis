# Singly Linked List Implementation in Python

class Node:
    """A node in a singly linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """Singly Linked List with basic operations."""
    def __init__(self):
        self.head = None

    def is_empty(self):
        """Check if the list is empty."""
        return self.head is None

    def insert_at_end(self, data):
        """Insert a new node at the end of the list."""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def insert_at_beginning(self, data):
        """Insert a new node at the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete_node(self, key):
        """Delete the first occurrence of a node with the given data."""
        if self.is_empty():
            print("List is empty. Nothing to delete.")
            return

        # If head node holds the key
        if self.head.data == key:
            self.head = self.head.next
            return

        current = self.head
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next

        if current is None:
            print(f"Value {key} not found in the list.")
            return

        prev.next = current.next

    def search(self, key):
        """Search for a node with the given data."""
        current = self.head
        position = 0
        while current:
            if current.data == key:
                return position
            current = current.next
            position += 1
        return -1  # Not found

    def display(self):
        """Display the linked list."""
        if self.is_empty():
            print("List is empty.")
            return
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")


# Example usage
if __name__ == "__main__":
    sll = SinglyLinkedList()

    # Insert elements
    sll.insert_at_end(10)
    sll.insert_at_end(20)
    sll.insert_at_beginning(5)
    sll.insert_at_end(30)

    print("Linked List after insertions:")
    sll.display()

    # Search for an element
    key = 20
    pos = sll.search(key)
    if pos != -1:
        print(f"Element {key} found at position {pos}")
    else:
        print(f"Element {key} not found.")

    # Delete an element
    sll.delete_node(10)
    print("Linked List after deleting 10:")
    sll.display()

    # Try deleting a non-existent element
    sll.delete_node(100)
