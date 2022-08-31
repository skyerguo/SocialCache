a = {}
a['5'] = {'b': 1, 'c': 2}
a['6'] = {'b': 1, 'c': 2, 'd': 3}
print(a)
print(len(a['6']))
del a['5']['b']
print(a)