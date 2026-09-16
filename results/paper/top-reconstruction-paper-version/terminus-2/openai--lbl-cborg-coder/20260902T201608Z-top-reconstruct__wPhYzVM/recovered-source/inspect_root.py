import uproot

file = uproot.open('/root/data/ttbar.root')
tree = file['output']
print('Branches:', tree.keys())

data = tree.arrays(["Number", "N_genjet", "genjet_pt", "genjet_eta", "genjet_phi"], entry_stop=5)
print('\nSample Data:')
print(data)

for i in range(4):
    branch = f'truth_triplet_{i}'
    if branch in tree.keys():
        print(f'\n{branch} sample: {tree[branch].array(entry_stop=5)}')
