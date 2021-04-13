import matplotlib.pyplot as plt
from IPython import display
import numpy as np

class Visual(object):

    def __init__(self, local=False):
        self.cells = []
        self.rows = None
        self.cols = None
        self.agent = (0, 0)
        self.save = {}
        self.local = local

    def imshow(self, board, text=None):

        def bg(i, j):
            x = (j + i % 2) % 2
            return x * 10 + 244

        col_obs = [0, 66, 120]
        col_dest = [0, 200, 33]
        col_path = [150, 150, 0]
        if self.rows is None:
            self.rows = board.env_height
            self.cols = board.env_width
            self.image = np.zeros((self.rows, self.cols, 3), dtype=np.uint8)
            for ir, r in enumerate(self.image):
                for ic, c in enumerate(r):
                    self.image[ir, ic] = bg(ir, ic)
            for c in board.obstacles:
                self.image[c] = col_obs
                self.save[c] = col_obs
            self.image[board.goal] = col_dest
            self.save[board.goal] = col_dest
        if board.agent:
            old = bg(self.agent[0], self.agent[1])
            if self.agent in self.save:
                old = self.save[self.agent]
            self.image[self.agent] = old
            self.image[board.agent.state[0], board.agent.state[1]] = [255, 40, 0]
            self.agent = tuple(board.agent.state)
        for c in board.path:
            self.image[c] = col_path
            self.save[c] = col_path

        if self.local:
            import cv2
            ratio = (self.image.shape[1]) / (self.image.shape[0])
            dims = (int(333*ratio), 333)
            img = cv2.cvtColor(self.image, cv2.COLOR_RGB2BGR)
            resized = cv2.resize(img, dims, interpolation=cv2.INTER_NEAREST)
            cv2.imshow('Board', resized)
            cv2.waitKey(1)
            return

        display.clear_output(wait=True)
        plt.imshow(self.image, interpolation='none')
        plt.text(0, -1, text)
        plt.pause(.0001)


display.clear_output(wait=True)

