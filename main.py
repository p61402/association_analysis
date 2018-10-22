import brute_force as bf
import apriori as ap
import fp_growth as fp
import preprocess
from itertools import combinations
import pandas as pd
from mlxtend.frequent_patterns import association_rules
import sys, getopt


def main(argv):
    mode = None
    try:
        opts, args = getopt.getopt(argv[1:], "m:")
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-m':
            mode = arg
    
    if mode == 'bf':
        run_brute_force()
    elif mode == 'ap':
        run_apriori()
    elif mode == 'fp':
        run_fp_growth()

def run_brute_force():
    instance1 = bf.brute_force(min_sup=70, num_of_items=10, num_of_transactions=97)
    instance1.brute_force()
    d = {}
    d['itemsets'] = instance1.freq_itemset
    d['support'] = instance1.correspond_sup
    freq_itemsets = pd.DataFrame(d)
    res = association_rules(freq_itemsets, support_only=True, min_threshold=0.1)
    res = res[['antecedents', 'consequents', 'support']]
    print(res)
    
def run_apriori():
    instance2 = ap.apriori(min_sup=70, num_of_items=10, num_of_transactions=97)
    instance2.apriori()
    d = {}
    d['itemsets'] = instance2.freq_itemset
    d['support'] = instance2.correspond_sup
    freq_itemsets = pd.DataFrame(d)
    res = association_rules(freq_itemsets, support_only=True, min_threshold=0.1)
    res = res[['antecedents', 'consequents', 'support']]
    print(res)

def run_fp_growth():
    df = preprocess.generate_dataframe()
    transactions = []
    for _, row in df.iterrows():
        l = []
        for key in list(df):
            if row[key]:
                l.append(key)
        transactions.append(l)
    
    instance3 = fp.fp_tree(20)
    instance3.build_freq_items(transactions)
    instance3.build_fp_tree(transactions)
    freq_itemset = set()
    fp.mine_tree(instance3, freq_itemset)
    print(freq_itemset)


if __name__=='__main__':
    main(sys.argv)