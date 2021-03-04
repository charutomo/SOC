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
    def __init__(self,data):
            self.head = None
            self.size = 0

    def insert(self,data):
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
        if self.head is None:
            self.head = data
        else:
            if self.head.data == data.data:
                pass
            elif self.head < data:
                self.node.rightchild = BST.insert(self.node.rightchild,data)
            else:
                self.node.leftchild = BST.insert(self.node.leftchild,data)
        return self.node
    
    def inordertraversal(self): 
        if self != None:
            BST.inordertraversal(self.node.leftchild)
            print(self.node)
            BST.inordertraversal(self.node.rightchild)
        else:
            return self.node
        
    def minval(node):
        curr = node
        while curr.left != None:
            curr = curr.leftchild
        return curr
    
    def delete(self,data):
        if self != None:
            if data < self.data:
                self.node.leftchild = BST.delete(self.node.leftchild,data)
            elif data > self.data:
                self.node.rightchild = BST.delete(self.node.rightchild,data)
            else:
                if self.node.leftchild == None:
                    temp = self.node.rightchild
                    self.data = None
                    return temp
                elif self.node.rightchild == None:
                    temp = self.node.leftchild
                    self.node = None
                    return temp
                temp = self.minval(self.node.rightchild)
                self.node = self.node
                self.node.rightchild = self.delete(self.node.rightchild,temp.data)
            return self.node
    def search(self,key):
        if self.head == None or self.node == key:
            return self.head
        if self.data < key:
            return BST.search(self.node.rightchild,key)
        else:
            return BST.search(self.node.leftchild,key)


bst1 = Node(None)
bst1 = BST.insert(bst1,40)   
bst1 = BST.insert(bst1,90)  
bst1 = BST.insert(bst1,64)     
BST.inordertraversal(bst1)  