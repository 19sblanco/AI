# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

        # print("in constructor")
        # print("states", mdp.getStates())

        # state = mdp.getStates()[3]
        # action = mdp.getPossibleActions(state)[0]
        # transition_states = mdp.getTransitionStatesAndProbs(state, action)
        # nextState = transition_states[0][0]
        # reward = mdp.getReward(state, action, nextState)

        # print("state, action", state, action)
        # print("is terminal", mdp.isTerminal(state))
        # print("transition states", transition_states)
        # print("reward", reward)

        # exit()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        prev_state_values = util.Counter()
        new_state_values = util.Counter()

        # set states 
        states = self.mdp.getStates()
        for state in states:
            prev_state_values[state]
            new_state_values[state]
        
        for i in range(self.iterations):
            for state in states:
                if self.mdp.isTerminal(state): continue

                # get values for actions
                actions = self.mdp.getPossibleActions(state)
                values = []
                for action in actions:
                    transition_states = self.mdp.getTransitionStatesAndProbs(state, action)

                    # get value of action
                    sum = 0
                    for nextState, probability in transition_states:
                        reward = self.mdp.getReward(state, action, nextState)
                        vi_s_prime = prev_state_values[nextState]
                        sum += probability * (reward + (self.discount * vi_s_prime))
                    values.append(sum)
                
                # set best value
                new_state_values[state] = max(values)

            # update state dict
            prev_state_values = new_state_values.copy()

        self.values = new_state_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        transition_states = self.mdp.getTransitionStatesAndProbs(state, action)
        value = 0
        for nextState, probability in transition_states:
            reward = self.mdp.getReward(state, action, nextState)
            vi_s_prime = self.values[nextState]
            value += probability * (reward + (self.discount * vi_s_prime))
        return value




    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        value_actions = []
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            transition_states = self.mdp.getTransitionStatesAndProbs(state, action)
            value = 0
            for nextState, probability in transition_states:
                reward = self.mdp.getReward(state, action, nextState)
                vi_s_prime = self.values[nextState]
                value += probability * (reward + (self.discount * vi_s_prime))
            value_actions.append( (value, action) )
        max_value_action = max(value_actions)
        return max_value_action[1]


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"

