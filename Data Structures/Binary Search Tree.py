# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 18:00:59 2021

@author: Charissa
"""

class Node:
    def __init__(self,data):
        self.data = data
        self.leftchild = None 
        self.rightchild = None

def insert(root,node):
    '''
        Parameters
        ----------
        data : float
            the float to be added to the binary search tree

        Returns
        -------
        self.data: bst
            returns the updated bst

        '''
    if root == None:
        root = node
    else:
        if root.data > node.data:
            if root.leftchild == None:
                root.leftchild = node
            else:
                insert(root.leftchild, node)
        else:
            if root.rightchild == None:
                root.rightchild = node
            else:
                insert(root.rightchild, node)
    return root

def inordertraversal(root): 
        if root != None:
            inordertraversal(root.leftchild)
            print(root.data)
            inordertraversal(root.rightchild)
        else:
            return root
def minval(node):
    curr = node
    while curr.leftchild != None:
        curr = curr.leftchild
    return curr

bst1 = Node(20)
bst1 = insert(bst1,Node(40))   
bst1 = insert(bst1,Node(90)) 
bst1 = insert(bst1,Node(78))
bst1 = insert(bst1,Node(1))
bst1 = insert(bst1,Node(23))
bst1 = insert(bst1,Node(85))
bst1 = insert(bst1,Node(123)) 
inordertraversal(bst1)  
 