# Compilação baseada no código de
#- https://medium.com/@aksh0001/avl-trees-in-python-bc3d0aeb9150

from typing import List


# ------------------------------------------------------------------------------------------
# Base Tree Node
class TreeNode:
    def __init__(self, key, val=None):
        self.key = key
        self.val = val
        self.left = None
        self.right = None

        
# ------------------------------------------------------------------------------------------
# Base BST Class
class BST:
    def __init__(self):
        self.root = None
        self.n = 0

    def insert(self, key, val=None):
        node = TreeNode(key, val)
        if self.root is None:
            self.root = node
        else:
            self._insert(self.root, node)
        self.n += 1

    def _insert(self, root: TreeNode, node: TreeNode):
        """
        Recursively inserts the passed in node into the BST.
        Clever Algorithm: First ascertain direction (l or r) to recur.
            Before recurring, check if we can insert directly in the ascertained direction by checking the child
            If a child in that direction does not exist, simply assign it there
            Else, recur in that direction
        :param root: root of bst
        :param node: node to insert
        :Time: O(log(n))
        :Space: O(log(n)) stack space
        :return: none
        """
        if root is None:
            return  # Could simply return/"rebound" the node parameter up the stack and assign where needed, or return

        if node.key < root.key:  # First check to determine direction: left
            if root.left is None:  # Second check to check if a left child doesn't exist
                root.left = node  # If it doesn't simply assign
            else:
                self._insert(root.left, node)  # Else, simply recur left

        elif node.key > root.key:  # Similar for the right subtree
            if root.right is None:
                root.right = node
            else:
                self._insert(root.right, node)

    def get(self, key) -> TreeNode:
        ret_val = self._get(self.root, key)
        if ret_val is None:
            raise LookupError("Error! Key doesn't exist!")
        else:
            return ret_val

    def _get(self, root: TreeNode, key: TreeNode) -> TreeNode:
        """
        Helper get method that to get the node associated with key
        :param root: root of tree
        :param key: key to look for
        :return: None if not found, the node, otherwise
        :Time: O(log(N))
        :Space: O(log(N))
        """
        # Always do the edge-case check, which could raise an error, FIRST!!
        if root is None:  # BC2 - not found
            return None
        # BST-order traverse: examine root first, then recur left or recur right depending on key comparison
        if root.key == key:  # BC1 - found
            return root

        result_left_subtree = None
        result_right_subtree = None

        if key < root.key:
            result_left_subtree = self._get(root.left, key)
        elif key > root.key:
            result_right_subtree = self._get(root.right, key)

        if result_left_subtree is not None:
            return result_left_subtree
        elif result_right_subtree is not None:
            return result_right_subtree
        else:
            return None


    def get_height(self) -> int:
        return self._get_height(self.root)

    def _get_height(self, root) -> int:
        """
        Returns the height of the binary tree.
        Algorithm: max(recur left, recur right) + 1
        Explanation: The height of a binary tree that is rooted at a certain node is equal to the
        maximum of the heights of its left and right subtrees + 1 (take into account the root node)
        :param root: root of the tree
        :return: the height of the tree
        """
        # BC
        if root is None:
            return 0
        # Take the maximum of the height of the left subtree and the right subtree, and add 1 to the result
        height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        return height

    def get_max(self):
        """
        This returns the maximum key in the BST
        Algorithm: If root is none, no solution. Else, traverse the right subtree like a linked list
        and return the right-most node
        :Time: O(N)
        :Space: O(1)
        :return: the maximum key in the tree
        """
        if self.root is None:  # BC1
            return float('-inf')

        current = self.root
        while current.right is not None:  # Traverse like a linked-list
            current = current.right

        return current.key

    def get_min(self):
        """
        This returns the minimum key in the BST
        Algorithm: If root is none, no solution. Else, traverse the left subtree like a linked list
        and return the left-most node
        :Time: O(N)
        :Space: O(1)
        :return: the minimum key in the tree
        """
        if self.root is None:  # BC1
            return float('+inf')

        current = self.root
        while current.left is not None:  # Traverse like a linked-list
            current = current.left

        return current.key


    def delete(self, key) -> TreeNode:
        def delete_helper(root: TreeNode, key) -> TreeNode:
            """
            Deletes a node associated with key, key, in the tree and returns the root of the resulting
            tree, which may be updated.
            :param root: root of tree
            :param key: key to be deleted
            :Time: O(log(n)) average
            :Space: O(log(n) average
            :return: the resulting root of the tree
            """
            if root is None:
                return None
            if key < root.key:
                new_root_left = delete_helper(root.left, key)  # get new root of left subtree
                root.left = new_root_left  # assign root.left to the new root of the left subtree
            elif key > root.key:
                new_root_right = delete_helper(root.right, key)
                root.right = new_root_right
            else:  # found match, handle 3 cases
                # case 1 - match is a leaf node (return None back up the stack)
                if root.left is None and root.right is None:
                    return None  # root of new subtree is None
                # case 2 - match has one child (return the other back up the stack)
                elif root.left is None:
                    return root.right  # return the right subtree back up the stack to indicate that its the new root
                elif root.right is None:  # vice-versa
                    return root.left
                # case 3 - replace match with inorder successor; delete the successor; return up the stack
                else:
                    inorder_successor = self.get_min_node(root.right)
                    root.key, root.val = inorder_successor.key, inorder_successor.val  # copy  successor into current
                    new_root_successor = delete_helper(root.right, inorder_successor.key)  # delete inorder successor
                    root.right = new_root_successor
                    return root

            return root  # return root of resulting tree as required

        return delete_helper(self.root, key)


