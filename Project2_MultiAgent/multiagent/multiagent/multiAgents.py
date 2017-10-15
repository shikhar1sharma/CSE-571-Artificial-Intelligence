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


    def getAction(self, gameState):

        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):

        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
# Calculating the manhattan distance of the ghost from pacman
        ghostDistance = manhattanDistance(newPos,newGhostStates[0].getPosition())
        current_PacmanPos = currentGameState.getPacmanPosition()
        new_PacmanPosX = newPos[0]
        new_PacmanPosY = newPos[1]
#Checking if there is food in the new position then, give more importance to food.
        if newFood[new_PacmanPosX][new_PacmanPosY] == True and ghostDistance >=2:
            ghostDistance += 3
        else:
            if ghostDistance >=3:
                ghostDistance = 0

        return ghostDistance
#my code ends



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

        """
        "*** YOUR CODE HERE ***"
        def min_value(state, depth,agentNumber):
        # Returning the value of the node, if it is the leaf or the game has been won by pacman.
            if depth == 0:
                return (self.evaluationFunction(state))
            if state.isLose() or state.isWin():
                return (self.evaluationFunction(state))

            legalActions = state.getLegalActions(agentNumber)
            agent_new = state.getNumAgents() - 1
            X = agent_new
            min_score = (float("inf"))
            for actions in legalActions:
                succ = state.generateSuccessor(agentNumber,actions)
                if agentNumber == X :
                    score = max_value(succ,depth-1)
                    if score < min_score:
                        min_score = score
                else:
                #If there is still ghost
                    new_agent_num = agentNumber +1
                    score = min_value(succ,depth,new_agent_num)
                    if score < min_score:
                        min_score = score

            return min_score

        def max_value(state,depth):
            if depth == 0:
                return (self.evaluationFunction(state))
            if state.isLose() or state.isWin():
                return (self.evaluationFunction(state))

            legalActions = state.getLegalActions(0)
            score = -float("inf")
            # There will be ghost turn.
            for actions in legalActions:
                succ = state.generateSuccessor(0,actions)
                score = max(score,min_value(succ,depth,1))
            return score
        legalActions = gameState.getLegalActions(0)
        v_best = -(float("inf"))
        v = v_best
        action_required = Directions.EAST
        for actions in legalActions:
            succ = gameState.generateSuccessor(0,actions)
            v = min_value(succ,self.depth,1)
            if v>v_best:
                v_best = v
                action_required = actions

        return  action_required


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        

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
        def expectedMax(state, depth,agentNumber):
            if depth == 0:
                return (self.evaluationFunction(state))
            if state.isLose() or state.isWin():
                return (self.evaluationFunction(state))

            legalActions = state.getLegalActions(agentNumber)
            agent_new = state.getNumAgents() - 1
            X = agent_new
            score = 0
            count_actions = len(legalActions)
        # The main focus will be to sum up all the leaf nodes of a ghost state and find the average of that value.
        # This value will be the expected value for that node.
            for actions in legalActions:
                succ = state.generateSuccessor(agentNumber,actions)
                if agentNumber == X :
                    score += max_value(succ,depth-1)
                else:
                    new_agent_num = agentNumber +1
                    score += expectedMax(succ,depth,new_agent_num)

            probability = score/count_actions
            return probability

        def max_value(state,depth):
            if depth == 0:
                return (self.evaluationFunction(state))
            if state.isLose() or state.isWin():
                return (self.evaluationFunction(state))

            legalActions = state.getLegalActions(0)
            score = -float("inf")
        #
            for actions in legalActions:
                succ = state.generateSuccessor(0,actions)
                score = max(score,expectedMax(succ,depth,1))
            return score
        depth = self.depth
    # With the Pacman turn, we will call the expectedMax function and finds the expected value for that node
        legalActions = gameState.getLegalActions(0)
        v_best = -(float("inf"))
        v = v_best
        action_required = Directions.EAST
        for actions in legalActions:
            succ = gameState.generateSuccessor(0,actions)
            v = expectedMax(succ,self.depth,1)
            if v>v_best:
                v_best = v
                action_required = actions

        return  action_required

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    if currentGameState.isWin():
        return 1000
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    v = scoreEvaluationFunction(currentGameState)
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    # my code
    ghostDistance = manhattanDistance(newPos, newGhostStates[0].getPosition())
    current_PacmanPos = currentGameState.getPacmanPosition()
    #new_PacmanPosX = newPos[0]
    #new_PacmanPosY = newPos[1]
    foodDistance_min = float("inf")
    food_list = newFood.asList()
    for distance in food_list:
        foodDistance = util.manhattanDistance(distance,newPos)
        if foodDistance < foodDistance_min:
            foodDistance_min = foodDistance
            foodtoghostDistance = util.manhattanDistance(distance,newGhostStates[0].getPosition())
    if foodtoghostDistance > foodDistance_min:
        ghostDistance = ghostDistance*10

    return ghostDistance
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

