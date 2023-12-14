# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    neg_inf = -999999
    inf = 999999


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        """
        print("printing....")
        print("action", action)
        print(" currentGameState\n",  currentGameState)
        print("successorGameState\n",successorGameState )
        print("newPos\n", newPos )
        print("newFood\n", newFood )
        print("newGhostStates\n", newGhostStates )
        print("newScaredTimes\n", newScaredTimes )
        print("\n")

        exit(0)
        """
        "*** YOUR CODE HERE ***"
        """
        reasoning through the game:
            goal: get all the food / power pellets w/out dying and have the most amount of points possible
            actions: up,down,left,right,stop, chosen based on highests score
            score: 
                * goes way up with a ghost eaten
                * goes up with number of food eaten
                * goes down with time
            cannot die

            thoughts:
                * if your next position and the ghosts next position overlap, you return -infinity (don't die)
                ? we want him to follow food somehow (just use score?)
                * if you get a power pellet and you are in time to catch a ghost, return a high boost in score based on distance (the closer the better)
                * return higher score based on closesness to food


        ideas:
            look at auto grader map and determine the best closest distance between pacman and any ghost at a given time
                * based on new position of pacman adn the ghosts and the state of the ghost and maybe the amount of time that they have left

        """

        # make sure pacman is always at least one square away from a ghost
        nearest_ghost_distance = self.inf
        for i in range(len(newGhostStates)):
            ghost_pos = newGhostStates[i].getPosition()
            dist = manhattanDistance(newPos, ghost_pos)
            if dist < nearest_ghost_distance:
                nearest_ghost_distance = dist
        if nearest_ghost_distance <= 1:
            return self.neg_inf


        # add points based on distance to the closest food (inverse of distance)
        score = successorGameState.getScore()
        food_locations = currentGameState.getFood().asList()
        closest_food = None
        closest_food_dist = self.inf
        for i in range(len(food_locations)):
            dist = manhattanDistance(newPos, food_locations[i])
            if dist < closest_food_dist:
                closest_food = food_locations[i]
                closest_food_dist = dist
        if closest_food_dist == 0:
            pass
        else:
            score += 1 / closest_food_dist


        return score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        value, action = self.minimax_max(gameState, self.depth)
        return action


    def minimax_max(self, gameState, depth):
        if gameState.isWin(): return (self.evaluationFunction(gameState), None)
        if gameState.isLose(): return (self.evaluationFunction(gameState), None)
        if depth == 0: return (self.evaluationFunction(gameState), None)

        pacman_action_values = [] # values for each pacman action
        legal_actions = gameState.getLegalActions(0)
        for action in legal_actions: 
            successor = gameState.generateSuccessor(0, action)
            value, a = self.minimax_min(successor, depth, 1)
            pacman_action_values.append( (value, action ) )

        return max(pacman_action_values)


    def minimax_min(self, gameState, depth, agent):
        if gameState.isWin(): return (self.evaluationFunction(gameState), None)
        if gameState.isLose(): return (self.evaluationFunction(gameState), None)

        last_agent = gameState.getNumAgents() - 1
        ghost_action_values = []
        legal_actions = gameState.getLegalActions(agent)
        for action in legal_actions:
            successor = gameState.generateSuccessor(agent, action)
            if agent == last_agent:
                value, a = self.minimax_max(successor, depth-1)
            else:
                value, a = self.minimax_min(successor, depth, agent+1)
            ghost_action_values.append( (value, action) )
        
        return min(ghost_action_values)
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    inf = 999999
    neg_inf = -999999

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value, action = self.max_value(gameState, self.depth, self.neg_inf, self.inf)
        return action


    def max_value(self, gameState, depth, alpha, beta):
        if gameState.isWin(): return (self.evaluationFunction(gameState), None)
        if gameState.isLose(): return (self.evaluationFunction(gameState), None)
        if depth == 0: return (self.evaluationFunction(gameState), None)

        pacman_action_values = [] # values for each pacman action
        legal_actions = gameState.getLegalActions(0)
        for action in legal_actions: 
            successor = gameState.generateSuccessor(0, action)
            value, a = self.min_value(successor, depth, 1, alpha, beta)
            pacman_action_values.append( (value, action ) )

            if value > beta: return (value, action)
            alpha = max(alpha, value)

        return max(pacman_action_values)

    def min_value(self, gameState, depth, agent, alpha, beta):
        if gameState.isWin(): return (self.evaluationFunction(gameState), None)
        if gameState.isLose(): return (self.evaluationFunction(gameState), None)

        last_agent = gameState.getNumAgents() - 1
        ghost_action_values = []
        legal_actions = gameState.getLegalActions(agent)
        for action in legal_actions:
            successor = gameState.generateSuccessor(agent, action)
            if agent == last_agent:
                value, a = self.max_value(successor, depth-1, alpha, beta)
            else:
                value, a = self.min_value(successor, depth, agent+1, alpha, beta)
            ghost_action_values.append( (value, action) )

            if value < alpha: return (value, action)
            beta = min(beta, value)
        
        return min(ghost_action_values)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        value, action = self.minimax_max(gameState, self.depth)
        # action = gameState.getLegalActions(0)[0]
        return action



    # TODO: study the change nodes
    def minimax_max(self, gameState, depth):
        """
        """
        if gameState.isWin(): return (self.evaluationFunction(gameState), None)
        if gameState.isLose(): return (self.evaluationFunction(gameState), None)
        if depth == 0: return (self.evaluationFunction(gameState), None)

        pacman_action_values = [] # values for each pacman action
        legal_actions = gameState.getLegalActions(0)
        for action in legal_actions: 
            successor = gameState.generateSuccessor(0, action)
            value, a = self.minimax_min(successor, depth, 1)
            pacman_action_values.append( (value, action ) )


        return max(pacman_action_values)


    def minimax_min(self, gameState, depth, agent):
        """
        """
        if gameState.isWin(): return (self.evaluationFunction(gameState), None)
        if gameState.isLose(): return (self.evaluationFunction(gameState), None)

        last_agent = gameState.getNumAgents() - 1
        ghost_action_values = []
        legal_actions = gameState.getLegalActions(agent)
        for action in legal_actions:
            successor = gameState.generateSuccessor(agent, action)
            if agent == last_agent:
                value, a = self.minimax_max(successor, depth-1)
            else:
                value, a = self.minimax_min(successor, depth, agent+1)
            ghost_action_values.append( value )

        sum = 0
        for value in ghost_action_values:
            sum += value
        sum /= len(legal_actions)
        return (sum, None)





