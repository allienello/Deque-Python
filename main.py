import gc
from typing import TypeVar, List
from random import randint, shuffle
from timeit import default_timer
# COMMENT OUT THIS LINE if you don't want matplotlib
from matplotlib import pyplot as plt

T = TypeVar('T')
CDLLNode = type('CDLLNode')

class CircularDeque:
    """
    Representation of a Circular Deque using an underlying python list
    """

    __slots__ = ['capacity', 'size', 'queue', 'front', 'back']

    def __init__(self, data: List[T] = None, front: int = 0, capacity: int = 4):
        """
        Initializes an instance of a CircularDeque
        :param data: starting data to add to the deque, for testing purposes
        :param front: where to begin the insertions, for testing purposes
        :param capacity: number of slots in the Deque
        """
        if data is None and front != 0:
            # front will get set to 0 by front_enqueue if the initial data is empty
            data = ['Start']
        elif data is None:
            data = []

        self.capacity: int = capacity
        self.size: int = len(data)
        self.queue: List[T] = [None] * capacity
        self.back: int = None if not data else self.size + front - 1
        self.front: int = front if data else None

        for index, value in enumerate(data):
            self.queue[index + front] = value

    def __str__(self) -> str:
        """
        Provides a string representation of a CircularDeque
        'F' indicates front value
        'B' indicates back value
        :return: the instance as a string
        """
        if self.size == 0:
            return "CircularDeque <empty>"

        str_list = [f"CircularDeque <"]
        for i in range(self.capacity):
            str_list.append(f"{self.queue[i]}")
            if i == self.front:
                str_list.append('(F)')
            elif i == self.back:
                str_list.append('(B)')
            if i < self.capacity - 1:
                str_list.append(',')

        str_list.append(">")
        return "".join(str_list)

    __repr__ = __str__

    # My Code Below #

    def __len__(self) -> int:
        """
        Returns the length/size of the circular deque.

        :return: int representing the length of the circular deque.

        This is a magic method and can be called with len(object_to_measure).

        Time complexity: O(1)
        Space complexity: O(1)
        """
        return self.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the circular deque is empty.

        :return: True if empty, False otherwise.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        if self.size == 0:
            return True
        return False

    def front_element(self) -> T:
        """
        Returns the first element in the circular deque.

        :return: The first element if it exists, otherwise None.

        Time complexity: O(1)
        Space Complexity: O(1)
        """
        if self.size == 0:
            return None
        else:
            return self.queue[self.front]

    def back_element(self) -> T:
        """
        Returns the last element in the circular deque.

        :return: The last element if it exists, otherwise None.

        Time complexity: O(1)
        Space complexity: O(1)
        """
        if self.size == 0:
            return None
        else:
            return self.queue[self.back]

    def grow(self) -> None:
        """
        Doubles the capacity of CD by creating a new underlying python list with double the capacity of the old one and copies the values over from the current list.
        The new copied list will be ‘unrolled’ s.t. the front element will be at index 0 and the tail element will be at index [size - 1].

        :return: None

        Time complexity: O(n)
        Space complexity: O(n)
        """
        new_cap= self.capacity * 2
        new_queue = [None] * new_cap

        if self.size > 0:
            for i in range(self.size):
                new_queue[i] = self.queue[(self.front + i) % self.capacity]

        self.capacity = new_cap  # update the capacity to double
        self.queue = new_queue
        self.front = 0
        self.back = self.size - 1

    def shrink(self) -> None:
        """
        Cuts the capacity of the queue in half using the same idea as grow. Copy over contents of the old list to a new list with half the capacity.
        The new copied list will be ‘unrolled’ s.t. the front element will be at index 0 and the tail element will be at index [size - 1].
        Will never have a capacity lower than 4, DO NOT shrink when shrinking would result in a capacity < 4.

        :return: None

        Time complexity: O(n)
        Space complexity: O(n)
        """
        new_cap = max(4, self.capacity // 2)  # ensure capacity doesn't go below 4
        new_queue = [None] * new_cap

        for i in range(self.size):
            new_queue[i] = self.queue[(self.front + i) % self.capacity]

        self.capacity = new_cap
        self.queue = new_queue
        self.front = 0
        self.back = self.size - 1

    def enqueue(self, value: T, front: bool = True) -> None:
        """
        Add a value to either the front or back of the circular deque based off the parameter front.
        If front is true, add the value to the front. Otherwise, add it to the back.
        Call grow() if the size of the list has reached capacity.

        :param value: T: Value to add into the circular deque.
        :param front: Where to add value T.

        :return: None

        Time complexity: O(1)*
        Space complexity: O(1)*
        """
        if self.front is None:
            self.front = 0
            self.back = 0
            index = 0
        else:
            if front:
                index = (self.front - 1) % self.capacity
                self.front = index
            else:
                index = (self.back + 1) % self.capacity
                self.back = index

        # set the value at the calculated index, update size
        self.queue[index] = value
        self.size += 1

        # grow the queue if it's full after adding an element
        if self.size == self.capacity:
            self.grow()

    def dequeue(self, front: bool = True) -> T:
        """
        Remove an item from the queue.
        Removes the front item by default, remove the back item if False is passed in.
        Calls shrink() If the current size is less than or equal to 1/4 the current capacity, and 1/2 the current capacity is greater than or equal to 4, halves the capacity.
        Hint: You shouldn’t delete the value from the dequeue (by setting it to None) as that spot will merely be overwritten when you enqueue on that spot so it’s more efficient to only adjust the back/front pointer instead.

        :param front: Whether to remove the front or back item from the dequeue.

        :return: Removed item, None if empty

        Time complexity: O(1)*
        Space complexity: O(1)*
        """
        if self.size == 0:
            return None

        if front:
            value = self.queue[self.front]
            self.front = (self.front + 1) % self.capacity
        else:
            value = self.queue[self.back]
            self.back = (self.back - 1) % self.capacity

        self.size -= 1

        if (self.size <= (self.capacity // 4)) and ((self.capacity // 2) >= 4):
            self.shrink()

        return value


class CDLLNode:
    """
    Node for the CDLL
    """

    __slots__ = ['val', 'next', 'prev']

    def __init__(self, val: T, next: CDLLNode = None, prev: CDLLNode = None) -> None:
        """
        Creates a CDLL node
        :param val: value stored by the next
        :param next: the next node in the list
        :param prev: the previous node in the list
        :return: None
        """
        self.val = val
        self.next = next
        self.prev = prev

    def __eq__(self, other: CDLLNode) -> bool:
        """
        Compares two CDLLNodes by value
        :param other: The other node
        :return: true if comparison is true, else false
        """
        return self.val == other.val

    def __str__(self) -> str:
        """
        Returns a string representation of the node
        :return: string
        """
        return "<= (" + str(self.val) + ") =>"

    __repr__ = __str__


class CDLL:
    """
    A (C)ircular (D)oubly (L)inked (L)ist
    """

    __slots__ = ['head', 'size']

    def __init__(self) -> None:
        """
        Creates a CDLL
        :return: None
        """
        self.size = 0
        self.head = None

    def __len__(self) -> int:
        """
        :return: the size of the CDLL
        """
        return self.size

    def __eq__(self, other: 'CDLL') -> bool:
        """
        Compares two CDLLs by value
        :param other: the other CDLL
        :return: true if comparison is true, else false
        """
        n1: CDLLNode = self.head
        n2: CDLLNode = other.head
        for _ in range(self.size):
            if n1 != n2:
                return False
            n1, n2 = n1.next, n2.next
        return True

    def __str__(self) -> str:
        """
        :return: a string representation of the CDLL
        """
        n1: CDLLNode = self.head
        joinable: List[str] = []
        while n1 is not self.head:
            joinable.append(str(n1))
            n1 = n1.next
        return ''.join(joinable)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#

    def insert(self, val: T, front: bool = True) -> None:
        """
        Inserts a node with value val in the front or back of the CDLL.
        Don’t forget to keep it circular!!

        :param val: T: The value to insert.
        :param front: bool = True: Whether to insert in the front of the list, or the back.

        :return: None

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        new_node = CDLLNode(val)

        if self.head is None:
            # if list is empty, new node is the only node,
            # so points to itself in both directions
            new_node.next = new_node
            new_node.prev = new_node
            self.head = new_node
        else:
            if front:
                # Insert at the front of the list.
                new_node.next = self.head
                new_node.prev = self.head.prev
                self.head.prev.next = new_node
                self.head.prev = new_node
                self.head = new_node
            else:
                # insert at the back of the list
                new_node.next = self.head
                new_node.prev = self.head.prev
                self.head.prev.next = new_node
                self.head.prev = new_node

        self.size += 1

    def remove(self, front: bool = True) -> None:
        """
        Removes a node from the CDLL.
        Don’t forget to keep it circular!!
        If the list is empty, do nothing.

        :param front: bool = True: Whether to remove from the front of the list, or the back.

        :return: None

        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        if self.size == 0:
            return

        if self.size == 1:
            self.head = None
        else:
            if front:
                # remove from the front of the list
                self.head.prev.next = self.head.next
                self.head.next.prev = self.head.prev
                self.head = self.head.next
            else:
                # remove from the back of the list
                self.head.prev.prev.next = self.head
                self.head.prev = self.head.prev.prev

        self.size -= 1


class CDLLCD:
    """
    (C)ircular (D)oubly (L)inked (L)ist (C)ircular (D)equeue
    This is essentially just an interface for the above
    """

    def __init__(self) -> None:
        """
        Initializes the CDLLCD to an empty CDLL
        :return: None
        """
        self.CDLL: CDLL = CDLL()

    def __eq__(self, other: 'CDLLCD') -> bool:
        """
        Compares two CDLLCDs by value
        :param other: the other CDLLCD
        :return: true if equal, else false
        """
        return self.CDLL == other.CDLL

    def __str__(self) -> str:
        """
        :return: string representation of the CDLLCD
        """
        return str(self.CDLL)

    __repr__ = __str__

    # ============ Modifiy Functions Below ============#
    def __len__(self) -> int:
        """
        Returns the length/size of the CDLLCD, and hence the underlying CDLL.
        This is a magic method and can be called with len(object_to_measure).

        Time complexity: O(1)
        Space complexity: O(1)

        Returns:
            int representing the length of the CDLLCD
        """
        return self.CDLL.size

    def is_empty(self) -> bool:
        """
        Returns a boolean indicating if the CDLLCD is empty.

        Time complexity: O(1)
        Space complexity: O(1)

        Returns:
            True if empty, False otherwise
        """
        return self.CDLL.size == 0

    def front_element(self) -> T:
        """
        Returns the first element in the CDLLCD.

        Time complexity: O(1)
        Space Complexity: O(1)

        Returns:
            The first element if it exists, otherwise None
        """
        return self.CDLL.head.val if self.CDLL.head else None

    def back_element(self) -> T:
        """
        Returns the last element in the CDLLCD.

        Time complexity: O(1)
        Space complexity: O(1)

        Returns:
            The last element if it exists, otherwise None
        """
        return self.CDLL.head.prev.val if self.CDLL.head else None

    def enqueue(self, val: T, front: bool = True) -> None:
        """
        Adds a value to the CDLLCD.
        Must use the insert function of the CDLL class.

        :param val: T: The value to be added.
        :param front: bool = True: Whether to add to the front or the back of the deque.

        :return: None

        Time complexity: O(1)
        Space complexity: O(1)
        """
        self.CDLL.insert(val, front)

    def dequeue(self, front: bool = True) -> T:
        """
        Removes a value from the deque, returning it.
        Must use the remove function of the CDLL class.

        :param front: bool = True: Whether to remove from the front or the back of the deque.

        :return: The dequeued element, None if empty

        Time complexity: O(1)
        Space complexity: O(1)
        """
        if self.CDLL.size == 0:
            return None

        node_to_remove = self.CDLL.head if front else self.CDLL.head.prev
        value = node_to_remove.val

        # use the remove method of CDLL class
        self.CDLL.remove(front)

        return value

