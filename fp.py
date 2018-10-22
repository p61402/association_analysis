import pandas as pd
import itertools
import preprocess
import itertools
from collections import OrderedDict

class tree_node():
    def __init__(self, name, freq):
        self.set_detail(name, freq)
        self.parent = None
        self.children = []

    def set_detail(self, name, freq):
        self.name = name
        self.freq = freq

    def set_parent(self, node):
        self.parent = node

    def add_child(self, node):
        self.children.append(node)

class fp_tree():
    def __init__(self):
        self.root = tree_node("root", None)
        self.header_table = {}
        self.freq_items = {}

    def add_path(self, pattern):
        current_node = self.root
        for item in pattern:
            for child in current_node.children:
                if item == child.name:
                    child.freq += 1
                    current_node = child
                    break
            else:
                new_node = tree_node(item, 1)
                new_node.set_parent(current_node)
                current_node.add_child(new_node)
                if new_node.name in self.header_table:
                    self.header_table[new_node.name].append(new_node)
                else:
                    self.header_table[new_node.name] = []
                    self.header_table[new_node.name].append(new_node)
                current_node  = new_node

    def build_freq_items(self, transactions):
        for transaction in transactions:
            for item in transaction:
                if item in self.freq_items:
                    self.freq_items[item] += 1
                else:
                    self.freq_items[item] = 1

    def get_paths(self):
        self.all_paths = []
        self.path_helper(self.root)
        return self.all_paths

    def path_helper(self, node, path=[]):
        path.append((node.name, node.freq))
        if len(node.children) == 0:
            self.all_paths.append([(n[0], n[1]) for n in path])
            path.pop()
        else:
            for child in node.children:
                self.path_helper(child)
            path.pop()

    def find_prefix_path(self, node_name):
        conditional_patterns = []
        for node in self.header_table[node_name]:
            prefix_path = []
            self.backward(node, prefix_path)
            if len(prefix_path) > 1:
                conditional_patterns.append(tuple(prefix_path[1:])[::-1])
        return conditional_patterns

    def backward(self, node, prefix_path):
        if node.parent:
            prefix_path.append(node.name)
            self.backward(node.parent, prefix_path)
    
    def only_single_path(self, node):
        if len(node.children) > 1:
            return False
        elif len(node.children) == 0:
            return True
        else:
            return self.only_single_path(node.children[0])

    def generate_patterns(self):
        patterns = []
        s = set()
        node = self.root
        while node.children:
            s.add(node.name)
            node = node.children[0]
        
        for l in range(2, len(s) + 1):
            for pattern in list(itertools.combinations(s, l)):
                patterns.append(pattern)

        return patterns

class fp_growth():
    def __init__(self, min_sup=0.6, num_of_items=10, num_of_transactions=101):
        self.num_of_items = num_of_items
        self.num_of_transactions = num_of_transactions
        self.df = preprocess.generate_dataframe()
        self.min_sup = min_sup
        self.items = [(item, ) for item in range(self.num_of_items)]
        self.freq_one_item_dict = OrderedDict()
        self.sorted_transactions = []
        self.freq_itemset = []

    def fp_growth(self):
        self.build_one_item_dict()
        transactions = []
        for _, row in self.df.iterrows():
            l = []
            for col in list(self.df):
                if row[col] and col in self.freq_one_item_dict:
                    l.append(col)
            if l:
                transactions.append(tuple(sorted(l, key=lambda x: self.freq_one_item_dict[x], reverse=True)))
        self.sorted_transactions = transactions
        self.build_fp_tree()

    def build_one_item_dict(self):
        freq_one_itemset = [item for item in self.items if self.support(item) >= self.min_sup]
        self.freq_one_item_dict = {item[0]: self.support(item) for item in freq_one_itemset}
        self.freq_one_item_dict = OrderedDict(sorted(self.freq_one_item_dict.items(), key=lambda t: t[1], reverse=True))

    def build_fp_tree(self):
        tree = fp_tree()
        tree.build_freq_items(self.sorted_transactions)
        for transaction in self.sorted_transactions:
            tree.add_path(transaction)
        
        paths = tree.get_paths()
        for path in paths:
            for n in path[:-1]:
                print("{}({})".format(n[0], n[1]), end='-> ')
            print("{}({})".format(path[-1][0], path[-1][1]))

        self.freq_itemset = sorted(self.freq_itemset, key=lambda k: len(k))
        # for i in range(2, 9):
        #     c = 0
        #     for item in self.freq_itemset:
        #         if len(item) == i:
        #             c += 1
        #     print(i, c)
        # print(self.freq_itemset)
        self.mine(tree)
        print(self.freq_itemset)

    def mine(self, tree):
        if tree.only_single_path(tree.root):
            self.freq_itemset.append(tree.generate_patterns())
        else:
            self.mining_tree(tree)

    def mining_tree(self, tree):
        mining_order = sorted(tree.freq_items.keys(), key=lambda k: tree.freq_items[k])
        print(mining_order)

        for item in mining_order:
            paths = tree.find_prefix_path(item)
            conditional_tree_input = []
            for path in paths:
                conditional_tree_input.append(path)
            print(conditional_tree_input)
            subtree = fp_tree()
            subtree.build_freq_items(conditional_tree_input)
            print(subtree.freq_items)
            self.items = [tuple(item, ) for item in subtree.freq_items]
            self.build_one_item_dict()
            self.sorted_transactions = []
            for transaction in conditional_tree_input:
                l = []
                for item in transaction:
                    if item in self.freq_one_item_dict:
                        l.append(item)
                self.sorted_transactions.append(tuple(sorted(l, key=lambda x: self.freq_one_item_dict[x], reverse=True)))
            print(self.sorted_transactions)
            for transaction in conditional_tree_input:
                subtree.add_path(self.sorted_transactions)

            self.mine(subtree)

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
        return sup_count / self.num_of_transactions