import os
import glob


def check_file(file_path):
    if os.path.isdir(file_path + '/RoiVolume_cut'):
        # print('RoiVolume_cut exists')
        lymph_list = os.listdir(file_path + '/RoiVolume_cut')
        # print(f'lymph list = {lymph_list}')
        if len(lymph_list) == 0:
            print(f'Lymph list is empty')
            print(file_path)


file_path = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/')
# file_path = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
# file_path = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')

for i in file_path:
    check_file(i)
