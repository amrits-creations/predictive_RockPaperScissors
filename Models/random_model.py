import random


class RandomModel:
    name = "Random Baseline"

    def predict(self, history):
        return random.randint(0, 2)
