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
    '''
    generates inorder traversal of binary search tree

    Parameters
    ----------
    root : Nodes
        Nodes of binary search tree

    Returns
    -------
    root : Node
       return inorder traversal of binary search tree

    '''
    if root != None:
        inordertraversal(root.leftchild)
        print(root.data)
        inordertraversal(root.rightchild)
    else:
        return root
def minval(node):
    '''
    Find the current reference to node of minimum value 

    Parameters
    ----------
    node : Node
        

    Returns
    -------
    curr : reference
        current reference to node of minimum value 

    '''
    curr = node
    while curr.leftchild != None:
        curr = curr.leftchild
    return curr

def search(root,key):
    '''
    binary search for an element

    Parameters
    ----------
    root : Nodes of BST
        
    key : Integer
        intgere to be found in BST 

    Returns
    -------
    key :Integer
        returns key if found

    '''
    if root.data == None or root.data == key:
        return root.data
    if root.data < key:
        return search(root.rightchild,key)
    else:
        return search(root.leftchild,key)

def delete(root,node):
    '''
    delete an element form BST

    Parameters
    ----------
    root : Nodes of bst
    
    node : Node 
        Node for which to be deleted

    Returns
    -------
    root
        BST excluding deleted element

    '''
    if root.data != None:
        if root.data > node.data:
            root.leftchild = delete(root.leftchild,node)
        elif root.data < node.data:
            root.rightchild = delete(root.rightchild,node)
        else:
            if root.leftchild == None:
                temp = root.rightchild
                root.data = None
                return temp
            elif root.rightchild == None:
                temp = root.leftchild
                root.node = None
                return temp
            temp = minval(root.rightchild)
            root.rightchild = delete(root.rightchild,temp.data)
        return root

bst1 = Node(20)
bst1 = insert(bst1,Node(40))   
bst1 = insert(bst1,Node(90)) 
bst1 = insert(bst1,Node(78))
bst1 = insert(bst1,Node(1))
bst1 = delete(bst1,Node(90))
bst1 = insert(bst1,Node(23))
bst1 = insert(bst1,Node(85))
bst1 = insert(bst1,Node(123)) 
print(search(bst1,23))
inordertraversal(bst1)  
 