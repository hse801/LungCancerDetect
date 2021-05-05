import os
import glob
import shutil

os.chdir('E:/HSE/LungCancerDetect/data/images/')
dst = 'E:/HSE/LungCancerDetect/data/labels/transverse/train/'

with open('train_ours.txt', 'r') as f:
    lines = f.readlines()
    lines = list(map(lambda s: s.strip(), lines))

for l in lines:
    # os.remove(l)
    # print(l)
    l = l.replace('jpg', 'txt')
    shutil.copy2(l, dst)
    print(f'copy {l} to {dst}')