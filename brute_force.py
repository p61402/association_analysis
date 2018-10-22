import pandas as pd
import numpy as np
from itertools import combinations
import preprocess


class brute_force():
    def __init__(self, min_sup=20, num_of_items=10, num_of_transactions=101):
        self.num_of_items = num_of_items
        self.num_of_transactions = num_of_transactions
        self.df = preprocess.generate_dataframe()
        self.min_sup = min_sup
        self.current_itemset = set([(i, ) for i in range(num_of_items)])
        self.freq_itemset = []
        self.correspond_sup = []
        self.pattern_length = 1

    def brute_force(self):
        while len(self.current_itemset) > 1:
            self.update()

    def update(self):
        new_freq_itemset = set()
        self.pattern_length += 1
        for pattern in combinations(range(self.num_of_items), self.pattern_length):
            if (self.support(pattern) >= self.min_sup):
                new_freq_itemset.add(pattern)
        self.current_itemset = new_freq_itemset
        for item in self.current_itemset:
            self.freq_itemset.append(item)
            self.correspond_sup.append(self.support(item) / (self.num_of_transactions))

    def support(self, pattern):
        sup_count = 0
        for _, row in self.df.iterrows():
            match = True
            for i in pattern:
                if row[i] != 1:
                    match = False
                    break
            if match:
                sup_count += 1
        return sup_count
