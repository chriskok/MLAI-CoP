
from grid import Grid
from agent import DPAgentGrid

# Define a 6x6 grid
env = Grid(6)

# Instantiate two agents with their starting points, destinations, and 'traps'.
agent1 = DPAgentGrid('A', env, (0, 0), (5, 5), (5, 4))
agent2 = DPAgentGrid('B', env, (5, 0), (0, 5), (1, 5))

# Initialize policy. Each state will have a value.
agent1.init_policy()
agent2.init_policy()

# Improve policy for agent 1.
agent1.improve_policy(True)
agent1.show_policy()
agent1.show_V()

# Improve policy for agent 2.
agent2.improve_policy(False)
agent2.show_policy()
agent2.show_V()


# Show results.
agent1.show_policy()
agent2.show_policy()
input('Policy compute. Press Enter to see paths')

# Show agents reaching target by following policy.
moving = True
while moving:
    env.render()
    moving = env.step()
