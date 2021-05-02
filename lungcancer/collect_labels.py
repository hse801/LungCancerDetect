import os
import glob
import shutil

os.chdir('E:/HSE/LungCancerDetect/data/images/')
dst = 'E:/HSE/LungCancerDetect/data/labels/transverse/train/'

with open('train_transverse_labels.txt', 'r') as f:
    lines = f.readlines()
    lines = list(map(lambda s: s.strip(), lines))

for l in lines:
    print(l)
    shutil.copy2(l, dst)
