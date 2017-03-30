# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 21:22:03 2017

@author: Megamindo_0
"""

__author__ = 'Peeyush Yadav'

import copy

# Where 0 denotes the blank tile or space.
initial_state = [3,1,2, 
                 6,4,5, 
                 7,8,0]
goal_state = [0,1,2,
              3,4,5,
              6,7,8]

def checkSolvability(initial_state):
    inversion = 0;
    for i in range(0,len(initial_state)-1):
        for j in range(i+1,len(initial_state)):
            if initial_state[i] != 0 and initial_state[j] != 0 and initial_state[i] > initial_state[j] :
                inversion += 1    

    if inversion % 2 == 0 :
        return True
    else:
        return False

def DFS_Search(initial_state, goal_state) :
    explored_states = []
    stack = Stack()
    stack.push(initial_state)
    
    while stack.isEmpty() == False :
        current_state = stack.pop()
        #print("Inside Stack", current_state.config)
        if current_state.config == goal_state:
            printPathtoGoal(current_state)
            return True;
              
        neighbour_states = explore_next_states(current_state, explored_states)
        for states in neighbour_states:
            stack.push(states)
        if len(explored_states) > 3 :
            print(len(explored_states))
        
        explored_states.append(current_state.config)
            
    return False
    
def explore_next_states(current_state, explored_states):
    
    new_states = []

    if(current_state.config not in explored_states):  
        
        new_state = move('down', current_state)
        if new_state[0] == True and new_state[1].config not in explored_states:
            new_states.append(new_state[1])
            new_state[1].parent = current_state
    
        new_state = move('right', current_state)
        if new_state[0] == True and new_state[1].config not in explored_states:
            new_states.append(new_state[1])
            new_state[1].parent = current_state
             
        new_state = move('up', current_state)
        if new_state[0] == True and new_state[1].config not in explored_states:
            new_states.append(new_state[1])
            new_state[1].parent = current_state
            
        new_state = move('left', current_state)    
        if new_state[0] == True and new_state[1].config not in explored_states:
            new_states.append(new_state[1])
            new_state[1].parent = current_state
            
    return new_states;    

def move(direction,state):
    
    new_state = copy.deepcopy(state)
    index = new_state.config.index( 0 )
    if direction == 'up':
        if index not in [0,1,2]:
           new_state.config[index - 3],new_state.config[index] = new_state.config[index],new_state.config[index-3]          
    elif direction == 'down':
        if index not in [6,7,8]:
            new_state.config[index + 3],new_state.config[index] = new_state.config[index],new_state.config[index + 3]  
    elif direction == 'left':
        if index not in [0,3,6]:
            new_state.config[index - 1],new_state.config[index] = new_state.config[index],new_state.config[index - 1]  
    else:
        if index not in [2,5,8]:
            new_state.config[index + 1],new_state.config[index] = new_state.config[index],new_state.config[index + 1]

    return (new_state.config != state.config,new_state)

def printPathtoGoal(current_state):
    print("Hello")
    stackTrace = Stack()
    while True:
        stackTrace.push(current_state.config)
        if current_state.parent == None :
            break
        current_state = current_state.parent
        
    while stackTrace.isEmpty() == False:
        state = stackTrace.pop()
        print(state[0],state[1],state[2])
        print(state[3],state[4],state[5])
        print(state[6],state[7],state[8])
        print()
        
        
class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()
        
     def size(self):
         return len(self.items)

class State :
    def __init__(self, config, parent, depth):
        self.config  = config
        self.parent = parent
        self.depth = depth
        
if __name__ == "__main__":
    
    initial_state_info = State(initial_state, None, 0)
    if checkSolvability(initial_state_info.config ) == True :
        if DFS_Search(initial_state_info, goal_state) == True:
            print("Solved")
        else:
            print("DFS FAiled")
    else:
        print ("Can't be Solved")
    