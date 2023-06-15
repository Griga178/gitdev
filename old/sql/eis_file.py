'''
объединение множеств в одно (из eis)
'''

import pickle

a = 'contra/pkl_'
b = '.pkl'
numersss = set()
for el in range(42):

    with open(a + str(el) + b, 'rb') as f:
        pickle_set = pickle.load(f)
        numersss |= pickle_set


numersss

with open('contra/2021kontr9.pkl', 'wb') as f:
    pickle.dump(numersss, f, pickle.HIGHEST_PROTOCOL)
    print(f'Всего: {len(numersss)} номеров')
