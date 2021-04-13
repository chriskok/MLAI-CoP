import numpy as np


class DPAgentGrid(object):

    action_space = range(4)
    close_enough = 1e-3
    gamma = .9

    def __init__(self, name, grid, start, win, lose):
        self.name = name
        self.grid = grid
        self.start = start
        self.win = win
        self.lose = lose
        self.grid.add_agent(self)
        self.state = self.start
        self._init_probability()
        self._init_V()

    def reset(self):
        pass

    def play(self):
        self.grid.render()
        while not self._is_terminal(self.state):
            a = next(iter(self.policy[self.state]))
            self.move(a)
            self.grid.render()

    def move(self, a=None):
        if a is None:
            s = self.policy[self.state]
            if s is None:
                return False
            a = next(iter(self.policy[self.state]))
        self.state = self._next_state(self.state, a)
        return True

    def _act_view(self, ap):
        if ap is None:
            return '    '
        y = ''
        for a in ap:
            y += ['D', 'R', 'U', 'L'][a]
        y = (y+' '*len(self.action_space))[:len(self.action_space)]
        return y

    def show_policy(self):
        print('Policy', self.name, end='')
        for s in self._iter_states():
            if s[1] == 0:
                print()
            print(self._act_view(self.policy[s]), end=' ')
        print()
        print()

    def show_V(self):
        def _special_state(s):
            if s == self.win:
                return None, '   W '
            if s == self.lose:
                return None, '   L '
            if s == self.start:
                return None, '   S '
            return self.V.get(s, 0), None

        print()
        print('Value', end='')
        for s in self._iter_states():
            if s[1] == 0:
                print()
            x, w = _special_state(s)
            print(w if w else (' ' if x >= 0 else '') + ("%.2f" % x), end=' ')
        print()
        print()

    def step(self, action):
        pass

    def _is_terminal(self, s):
        return s == self.win or s == self.lose

    def game_over(self):
        return self.state == self.win or self.state == self.lose

    def _init_V(self):
        self.V = {}
        states = self._iter_states()
        for s in states:
            if self._is_terminal(s):
                continue
            ri, ci = tuple(s)
            self.V[s] = 0

    def _iter_states(self):
        return self.grid.locations()

    def _init_probability(self):
        self.rewards = {}
        self.trans_prob = {}
        states = self._iter_states()
        for s0 in states:
            if self._is_terminal(s0):
                continue
            for a in self.action_space:
                s1 = self._next_state(s0, a)
                self.trans_prob[(s0, a, s1)] = 1
                if s1 == self.win:
                    self.rewards[(s0, a, s1)] = 1
                elif s1 == self.lose:
                    self.rewards[(s0, a, s1)] = -1

    def _next_state(self, s, a):
        s = list(s)
        def _inc_ind(s, a):
            if a == 0:
                s[0] += 1
            if a == 1:
                s[1] += 1
            if a == 2:
                s[0] -= 1
            if a == 3:
                s[1] -= 1
        _inc_ind(s, a)
        return tuple(s)

    def init_policy(self):
        self.policy = {}
        states = self._iter_states()
        for s in states:
            if self._is_terminal(s):
                a = None
            else:
                a = {np.random.choice(self.action_space): 1.}
            self.policy[s] = a

    def evaluate_policy(self):
        self.show_policy()
        it = 0
        maxit = 1000
        while it < maxit:
            biggest_change = 0
            for s0 in self._iter_states():
                if self._is_terminal(s0):
                    continue
                old_v = self.V.get(s0, 0)
                new_v = 0
                for a in self.action_space:
                    for s1 in self._iter_states():
                        assert len(self.policy[s0]) == 1
                        act_prob = 1 if a in self.policy[s0] else 0
                        r = self.rewards.get((s0, a, s1), 0)
                        new_v += act_prob * self.trans_prob.get((s0, a, s1), 0) * (r + self.gamma * self.V.get(s1, 0))
                self.V[s0] = new_v
                biggest_change = max(biggest_change, np.abs(old_v - self.V[s0]))

            print('Iteration:', it+1, ' Biggest change: {:.3f}'.format(biggest_change))
            it += 1

            if biggest_change < self.close_enough:
                break
        self.show_V()

    def improve_policy(self, stop=False):
        self.evaluate_policy()
        converged = True
        for s0 in self._iter_states():
            if self._is_terminal(s0):
                continue
            old_a = next(iter(self.policy[s0]))
            new_a = None
            best_value = float('-inf')
            for a in self.action_space:
                v = 0
                for s1 in self._iter_states():
                    r = self.rewards.get((s0, a, s1), 0)
                    v += self.trans_prob.get((s0, a, s1), 0) * (r + self.gamma * self.V.get(s1, 0))
                if v > best_value:
                    best_value = v
                    new_a = a

            self.policy[s0] = {new_a: 1.}
            if new_a != old_a:
                converged = False
        if converged:
        	print('Policy converged')
        	return 


    def compute_policy(self, stop=False):
        while True:
        	improve_policy()



