# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:04:51 2021

@author: Charissa
"""

'''
==================================
Queue
==================================
'''

class QNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def enqueue(self, data):
        '''
        enqueue elements at the rear of the list

        Parameters
        ----------
        element : 
            element that is to be added at the rear of the queue

        '''
        newNode = QNode(data)  
        if self.front == None and self.rear == None:
            self.front=newNode 
            self.rear=newNode 
        else:
            self.rear.next = newNode 
            self.rear = newNode 
        self.size += 1
       
    def dequeue(self):
        '''
        dequeues the front element 


        Returns
        -------
        Error message only if there is None elements in the queue
        
        data: 
            data that was removed

        '''
        if (self.front == None) and (self.rear == None):
            return print("Error Occurred, no element in queue to dequeue please try again.")
        else:
            data = self.front.data 
            self.front = self.front.next
            if self.front == None:
                self.rear = None 
            self.size -= 1 
            return data 
        
    def printQueue(self):
        queuelist = []
        curr = self.front
        while curr:
            queuelist.append(curr.data) 
            curr = curr.next 
        print(queuelist) 

'''
================================================
Binary Search Tree
================================================
'''

class BSTNode:
    def __init__(self,data):
        self.data = data
        self.leftchild = None 
        self.rightchild = None

class BinarySearchTree:
    def __init__(self): 
        self.root = None  
        self.size = 0

    def insert(self, data):
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
        newNode = BSTNode(data)
        if self.root == None:
            self.root = newNode
            self.size +=1
            return 
        else:
            curr = self.root
            while curr:
                if newNode.data == curr.data:
                    return 
                elif newNode.data > curr.data:
                    if curr.rightchild != None: 
                        curr = curr.rightchild
                    else:
                        curr.rightchild = newNode
                else:
                    if curr.leftchild != None: 
                        curr = curr.leftchild
                    else:
                        curr.leftchild = newNode 
            self.size+=1
            return 
    
    def inordertraversal(self,root): 
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
            self.inordertraversal(root.leftchild)
            print(root.data)
            self.inordertraversal(root.rightchild)
        else:
            return self.root
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
    
    def search(self,key):
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
        if self.root.data == None or self.root.data == key:
            return self.root.data
        if self.root.data < key:
            return self.search(self.root.rightchild,key)
        else:
            return self.search(self.root.leftchild,key)
    
    def delete(self,root,node):
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
        if self.root.data != None:
            if self.root.data > node:
                self.root.leftchild = self.delete(self.root.leftchild,node)
            elif self.root.data < node:
                self.root.rightchild = self.delete(self.root.rightchild,node)
            else:
                if self.root.leftchild == None:
                    temp = self.root.rightchild
                    self.root.data = None
                    return temp
                elif self.root.rightchild == None:
                    temp = self.root.leftchild
                    self.root.node = None
                    return temp
                temp = self.minval(self.root.rightchild)
                self.root.rightchild = self.delete(self.root.rightchild,temp.data)
            return self.root
        
    def levelorderTraversal(self): 
        '''
        generates level order traversal of binary search tree

        Returns
        -------
        result : 
            generates level order traversal of binary search tree

        '''
        result = [] 
        myqueue = Queue() 
        curr = self.root
        if curr != None: 
            myqueue.enqueue(curr)  
        while myqueue.front:  
            curr = myqueue.dequeue()  
            result.append(curr.data) 
            if curr.leftchild != None:
                myqueue.enqueue(curr.leftchild)
            if curr.rightchild != None:
                myqueue.enqueue(curr.rightchild)  
        return result

BST = BinarySearchTree()
for i in range(10):
    BST.insert(2*i)
print(BST.levelorderTraversal())
print()
print(BST.inordertraversal(BST.root))
