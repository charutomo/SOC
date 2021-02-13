# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 18:10:14 2021

@author: Charissa
"""

#Binary Search Tree 
class Node:
    def __init__(self,data):
        self.data = data
        self.leftchild = None 
        self.rightchild = None
    
class BST:
    def insert(bst,data):
        if bst == None:
            return Node(data)
        else:
            if bst.data == data:
                return bst
            elif bst.data < data:
                bst.rightchild = BST.insert(bst.rightchild,data)
            else:
                bst.leftchild = BST.insert(bst.leftchild,data)
        return bst
    def inordertraversal(bst): #I decided to use inorder traversal for bst
        if bst != None:
            BST.inordertraversal(bst.leftchild)
            print(bst.data)
            BST.inordertraversal(bst.rightchild)

#example that the BST works
bst1 = Node(20)
bst1 = BST.insert(bst1,40)   
bst1 = BST.insert(bst1,90)   
bst1 = BST.insert(bst1,64)  
bst1 = BST.insert(bst1,54)  
BST.inordertraversal(bst1)  