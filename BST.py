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
        self.head = None
       
    
class BST: 
    def __init__(self):
         self.head = None

    def insert(self,data):
        if self == None:
            self.head = Node(data)
            return self.head
        else:
            if self.data == data:
                return self.data
            elif self.data < data:
                self.rightchild = BST.insert(self.rightchild,data)
            else:
                self.leftchild = BST.insert(self.leftchild,data)
            return self.data
    
    def inordertraversal(self): 
        if self != None:
            BST.inordertraversal(self.leftchild)
            print(self.data)
            BST.inordertraversal(self.rightchild)
        else:
            return self.data
        
    def minval(node):
        curr = node
        while curr.left != None:
            curr = curr.leftchild
        return curr
    
    def delete(self,data):
        if self != None:
            if data < self.data:
                self.leftchild = BST.delete(self.leftchild,data)
            elif data > self.data:
                self.rightchild = BST.delete(self.rightchild,data)
            else:
                if self.leftchild == None:
                    temp = self.rightchild
                    self.data = None
                    return temp
                elif self.rightchild == None:
                    temp = self.leftchild
                    self.data = None
                    return temp
                temp = self.minval(self.rightchild)
                self.data = self.data
                self.rightchild = self.delete(self.rightchild,temp.data)
            return self.data
    def search(self,key):
        if self.head == None or self.data == key:
            return self.head
 
        if self.data < key:
            return BST.search(self.head.rightchild,key)
        else:
            return BST.search(self.head.leftchild,key)
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