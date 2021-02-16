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
    def inordertraversal(bst): 
        if bst != None:
            BST.inordertraversal(bst.leftchild)
            print(bst.data)
            BST.inordertraversal(bst.rightchild)
        else:
            return bst
    def minval(node):
        curr = node
        while curr.left != None:
            curr = curr.leftchild
        return curr
    def delete(bst,data):
        if bst != None:
            if data < bst.data:
                bst.leftchild = BST.delete(bst.leftchild,data)
            elif data > bst.data:
                bst.rightchild = BST.delete(bst.rightchild,data)
            else:
                if bst.leftchild == None:
                    temp = bst.rightchild
                    bst = None
                    return temp
                elif bst.rightchild == None:
                    temp = bst.leftchild
                    bst = None
                    return temp
                temp = BST.minval(bst.rightchild)
                bst.data = temp.data
                bst.rightchild = BST.delete(bst.rightchild,temp.data)
            return bst
#example that the BST works
bst1 = None
bst1 = BST.insert(bst1,40)   
bst1 = BST.insert(bst1,90)   
bst1 = BST.insert(bst1,64)  
bst1 = BST.insert(bst1,54)  
bst1 = BST.delete(bst1,64)
bst1 = BST.insert(bst1,20)   
bst1 = BST.insert(bst1,50)   
bst1 = BST.insert(bst1,35)  
bst1 = BST.insert(bst1,15)
bst1 = BST.insert(bst1,40)   
bst1 = BST.delete(bst1,35)
BST.inordertraversal(bst1)  