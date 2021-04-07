import random
import tkinter as tk
import time  # Time is needed to slow down the agent and to see how it runs
from PIL import Image, ImageTk  # For adding images into the canvas widget

class Agent(object):
    def __init__(self, shape, state):
        self.shape = shape
        self.state = state

# Global variable for dictionary with coordinates for the final route
a = {}


# Creating class for the environment
class Environment(tk.Tk, object):

    pixels = 24

    def __init__(self, shape=(10, 10), delay=0.02, stop_at_goal=False):
        super(Environment, self).__init__()
        self.env_height = shape[0]
        self.env_width = shape[1]
        self.delay = delay
        self.num_obstacles = self.env_height + self.env_width
        self.stop_at_goal = stop_at_goal

        self.action_space = ['U', 'D', 'L', 'R']
        self.n_actions = len(self.action_space)
        self.title('Path Following')
        self.geometry('{0}x{1}'.format(self.env_width * self.pixels, self.env_height * self.pixels))
        self.build_environment()

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

    def _create_obstacle(self, row, col):
        self.canvas_widget.create_rectangle(
            (col + 0) * self.pixels, (row + 0) * self.pixels,
            (col + 1) * self.pixels, (row + 1) * self.pixels,
            outline='grey', fill='#6b9bbf'
        )
        self.coords_obstacles.append((row, col),)

    # Function to build the environment
    def _prep_widget(self):
        self.canvas_widget = tk.Canvas(self, bg='white',
                                       height=self.env_height * self.pixels,
                                       width=self.env_width * self.pixels)
        img_background = Image.open("images/bg.png")
        self.background = ImageTk.PhotoImage(img_background)
        self.bg = self.canvas_widget.create_image(0, 0, anchor='nw', image=self.background)
        for col in range(0, self.env_width + 1):
            x0 = x1 = col * self.pixels
            y0 = 0
            y1 = self.pixels * self.env_height
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')
        for row in range(0, self.env_height + 1):
            y0 = y1 = row * self.pixels
            x0 = 0
            x1 = self.pixels * self.env_width
            self.canvas_widget.create_line(x0, y0, x1, y1, fill='grey')

    def _add_obstacles(self):
        # Creating a list of random obstacles
        self.obstacles = []
        self.coords_obstacles = []
        for oi in range(self.num_obstacles):
            row, col = (random.randint(0, self.env_width), random.randint(0, self.env_width))
            if (row, col) == (0, 0):
                continue
            self._create_obstacle(row, col)

    def _center_of_box(self, px, p):
        x = p[0] * px + px // 2
        y = p[1] * px + px // 2
        return x, y

    def _add_marker(self, state, color='#FF3455'):
        x, y = self._center_of_box(self.pixels, state)
        rad = int(self.pixels * 1/3)
        shape = self.canvas_widget.create_oval(
            x - rad, y - rad, x + rad, y + rad,
            outline='#FF3455', fill=color
        )
        return shape

    def _add_agent(self):
        state = [0, 0]
        shape = self._add_marker(state)
        try:
            self.canvas_widget.delete(self.agent.shape)
        except:
            pass
        self.agent = Agent(shape, state)

    def _add_goal(self):
        row = int(self.env_height * 4/5)
        col = int(self.env_width * 4/5)
        self.canvas_widget.create_rectangle(
            (col + 0) * self.pixels, (row + 0) * self.pixels,
            (col + 1) * self.pixels, (row + 1) * self.pixels,
            outline='grey', fill='#22ee00'
        )
        self.goal = (row, col)

    def build_environment(self):
        # Prepare widget with background, and grid
        self._prep_widget()
        # Add a few random obstacles
        self._add_obstacles()
        # Create agent
        self._add_agent()
        # Create goal
        self._add_goal()
        # Packing everything
        self.canvas_widget.pack()

    # Function to reset the environment and start new Episode
    def reset(self):
        self.update()
        #time.sleep(0.5)

        # Updating agent
        self._add_agent()

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
        self.canvas_widget.move(self.agent.shape, base_action[1] * self.pixels, base_action[0] * self.pixels)
        self.agent.state = next_state

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

        elif next_state in self.coords_obstacles:

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
        self.update()

    # Function to show the found route
    def final(self):
        # Deleting the agent at the end
        self.canvas_widget.delete(self.agent)

        # Showing the number of steps
        print('The shortest route:', self.shortest)
        print('The longest route:', self.longest)

        # Creating initial point
        self._add_agent()
        self._add_marker((0, 0), color='blue')

        # Filling the route
        for j in range(len(self.f)):
            # Showing the coordinates of the final route
            s = self.f[j]
            print(s)
            self._add_marker(list(reversed(s)), color='blue')
            self.update()
            a[j] = self.f[j]
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
