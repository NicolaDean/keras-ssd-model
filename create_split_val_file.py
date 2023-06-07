import os
import tqdm
dirs = os.listdir('./train')

files = []
for filename in tqdm.tqdm(dirs, desc='dirs') :
  name = os.path.basename(filename)
  name = filename.split('.')
  name.pop()
  name = '.'.join(name)
  files.append(name)

set_res = set(files)
files   = list(files)

size = len(files)
train_split = 0.8


train_size = int(size * train_split)
print(train_size)
train = files[:train_size]
valid = files[train_size:]

print(train)
print(valid)
        
with open(os.path.join('./', "train_split_file.txt"), "w") as trainval_split_file:
  for f in train:
    trainval_split_file.write(f"{f}.jpg {f}.xml\n")

with open(os.path.join('./', "val_split_file.txt"), "w") as trainval_split_file:
  for f in valid:
    trainval_split_file.write(f"{f}.jpg {f}.xml\n")