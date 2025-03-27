## Bibliotecas
from __future__ import annotations
from abc import ABC, abstractmethod

class Node:
    def __init__(self, key: object, value: object):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

        def __str__(self) -> str:
            return str(self.key)
        
        def next(self, other_key: object) -> Node:
            return self.left if other_key < self.key else self.right
        
class BinarySearchTreeADT(ABC):
    @abstractmethod
    def clear(self) -> None: ...
    @abstractmethod
    def is_empty(self) -> bool: ...
    @abstractmethod
    def search(self, key: object) -> object: ...
    @abstractmethod
    def insert(self, key: object, value: object) -> None: ...
    @abstractmethod
    def delete(self, key: object) -> bool: ...
    @abstractmethod
    def pre_order_traversal(self) -> None: ...
    @abstractmethod
    def in_order_traversal(self) -> None: ...
    @abstractmethod
    def post_order_traversal(self) -> None: ...
    @abstractmethod
    def level_order_traversal(self) -> None: ...
  
    # Métodos para desenvolver
    @abstractmethod
    def count_internal(self) -> int: ...
    @abstractmethod
    def degree(self, key: object) -> int: ...
    @abstractmethod
    def height(self, key: object) -> int: ...
    @abstractmethod
    def level(self, key: object) -> int: ...
    @abstractmethod
    def descendent(self, key: object) -> str: ...

class BinarySearchTree(BinarySearchTreeADT):
    def __init__(self) -> None:
        self.root = None
        self.aux_list = []

    def clear(self) -> None:
        self.root = None
        
    def is_empty(self) -> bool:
        return self.root is None
    
    def _get_parent(self, key: object) -> Node:
        parent: Node = None
        current: Node = self.root
        while current and key != current.key:
            parent = current
            current = current.next(key)

        return parent, current
    
    def search(self, key: object) -> object:
        def search(current: Node, key: object) -> object:
            if current is None:
                return None
            elif key == current.key:
                return current.value
            return search(current.next(key), key)
        
        return search(self._root, key)
    
    def insert(self, key: object, value: object) -> None:
        def insert(current: Node, key: object, value: object) -> Node:
            if current is None:
                return Node(key, value)
            elif key > current.key:
                current.right = insert(current.right, key, value)
            elif key < current.key:
                current.left = insert(current.left, key, value)
            return current
        
        self._root = insert(self._root, key, value)

    def __str__(self) -> str:
        return '[empty]' if self.is_empty() else self._str_tree()

    def _str_tree(self) -> str:
        def _str_tree(current: Node, is_right: bool, tree: str, ident: str) -> str:
            if current.right:
                tree = _str_tree(current.right, True, tree, ident + (' ' * 8 if is_right else ' |' + ' ' * 6))
            tree += ident + (' /' if is_right else ' \\') + "----- " + str(current) + '\n'
            if current.left:
                tree = _str_tree(current.left, False, tree, ident + (' |' + ' ' * 6 if is_right else ' ' * 8))
            return tree

        tree: str = ''
        if self._root.right:
            tree = _str_tree(self._root.right, True, tree, '')
        tree += str(self._root) + '\n'
        if self._root.left:
            tree = _str_tree(self._root.left, False, tree, '')
        return tree

    def _delete_by_copying(self, key: object) -> bool:
        parent: Node
        current: Node
        parent, current = self._get_parent(key)

        if current is None:
            return False

        # Case 3: O nó tem dois filhos
        elif current.left and current.right:
            at_the_right: Node = current.left
            while at_the_right.right:
                at_the_right = at_the_right.right
            self._delete_by_copying(at_the_right.key)
            current.key, current.value = at_the_right.key, at_the_right.value

        # Case 1/2: O nó tem um ou nenhum filho
        else:
            next_node: Node = current.left or current.right
            if current == self._root:
                self._root = next_node
            elif current == parent.left:
                parent.left = next_node
            else:
                parent.right = next_node

        return True
    
    def delete(self, key: object) -> bool:
        return self._delete_by_copying(key)

    def _delete_by_merging(self, key: object) -> bool:
        parent: Node
        current: Node
        parent, current = self._get_parent(key)

        if current is None:
            return False

        # Case 3: O nó tem dois filhos
        elif current.left and current.right:
            at_the_right: Node = current.left
            while at_the_right.right:
                at_the_right = at_the_right.right
            at_the_right.right = current.right

            if current == self._root:
                self._root = current.left
            elif parent.left == current:
                parent.left = current.left
            else:
                parent.right = current.left

        # Case 1/2: O nó tem um ou nenhum filho
        else:
            next_node: Node = current.left or current.right
            if current == self._root:
                self._root = next_node
            elif current == parent.left:
                parent.left = next_node
            else:
                parent.right = next_node

        return True

    def delete(self, key: object) -> bool:
        return self._delete_by_merging(key)

    def pre_order_traversal(self) -> None:
        def pre_order_traversal(current: Node) -> None:
            if current:
                print(current.key, end=' ')
                pre_order_traversal(current.left)
                pre_order_traversal(current.right)
        pre_order_traversal(self._root)

    def in_order_traversal(self) -> None:
        def in_order_traversal(current: Node) -> None:
            if current:
                in_order_traversal(current.left)
                print(current.key, end=' ')
                in_order_traversal(current.right)
        in_order_traversal(self._root)

    def post_order_traversal(self) -> None:
        def post_order_traversal(current: Node) -> None:
            if current:
                post_order_traversal(current.left)
                post_order_traversal(current.right)
                print(current.key, end=' ')
        post_order_traversal(self._root)

    def level_order_traversal(self) -> None:
        if self._root:
            queue = [self._root]
            while queue:
                current: Node = queue.pop(0)
                print(current.key, end=' ')
                if current.left: queue.append(current.left)
                if current.right: queue.append(current.right)

    def count_internal(self) -> int:
        def count_internal(current: Node) -> int:
            if current is None:
                return 0
            if current.left or current.right:
                return 1 + count_internal(current.left) + count_internal(current.right)
            return 0
        
        return count_internal(self._root)
    