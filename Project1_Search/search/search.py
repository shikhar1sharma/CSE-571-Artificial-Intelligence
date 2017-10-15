# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """0
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
"""
    start_state = problem.getStartState()
    #current_state = start_state
    #print "Start", start_state
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    
    "*** YOUR CODE HERE ***"

    visited_nodes = set()
    object_Stack = util.Stack()
    object_Stack.push((start_state,[],0)) # Push the root node in the stack
    
    while not object_Stack.isEmpty():
        current_node = object_Stack.pop() # Pop the current node from stack
        if current_node[0] in visited_nodes: # If the node is already visited, continue
             continue;
        visited_nodes.add(current_node[0]) # add the visited node in a list
        
        if problem.isGoalState(current_node[0]):
            return current_node[1]
        successor_state = problem.getSuccessors(current_node[0]) # Find the children of the current node
        
        for successors in successor_state:
            if not successors[0] in visited_nodes :
                object_Stack.push((successors[0],current_node[1]+[successors[1]],successors[2]))
    return []
    util.raiseNotDefined()
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first.""" 
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    visited_nodes = set()
    object_Queue = util.PriorityQueue()
    object_Queue.push((start_state,[],0),len(visited_nodes)) # Push the root node in the priority queue with the priority as the depth
    
    while not object_Queue.isEmpty():
        current_node = object_Queue.pop() # Pop the current node from queue
        if current_node[0] in visited_nodes: # If the node is already visited, continue
             continue;
        visited_nodes.add(current_node[0])
        
        if problem.isGoalState(current_node[0]):
            return current_node[1]
        successor_state = problem.getSuccessors(current_node[0]) # Find the children of the current node
        
        for successors in successor_state:
            object_Queue.push((successors[0],current_node[1]+[successors[1]],successors[2]),len(visited_nodes)+1)
    return []
    
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    
    start_state = problem.getStartState()
    visited_nodes = set()
    cost = 0
    object_Queue = util.PriorityQueue()
    object_Queue.push((start_state,[],0),cost) # Push the root node in the priority queue with the priority as path cost
    
    while not object_Queue.isEmpty():
        current_node = object_Queue.pop()
        
        if current_node[0] in visited_nodes:
             continue;
        visited_nodes.add(current_node[0])
        cost = current_node[2]
        if problem.isGoalState(current_node[0]):
            return current_node[1]
        successor_state = problem.getSuccessors(current_node[0])
        
        for successors in successor_state:
            if not successors[0] in visited_nodes :
                object_Queue.push((successors[0],current_node[1]+[successors[1]],successors[2]+cost),successors[2]+cost)
    return []
    
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    visited_nodes = set()
    cost = 0
    heuristic_node = heuristic(start_state, problem)
    object_Queue = util.PriorityQueue()
    object_Queue.push((start_state,[],0),cost+heuristic_node) # Push the root node in the priority queue with the priority as path cost and heuristic
    
    while not object_Queue.isEmpty():
        current_node = object_Queue.pop()
        
        if current_node[0] in visited_nodes:
             continue;
        visited_nodes.add(current_node[0])
        cost = current_node[2]
        if problem.isGoalState(current_node[0]):
            return current_node[1]
        successor_state = problem.getSuccessors(current_node[0])
        
        for successors in successor_state:
            if not successors[0] in visited_nodes :
                heuristic_node = heuristic(successors[0], problem)
                object_Queue.push((successors[0],current_node[1]+[successors[1]],successors[2]+cost),successors[2]+cost+heuristic_node)
    return []
    
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch

astar = aStarSearch
ucs = uniformCostSearch
