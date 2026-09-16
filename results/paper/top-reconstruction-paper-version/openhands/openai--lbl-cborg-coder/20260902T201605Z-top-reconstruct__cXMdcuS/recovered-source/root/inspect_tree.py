import uproot
file = uproot.open("/root/data/ttbar.root")
tree = file["output;1"]
print(tree.show())
