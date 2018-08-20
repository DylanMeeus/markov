import numpy as np
import random


class token:
    def __init__(self, token):
        self.token = token
        # dictionary of next-tokens + the odds they appear


class trainer:
    def __init__(self):
        # dictionary of a token with a list of all things after it
        self.tokens = {}

    def train(self, line: '[String]'):
        # collect all possible states
        # record all the transitions
        parts = line.split(" ") # simple tokenizer

        # add a start token
        if "START" in self.tokens:
            self.tokens["START"].append(parts[0])
        else:
            self.tokens["START"] = [parts[0]]
        for i in range(len(parts)):
            next_token = "EOL" if i + 1 == len(parts) else parts[i+1]
            if parts[i] in self.tokens:
                self.tokens[parts[i]].append(next_token)
            else:
                self.tokens[parts[i]] = [next_token]



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
    trainer = trainer()
    trainer.train("this is a test for parsing a sentence.")
    print(trainer.tokens)
