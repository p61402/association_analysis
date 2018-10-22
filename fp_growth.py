import pandas as pd
import itertools
import preprocess
import itertools
from collections import OrderedDict

class tree_node():
    def __init__(self, name, freq=0, parent=None):
        self.name = name
        self.freq= freq
        self.parent = parent
        self.children = {}
        self.link = None

class fp_tree():
    def __init__(self, min_sup):
        self.root = tree_node("root", 100000000000)
        self.min_sup = min_sup
        self.freq_item_count = {}
        self.header_table = {}

    def build_freq_items(self, transactions):
        for transaction in transactions:
            for item in transaction:
                self.freq_item_count[item] = self.freq_item_count.get(item, 0) + 1

        for key in list(self.freq_item_count):
            if self.freq_item_count[key] < self.min_sup:
                del self.freq_item_count[key]

    def build_fp_tree(self, transactions):
        for transaction in transactions:
            sorted_transaction = []
            for item in transaction:
                if item in self.freq_item_count:
                    sorted_transaction.append(item)
            sorted_transaction.sort(key=lambda k: self.freq_item_count[k], reverse=True)
            self.update_tree(sorted_transaction)

    def update_tree(self, transaction):
        current_node = self.root
        for item in transaction:
            if item in current_node.children:
                current_node.children[item].freq += 1
            else:
                current_node.children[item] = tree_node(item, 1, current_node)
                if item in self.header_table:
                    node = self.header_table[item]
                    while node.link:
                        node = node.link
                    node.link = current_node.children[item]
                else:
                    self.header_table[item] = current_node.children[item]
            current_node = current_node.children[item]

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
            for child in node.children.values():
                self.path_helper(child)
            path.pop()
    
    def find_prefix_path(self, base_pattern):
        conditional_pattrns = []
        counts = []
        node = self.header_table[base_pattern]
        while node:
            prefix_path = []
            self.ascend_tree(node, prefix_path)
            if prefix_path:
                conditional_pattrns.append(prefix_path[::-1][:-1])
                counts.append(node.freq)
            node = node.link
        return zip(conditional_pattrns, counts)

    def ascend_tree(self, node, prefix_path):
        if node.parent:
            prefix_path.append(node.name)
            self.ascend_tree(node.parent, prefix_path)
    
    def only_single_path(self, node):
        if len(node.children) > 1:
            return False
        elif len(node.children) == 0:
            return True
        else:
            return self.only_single_path(node.children[list(node.children)[0]])

    def generate_patterns(self):
        patterns = {}
        supports = {}
        s = set()
        node = self.root
        while node.children:
            if node.name != "root":
                s.add(node.name)
            supports[node.name] = node.freq
            node = node.children[list(node.children)[0]]
        
        for l in range(2, len(s) + 1):
            for pattern in list(itertools.combinations(s, l)):
                patterns[pattern] = min([supports[item] for item in pattern])

        return patterns

def mine_tree(tree, freq_itemset):
    if tree.only_single_path(tree.root):
        patterns = tree.generate_patterns()
        for pattern, support in patterns.items():
            if support >= tree.min_sup:
                freq_itemset.add(pattern)
    else:
        for node in list(tree.header_table.values())[::-1]:
            transactions = []
            patterns = tree.find_prefix_path(node.name)
            for pattern, count in patterns:
                for _ in range(count):
                    transactions.append(pattern)
            subtree = fp_tree(tree.min_sup)
            subtree.build_freq_items(transactions)
            subtree.build_fp_tree(transactions)
            if len(subtree.root.children) != 0:
                mine_tree(subtree, freq_itemset)