import pandas as pd
import itertools
import preprocess


class apriori():
    def __init__(self, min_sup=3, num_of_items=10, num_of_transactions=100):
        self.num_of_items = num_of_items
        self.num_of_transactions = num_of_transactions
        self.df = preprocess.generate_dataframe()
        self.min_sup = min_sup
        self.current_itemset = set([(i, ) for i in range(num_of_items)])
        self.freq_itemset = []
        self.correspond_sup = []
        self.pattern_length = 0

    def apriori(self):
        while (len(self.current_itemset) > 1):
            self.generate()
            for item in self.current_itemset:
                self.freq_itemset.append(item)
                self.correspond_sup.append(self.support(item) / self.num_of_transactions)

    def generate(self):
        item_set = self.self_join()
        self.prune(item_set)

    def self_join(self):
        x = y = list(self.current_itemset)
        temp_itemset = []
        for i in range(len(x)):
            for j in range(i, len(y)):
                except_last_term = all([a == b for a, b in zip(x[i][:-1], y[j][:-1])])
                if except_last_term and x[i][-1] != y[j][-1]:
                    new_pattern = x[i] + (y[j][-1], )
                    if self.support(new_pattern) >= self.min_sup:
                        temp_itemset.append(new_pattern)
        return temp_itemset

    def prune(self, item_set):
        new_freq_itemset = set()
        for item in item_set:
            sub_items = set(itertools.combinations(item, len(item) - 1))
            is_all_sub_items_in_freq_itemset = all([sub_item for sub_item in sub_items if sub_item in self.current_itemset])
            if is_all_sub_items_in_freq_itemset:
                new_freq_itemset.add(item)
        self.current_itemset = new_freq_itemset

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