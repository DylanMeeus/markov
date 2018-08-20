import numpy as np
import random

class markov:
    def __init__(self):
        cols = 2
        rows = 2
        self.matrix = [[0 for x in range(cols)] for y in range(rows)] 
        self.matrix[0][0] = 0.3
        self.matrix[0][1] = 0.7
        self.matrix[1][0] = 0.5 
        self.matrix[1][1] = 0.5

    def run(self):
        state = 0
        for i in range(100):
            print(" S " if state == 0 else " R ")
            r = random.random()
            sum_opt = 0
            for index, option in enumerate(self.matrix[state]):
                sum_opt += option
                if r < sum_opt:
                    # we have reached a state that matches our random number so we assign it
                    state = index
                    break
                    



    


if __name__ == '__main__':
    m = markov()
    m.run()
