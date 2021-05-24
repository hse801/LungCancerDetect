import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import seaborn as sns

size_list = []


def cancer_size(fold_list):

    label_list = glob.glob(fold_list + '/*_conv_*.txt')
    print(f'label_list = {label_list}')
    targets = []
    for label in label_list:
        if os.path.isfile(label):
            labels = open(label, 'r')
            label_lines = labels.readlines()
            for l in label_lines:
                target = list(map(float, l.rstrip().split(' ')))
                # size 160*128*2.43*2.43 = 120932.352
                # 단위 mm^2
                size = target[3] * target[4] * 120932.352
                size_list.append(size)
                print(f'size = {size}, size len = {len(size_list)}')
                print(f'target[3] = {target[3]}, target[4] = {target[4]}')
                targets.append(list(target))
                print(f'targets = {targets}')
                print(f'type = {type(targets)}, len = {len(targets)}')
            # print(targets[1])
        # return np.array(targets)


def plot_size(size_list):
    # hist = plt.hist()
    plt.hist(size_list, range=[0, 0.1])
    # sns.distplot(size_list)
    plt.show()

foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/test/*/')
count = 0

for i in foldList:
    cancer_size(i)
    # get_labels(i)
    # break
    count += 1
    print('count = ', count)

plot_size(size_list)