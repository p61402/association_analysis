import pandas as pd
from mlxtend.frequent_patterns import association_rules
dict = {'itemsets': [['177', '176'], ['177', '179'],
                     ['176', '178'], ['176', '179'],
                     ['93', '100'], ['177', '178'],
                     ['177', '176', '178']],
        'support': [0.253623, 0.253623, 0.217391,
                    0.217391, 0.181159, 0.108696, 0.108696]}

freq_itemsets = pd.DataFrame(dict)
print(freq_itemsets)

res = association_rules(freq_itemsets, support_only=True, min_threshold=0.1)
print(res)