def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    """
    if your dead then return negative infinity

    base score on current game score 

    awards points based on distance to food
    """
    inf = 999999
    value, action = max_value(currentGameState, 1, -inf, inf)
    return value

def betterEvaluationHelper(currentGameState):
    inf = 9999999
    gameState = currentGameState
    score = gameState.getScore()
    if gameState.isWin(): return score
    if gameState.isLose(): return score

    food_locations = currentGameState.getFood().asList()
    closest_food_dist = inf
    pos = currentGameState.getPacmanPosition()
    for i in range(len(food_locations)):
        dist = manhattanDistance(pos, food_locations[i])
        if dist < closest_food_dist:
            closest_food_dist = dist
    if closest_food_dist == 0:
        pass
    else:
        score += 1 / closest_food_dist

    return score


def max_value(gameState, depth, alpha, beta):
    if gameState.isWin(): return (betterEvaluationHelper(gameState), None)
    if gameState.isLose(): return (betterEvaluationHelper(gameState), None)
    if depth == 0: return (betterEvaluationHelper(gameState), None)

    pacman_action_values = [] # values for each pacman action
    legal_actions = gameState.getLegalActions(0)
    for action in legal_actions: 
        successor = gameState.generateSuccessor(0, action)
        value, a = min_value(successor, depth, 1, alpha, beta)
        pacman_action_values.append( (value, action ) )

        if value > beta: return (value, action)
        alpha = max(alpha, value)

    return max(pacman_action_values)

def min_value(gameState, depth, agent, alpha, beta):
    if gameState.isWin(): return (betterEvaluationHelper(gameState), None)
    if gameState.isLose(): return (betterEvaluationHelper(gameState), None)

    last_agent = gameState.getNumAgents() - 1
    ghost_action_values = []
    legal_actions = gameState.getLegalActions(agent)
    for action in legal_actions:
        successor = gameState.generateSuccessor(agent, action)
        if agent == last_agent:
            value, a = max_value(successor, depth-1, alpha, beta)
        else:
            value, a = min_value(successor, depth, agent+1, alpha, beta)
        ghost_action_values.append( (value, action) )

        if value < alpha: return (value, action)
        beta = min(beta, value)
    
    return min(ghost_action_values)




# Abbreviation
better = betterEvaluationFunction
