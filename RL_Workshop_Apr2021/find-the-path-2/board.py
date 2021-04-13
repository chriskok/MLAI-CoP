import numpy as np
import time
import random


class Agent(object):
    def __init__(self, name, state, obj):
        self.name = name
        self.state = state
        self.obj = obj


# Global variable for dictionary with coordinates for the final route
a = {}


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


class BoardObject(object):

    def _circle_mask(self):
        mask = np.zeros((self.board.pixels, self.board.pixels, 3), dtype=np.uint8)
        for i in range(self.board.pixels):
            ii = self.board.pixels // 2 - i
            for j in range(self.board.pixels):
                jj = self.board.pixels // 2 - j
                if self.rad2 > jj**2 + ii**2:
                    mask[i, j, :] = 1
        return mask

    def __init__(self, name, board, x=0, y=0, layer=1, color='#999999', style=None):
        self.board = board
        self.name = name
        self.layer = layer
        self.style = style
        self.box = [x, y, x+board.pixels, y+board.pixels]
        self.color = color
        self.rad2 = int(self.board.pixels * .3) ** 2
        self.mask = 1 if style is None else self._circle_mask()

    def move(self, dx, dy):
        x0, y0 = self.box[0], self.box[1]
        if self.layer > 0:
            self.board.color_area(x0, y0, '#000', layer=self.layer)
        self.board.color_area(x0+dx, y0+dy, self.color, layer=self.layer, mask=self.mask)
        self.box = [x0+dx, y0+dy]


class BoardDisplay(object):

    @staticmethod
    def center_of_box(self, px, p):
        x = p[0] * px + px // 2
        y = p[1] * px + px // 2
        return x, y

    def __init__(self, board, pixels, vis):
        self.board = board
        self.pixels = pixels
        self.image = np.zeros([2] + [a*pixels for a in board.shape] + [3], dtype=np.uint8)
        self.image[0] += 255
        self.image[0, :, ::pixels] = 22
        self.image[0, ::pixels, :] = 22
        self.vis = vis
        self.objects = {}

    def color_area(self, x, y, color, layer=0, mask=1):
        try:
            self.image[layer, y:y+self.pixels, x:x+self.pixels] = mask * hex_to_rgb(color)
        except:
            pass
        self.image[layer, y:y+1, x:x+self.pixels] = 22
        self.image[layer, y:y+self.pixels, x:x+1] = 22

    def update(self):
        self.vis.imshow(self.board)

    def add_object(self, name, state, color, layer=0, style=None, keep=False):
        def _make_name():
            return 'N' + str(time.time() + random.randint(1, 99))
        if name is None:
            name = _make_name()
            while name in self.objects:
                name = _make_name()
        x, y = self.xy_from_state(state)
        o = BoardObject(name, self, x, y, layer, color, style)
        self.objects[name] = o
        if layer > 0 and not keep:
            self.clear_layer(layer)
        o.move(0, 0)
        return o

    def xy_from_state(self, state):
        y = state[0] * self.pixels
        x = state[1] * self.pixels
        return x, y

    def move(self, name, dy, dx, layer=0):
        a = self.objects[name]
        a.move(dx, dy)

    def clear_layer(self, layer):
        self.image[layer, :, :, :] = 0


class Environment(object):

    def __init__(self):
        pass

