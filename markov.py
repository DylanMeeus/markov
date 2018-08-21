import random
import json
from datetime import datetime
from hnapi import HnApi 


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
            self.tokens["EOL"] = []
        for i in range(len(parts)):
            next_token = "EOL" if i + 1 >= len(parts) else parts[i+1]
            if parts[i] in self.tokens:
                self.tokens[parts[i]].append(next_token)
            else:
                self.tokens[parts[i]] = [next_token]

    def sanitize(self):
        # remove bad entries (like spaces)
        for token in self.tokens:
            no_space_tokens = list(filter(lambda t: t != "", self.tokens[token]))
            self.tokens[token] = no_space_tokens


    def transform_matrix(self) -> '[float][float]':
        self.sanitize()
        # turn our tokens into a matrix for the markov chain
        matrix = [[None for x in range(len(self.tokens))] for y in range(len(self.tokens))] 
        for row, token in enumerate(self.tokens):
            for column, other_token in enumerate(self.tokens):
                # count the percentage of 'other_token' in token
                successor_count = len(self.tokens[token])
                matching_count = len(list(filter(lambda t: t == other_token, self.tokens[token])))
                matrix[row][column] = matching_count / successor_count if successor_count != 0 else 0
        return matrix
        



    def save_state(self):
        # write the list of tokens to an easy to parse TSV
        f = open("state.json", "w+")
        f.write(json.dumps(self.tokens, ensure_ascii=False, indent=4))

    def read_state(self):
        f = open("state.json", "r")
        self.tokens = json.load(f)
        




class markov:
    def __init__(self, tokens, matrix):
        self.tokens = tokens
        self.matrix = matrix
        # determine initial state


    def run(self) -> 'String':
        state = 0
        sentence = ""
        words = list(self.tokens.keys())
        while words[state] != "EOL":
            if words[state] != "START":
                sentence += words[state] + " "
            random.seed(datetime.now())
            r = random.random()
            sum_opt = 0
            for index, option in enumerate(self.matrix[state]):
                sum_opt += option
                if r < sum_opt:
                    # we have reached a state that matches our random number so we assign it
                    state = index
                    break
                    
        return sentence



def get_hackernews_stories():
    con = HnApi()
    stories = []
    limit = 10000
    for i in range(1,limit):
        print("parsing story: " + str(i) + " of " + str(limit))
        try:
            item = con.get_item(i)
            title = item.get('title')
            stories.append(title)
        except:
            pass
    return stories


if __name__ == '__main__':
    input("generate?")
    trainer = trainer()
    #stories = get_hackernews_stories()
    #for story in stories:
    #    trainer.train(story)
    #trainer.save_state()
    trainer.read_state()
    matrix = trainer.transform_matrix()
    markov = markov(trainer.tokens, matrix)
    while True:
        for i in range(5):
            print(markov.run())
        input("")
