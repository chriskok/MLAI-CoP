
from board import Board
from agent import QLearningTable


def improve_table(env, q, episodes=100, stop_at_goal=False):
    # Resulted list for the plotting Episodes via Steps
    steps = []

    # Summed costs for all episodes in resulted list
    all_costs = []

    for episode in range(episodes):
        print('Episode ', episode, 'of', episodes)
        observation = env.reset()
        i = 0
        cost = 0
        while True:
            env.render()  # Update view of environment
            action = q.choose_action(str(observation)) # Choose action
            observation_, reward, done = env.step(action)  # 
            cost += q.learn(str(observation), action, reward, str(observation_))
            if done:
                print(observation_)
            observation = observation_
            i += 1
            if done:  # Episode ends when an obstacle or the target are reached
                steps += [i]
                all_costs += [cost]
                break
    env.final()  # Show final route
    q.print_q_table()  # Show final Q-table
    q.plot_results(steps, all_costs)  # Plot stats

def run_example(grid=[(7, 9)], episodes=100, stop_at_goal=False, delay=None, vis=None):
    env = Board(grid, delay, stop_at_goal, vis)
    q = QLearningTable(actions=list(range(env.n_actions)))
    improve_table(env, q, episodes)