# Creating class for the environment
class Board(object):

    def __init__(self, grid=[(10, 10)], delay=0.02, stop_at_goal=False, vis=None):
        super().__init__()
        self.shape = grid[0]
        self.env_height = grid[0][0]
        self.env_width = grid[0][1]
        self.delay = delay
        self.stop_at_goal = stop_at_goal
        self.action_space = ['U', 'D', 'L', 'R']
        self.n_actions = len(self.action_space)
        self.display = BoardDisplay(self, 24, vis)
        self.agent = None
        self.build_environment(grid[1:])
        self.path = []

        # Dictionaries to draw the final route
        self.d = {}
        self.f = {}

        # Key for the dictionaries
        self.i = 0

        # Writing the final dictionary first time
        self.c = True

        # Showing the steps for longest found route
        self.longest = 0

        # Showing the steps for the shortest route
        self.shortest = 0

    def _create_obstacle(self, state):
        self._add_object(None, state, '#88bbdd')
        self.obstacles.append(state)

    def _add_obstacles(self, obstacles):
        # Creating a list of random obstacles
        self.obstacles = []
        if obstacles is None:
            self.num_obstacles = (self.env_height + self.env_width)
            for oi in range(self.num_obstacles):
                col, row = (random.randint(0, self.env_width-1), random.randint(0, self.env_height-1))
                if (row, col) == (0, 0):
                    continue
                if (row, col) == self.goal:
                    continue
                self._create_obstacle((row, col),)
        else:
            self.num_obstacles = len(obstacles)
            for o in obstacles:
                self._create_obstacle(o)

    def _add_object(self, name, state, color, layer=0, style=None):
        return self.display.add_object(name, state, color, layer, style)

    def _add_agent(self, name):
        state = [0, 0]
        obj = self._add_object(name, state, color='#FF3455', layer=1, style='circle')
        self.agent = Agent(name, state, obj)

    def _add_goal(self, goal):
        if goal is None:
            row = int(self.env_height * 4/5)
            col = int(self.env_width * 4/5)
        else:
            row, col = goal
        self.display.add_object('Goal', (row, col), '#22ee00')
        self.goal = (row, col)

    def build_environment(self, grid_data):
        goal = None if len(grid_data) < 1 else grid_data[0]
        obstacles = None if len(grid_data) < 2 else grid_data[1]
        # Create goal
        self._add_goal(goal)
        # Add a few random obstacles
        self._add_obstacles(obstacles)

    # Function to reset the environment and start new Episode
    def reset(self):
        self.display.update()
        #time.sleep(0.5)

        # Updating agent
        self._add_agent('Agent')

        # Clearing the dictionary and the i
        self.d = {}
        self.i = 0

        # Return observation
        return 'start'

    # Function to get the next observation and reward by doing next step
    def step(self, action):

        # Current state of the agent
        state = self.agent.state
        base_action = [0, 0]

        # Updating next state according to the action
        # Action 'up'
        if action == 0:
            if state[0] > 0:
                base_action[0] -= 1
        # Action 'down'
        elif action == 1:
            if state[0] < (self.env_height - 1):
                base_action[0] += 1
        # Action 'left'
        elif action == 2:
            if state[1] > 0:
                base_action[1] -= 1
        # Action 'right'
        elif action == 3:
            if state[1] < (self.env_width - 1):
                base_action[1] += 1

        # Moving the agent according to the action
        next_state = [v + base_action[i] for i, v in enumerate(state)]
        assert next_state[0] >=0 and next_state[0] < self.env_height
        assert next_state[1] >=0 and next_state[1] < self.env_width
        self.agent.state = next_state

        self.display.move(self.agent.name, base_action[0]*self.display.pixels, base_action[1]*self.display.pixels, layer=1)

        # Writing in the dictionary coordinates of found route
        self.d[self.i] = tuple(self.agent.state)

        # Updating next state
        next_state = self.d[self.i]

        # Updating key for the dictionary
        self.i += 1

        # Calculating the reward for the agent
        if next_state == self.goal:
            #time.sleep(0.001)
            reward = 1
            done = True
            next_state = 'goal'
            print('*********** GOOOOOOOOOOOOOOOOOOOOOOOOAL ****************')
            if self.stop_at_goal:
                input('Goal reached')

            # Filling the dictionary first time
            if self.c == True:
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]
                self.c = False
                self.longest = len(self.d)
                self.shortest = len(self.d)

            # Checking if the currently found route is shorter
            if len(self.d) < len(self.f):
                # Saving the number of steps for the shortest route
                self.shortest = len(self.d)
                # Clearing the dictionary for the final route
                self.f = {}
                # Reassigning the dictionary
                for j in range(len(self.d)):
                    self.f[j] = self.d[j]

            # Saving the number of steps for the longest route
            if len(self.d) > self.longest:
                self.longest = len(self.d)

        elif next_state in self.obstacles:

            reward = -1
            done = True
            next_state = 'obstacle'

            # Clearing the dictionary and the i
            self.d = {}
            self.i = 0


        else:
            reward = 0
            done = False

        return next_state, reward, done

    # Function to refresh the environment
    def render(self):
        if self.delay is not None:
            time.sleep(self.delay)
        self.display.update()

    # Function to show the found route
    def final(self):
        # Deleting the agent at the end
        self.display.clear_layer(1)

        # Showing the number of steps
        print('The shortest route:', self.shortest)
        print('The longest route:', self.longest)

        # Creating initial point
        color = '#662233'
        s = (0, 0)

        # Filling the route

        self._add_object(None, s, '#cccc00')
        self.path.append(s)
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            s = self.f[j]
            print(s)
            self.path.append(s)
            self._add_object(None, s, '#cccc00')
            self.render()
            a[j] = self.f[j]
        import matplotlib.pyplot as plt
        plt.show()
        return


# Returning the final dictionary with route coordinates
# Then it will be used in agent_brain.py
def final_states():
    return a


# This we need to debug the environment
# If we want to run and see the environment without running full algorithm
if __name__ == '__main__':
    env = Environment()
    env.mainloop()
