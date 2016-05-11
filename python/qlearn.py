"""Flow - Algorithmic HF trader

   Copyright 2016, Yazan Obeidi

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import random

__author__ = 'micheal/yazan'

class QLearn():
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
        if random.random() < 0.10:
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
