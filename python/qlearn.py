import random

__author__ = 'micheal/yazan'

class QLearn():
    """
    This class defines the Q Learning model free reinforcement learning 
    algorithm, essentially mapping a state tuple to an optimal action.
    """
    def __init__(self, all_actions, state_size, alpha):
        self.alpha = alpha
        self.all_actions = all_actions
        self.state_sz = state_size

    def Q(self, s, a):
        """ 
        Simple evaluation of Q function
        """
        return self.q.get((tuple(s), a), 0.0)

    def get_action(self, s):
        """
        This function will take the current state and choose
           what the Q function believes to the best action and return it
        """
        if len(s) != self.state_sz:
            raise Exception('invalid state dim')

        # random actions are needed for learning to avoid local optimums
        if random.random() < 0.07:
            return random.choice(self.all_actions)

        all_q_vals = [(action, self.Q(s, action)) for action in self.all_actions]
        best_index = 0
        best_q_val = -(1 << 30)
        for i in range(len(all_q_vals)):
            if all_q_vals[i] > best_q_val:
                best_q_val = all_q_vals[i]
                best_index = i
        return self.all_actions[best_index]

    def updateQ(self, state, action, reward, value):
        """
        Apply update to Q functions lookup table based on the Q learning equation
        """
        oldv = self.q.get((tuple(state), action), None)
        if oldv is None:
            self.q[(tuple(state), action)] = reward
        else:
            self.q[(tuple(state), action)] = oldv + self.alpha * (value - oldv)

    def learnQ(self, state1, action, state2, reward):
        """ 
        This function will update the Q function to respond the actions impact 
            on state1 to state2 based on the given reward
        """

        if len(state1) != self.state_sz or len(state2) != self.state_sz:
            raise Exception('invalid state dim')

        best_q_new = max([self.Q(state2, a) for a in self.actions])
        self.updateQ(state1, action, reward, reward + self.alpha * best_q_new)