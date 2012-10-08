from collections import defaultdict
import random
import re
import os.path


def clean_punctuation(string):
    """
    >>> clean_punctuation('Hello , world ! how ? you : doing ;')
    'Hello, world! how? you: doing;'
    >>> clean_punctuation('you , , would')
    'you, would'
    """
    return re.sub(r' ([,\.\?;:!])(?: [,\.\?;:!])?', r'\1', string)


class MarkovGenerator(object):
    def __init__(self, corpus, token_size=2):
        self.current = tuple()
        self.token_size = token_size

        self.tokens = self.tokenize(corpus)
        self.graph = self.analyze(self.tokens)

    def analyze(self, tokens):
        graph = defaultdict(list)

        for i, token in enumerate(tokens):
            graph[tuple(tokens[i - self.token_size:i])].append(token)

        return graph

    def tokenize(self, corpus):
        return corpus.split(' ')

    def word(self):
        self.current = self.current[1:], random.choice(
            self.graph.get(self.current, self.tokens)
        )

        return self.current[-1]

    def sentence(self):
        current = None
        words = []

        while current != '.':
            current = self.word()
            words.append(current)

        return clean_punctuation(' '.join(words))


shakespeare_path = os.path.join(os.path.dirname(__file__), '..', 'content', 'shakespeare.txt')

with open(shakespeare_path) as f:
    shakespeare = MarkovGenerator(f.read(), 7)
