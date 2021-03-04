# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:04:51 2021

@author: Charissa
"""

class Queue:
    def __init__(self, data):
        self.front = None
        self.rear = None
        self.list = data
        self.size = len(self.list)
    
    def enqueue(self, element):
        '''
        enqueue elements at the rear of the list

        Parameters
        ----------
        element : 
            element that is to be added at the rear of the queue

        '''
        if (self.front == None) and (self.rear == None):
            self.front = 0
            self.rear = 0
        else:
            if self.rear - self.front <self.size:
                self.rear +=1
            else:
                return print("Error Occured, the size of list has been exceeded, please dequeue.")
        if self.list == None:
            self.list = [element]
        else:
            self.list.append(element)

        self.size = len(self.list)
       
    def dequeue(self, num):
        '''
        dequeues the num elements depending on the specific input from the queue

        Parameters
        ----------
        num : Integer
            num denotes the number of elements that is going to be dequeued
        
        Returns
        -------
        Error message only if there is None elements in the queue

        '''
        if (self.front == None) and (self.rear == None):
            return print("Error Occurred, no element in queue to dequeue please try again.")
        else:
            self.front += num
            for x in range(num):
                self.list.pop(0)
        
        self.size = len(self.list)
    
    def pop(self):
        if (self.front == None) and (self.rear == None):
            return print("Error Occurred, no element in queue to pop please try again.")
        else:
            return self.list.pop(0)

        self.size = len(self.list)
    
    def printQueue(self):
        print(self.list)
        
newQueue = Queue(None)
newQueue.enqueue(2)
newQueue.enqueue(5)
newQueue.enqueue(15)
newQueue.enqueue(25)
newQueue.enqueue(60)
newQueue.enqueue(39)
newQueue.dequeue(3)
newQueue.enqueue(21)
newQueue.enqueue(15)
newQueue.dequeue(2)
newQueue.printQueue()
