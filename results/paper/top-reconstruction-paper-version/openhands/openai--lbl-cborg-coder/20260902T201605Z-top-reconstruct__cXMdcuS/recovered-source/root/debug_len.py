import uproot
import pandas as pd
file = uproot.open("/root/data/ttbar.root")
tree = file["output;1"]
data = tree.arrays(["Number"], library="pd")
print(f"Len of data: {len(data)}")
