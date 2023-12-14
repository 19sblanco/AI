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
        """
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
    stack = util.Stack()
    expanded = []
    stack.push((problem.getStartState(), [], 0))

    while not stack.isEmpty():
        curr = stack.pop()
        curr_state = curr[0]
        curr_path = curr[1]
        curr_cost = curr[2]

        if problem.isGoalState(curr_state):
            return curr_path

        if curr_state in expanded: continue
        successors = problem.getSuccessors(curr_state)
        expanded.append(curr_state)

        for s in successors:
            s_state = s[0]
            new_path = curr_path.copy()
            new_path.append(s[1])
            new_cost = curr_cost + s[2]

            new_state = (s[0], new_path, new_cost)
            stack.push(new_state)
    


def breadthFirstSearch(problem):
    Queue = util.Queue()
    expanded = []
    Queue.push((problem.getStartState(), [], 0))

    while not Queue.isEmpty():
        curr = Queue.pop()
        curr_state = curr[0]
        curr_path = curr[1]
        curr_cost = curr[2]

        if problem.isGoalState(curr_state):
            return curr_path

        if curr_state in expanded: continue
        successors = problem.getSuccessors(curr_state)
        expanded.append(curr_state)

        for s in successors:
            s_state = s[0]
            s_action = s[1]
            new_path = curr_path.copy()
            new_path.append(s_action)
            new_cost = curr_cost + s[2]

            new_state = (s_state, new_path, new_cost)
            Queue.push(new_state)

def uniformCostSearch(problem):
    pq = util.PriorityQueue()
    expanded = []
    pq.push((problem.getStartState(), [], 0), 0)

    while not pq.isEmpty():
        curr = pq.pop()
        curr_state = curr[0]
        curr_path = curr[1]
        curr_cost = curr[2]

        if problem.isGoalState(curr_state):
            return curr_path

        if curr_state in expanded: continue
        successors = problem.getSuccessors(curr_state)
        expanded.append(curr_state)

        for s in successors:
            s_state = s[0]
            if s_state in expanded: continue
            new_path = curr_path.copy()
            new_path.append(s[1])
            new_cost = curr_cost + s[2]

            new_state = (s_state, new_path, new_cost)
            pq.push(new_state, new_cost)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    pq = util.PriorityQueue()
    expanded = []
    start = problem.getStartState()
    heuristic_prediction = heuristic(start, problem)
    pq.push((start, [], (0, heuristic_prediction)), heuristic_prediction)

    while not pq.isEmpty():
        curr = pq.pop()
        curr_state = curr[0]
        curr_path = curr[1]
        cost_to_curr = curr[2][0]
        curr_heuristic_cost = curr[2][1]
        cost_through_curr = cost_to_curr + curr_heuristic_cost

        if problem.isGoalState(curr_state):
            return curr_path

        if curr_state in expanded: continue
        successors = problem.getSuccessors(curr_state)
        expanded.append(curr_state)

        for s in successors:
            s_state = s[0]
            new_path = curr_path.copy()
            new_path.append(s[1])
            cost_to_s = cost_to_curr + s[2]
            s_heuristic = heuristic(s_state, problem)

            cost_tuple = (cost_to_s, s_heuristic)
            cost_through_s = cost_to_s + s_heuristic

            new_state = (s_state, new_path, cost_tuple)
            pq.push(new_state, cost_through_s)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