# ------------------------------------------------------------------------------------------
# AVL Tree Node
class AVLTreeNode(TreeNode):
    def __init__(self, key, val=None, bf=0):
        super().__init__(key, val)
        self.key = key
        self.val = val
        self.left = None
        self.right = None
        self.parent = None  # Also track parent of this node for easier rotations
        self.bf = bf  # Balance factor of current node
        self.height = 1  # Height of tree rooted at this node (this is important to update bf's after re-balancing)
        

# ------------------------------------------------------------------------------------------
# AVL Tree Class
class AVLTree(BST):
    def __init__(self):
        super().__init__()

    def insert(self, key, val=None):
        """
        Public insert function to insert a node into an AVL Tree.
        :param key: key of node to be inserted
        :param val: corresponding value
        :Time: O(log(n))
        :Space: O(log(n))
        :return: none
        """
        self.root = self._insert(self.root, key, val)  # Returns root of resulting tree after insertion - update it
        self.n += 1

    def _insert(self, root: AVLTreeNode, key, val=None) -> AVLTreeNode:
        """
        Given an AVLTreeNode, inserts the node in the tree rooted at "root", updates heights and balance
        factors of affected nodes in the tree, and updates parent pointers; finally, returns root of resulting tree.
        :param root: root of AVL tree
        :param key: key of node to be inserted
        :param val: value of node to be inserted
        :Time: O(log(n))
        :Space: O(log(n)) stack space proportional to height
        :return: root of resulting tree after insertion
        """
        if not root:
            return AVLTreeNode(key, val, bf=0)  # If empty root this is the root of new tree
        if key < root.key:
            left_sub_root = self._insert(root.left, key, val)  # insert and update left subroot
            root.left = left_sub_root
            left_sub_root.parent = root  # assign the parent
        elif key > root.key:
            right_sub_root = self._insert(root.right, key, val)  # insert and update right subroot
            root.right = right_sub_root
            right_sub_root.parent = root
        else:
            return root  # no duplicate keys allowed; no insertion, return current root as is
        # finally, update heights and bf's of current root after insertion completed (postorder processing)
        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        return self.rebalance(root)  # RE-BALANCE CURRENT ROOT (if required)

    def rebalance(self, root: AVLTreeNode) -> AVLTreeNode:
        """
        Main rebalance routine to rebalance the tree rooted at root appropriately using rotations.
        4 cases:
        1) bf(root) = 2 and bf(root.left) < 0 ==> L-R Imbalance
        2) bf(root) = 2 ==> L-L Imbalance
        3) bf(root) = -2 and bf(root.right) > 0 ==> R-L Imbalance
        4) bf(root) = -2 ==> R-R Imbalance
        :param root: root of tree needing rebalancing.
        :return: root of resulting tree after rotations
        """
        if root.bf == 2:
            if root.left.bf < 0:  # L-R
                root.left = self.rotate_left(root.left)
                return self.rotate_right(root)
            else:  # L-L
                return self.rotate_right(root)
        elif root.bf == -2:
            if root.right.bf > 0:  # R-L
                root.right = self.rotate_right(root.right)
                return self.rotate_left(root)
            else:  # R-R
                return self.rotate_left(root)
        else:
            return root  # no need to rebalance

    def rotate_right(self, root: AVLTreeNode) -> AVLTreeNode:
        """
        Performs a right rotation on the tree rooted at root, and returns root of resulting tree
        :param root: root of tree
        :Time: O(1)
        :Space: O(1)
        :return: root of updated tree
        """
        pivot = root.left  # set up pointers
        tmp = pivot.right
        # 1st Move: reassign pivot's right child to root and update parent pointers
        pivot.right = root
        pivot.parent = root.parent  # pivot's parent now root's parent
        root.parent = pivot  # root's parent now pivot
        # 2nd Move: use saved right child of pivot and assign it to root's left and update its parent
        root.left = tmp
        if tmp:  # tmp can be null
            tmp.parent = root

        # Not done yet - need to update pivot's parent (manually check which one matches the root that was passed)
        if pivot.parent:
            if pivot.parent.left == root:  # if the parent's left subtree is the one to be updated
                pivot.parent.left = pivot  # assign the pivot as the new child
            else:
                pivot.parent.right = pivot  # vice-versa for right child

        # Still not done :) -- update heights and bf's using tracked heights
        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.bf = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot  # return root of new tree

    def rotate_left(self, root: AVLTreeNode) -> AVLTreeNode:
        """
        Performs a left rotation on the tree rooted at root, and returns root of resulting tree.
        :param root: root of tree
        :Time: O(1)
        :Space: O(1)
        :return: root of updated tree.
        """
        pivot = root.right
        tmp = pivot.left

        pivot.left = root
        pivot.parent = root.parent
        root.parent = pivot

        root.right = tmp
        if tmp:  # tmp can be null
            tmp.parent = root

        # Not done -- need to update pivot's parent as well
        if pivot.parent:
            if pivot.parent.left == root:  # if the parent's left subtree is the one to be updated
                pivot.parent.left = pivot  # assign the pivot as the new child
            else:
                pivot.parent.right = pivot  # vice-versa for right child
        # Still not done :) -- update heights and bf's using tracked heights
        root.height = max(self._get_height(root.left), self._get_height(root.right)) + 1
        root.bf = self._get_height(root.left) - self._get_height(root.right)
        pivot.height = max(self._get_height(pivot.left), self._get_height(pivot.right)) + 1
        pivot.bf = self._get_height(pivot.left) - self._get_height(pivot.right)
        return pivot  # return root of new tree

    def _get_height(self, root: AVLTreeNode) -> int:
        """
        Overridden to account for the fact that we are tracking heights during tree construction.
        :param root: root of subtree of which to get height for
        :return: height of tree rooted at root
        """
        if not root:  # empty tree means height of 0
            return 0
        else:
            return root.height  # return instance var height

    @staticmethod
    def burst_insert(a: List):
        """
        Inserts a list of n items into an AVL Tree and returns the root.
        :param a: list of items
        :Time: O(N*log(N))
        :Space: O(N)
        :return: tree root
        """
        root = AVLTree()
        for item in a:
            root.insert(item)
        return root
