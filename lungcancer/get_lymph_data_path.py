import os
import glob
import pickle

# train / test 할 이미지의 경로들을 각각 txt 파일에 저장
# train.txt / test.txt

# file_list = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/CT_PET_*.npy')
# file_list = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/CT_PET_*.jpg')
file_list = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/CT_PET_*.jpg')
# file_list = glob.glob('E:/HSE/LungCancerDetect/data/imags/valid/*/CT_PET_*.jpg')
# file_list = glob.glob('E:/HSE/LungCancerDetect/one/23835418/')

print('type = ', type(file_list))
print('len = ', len(file_list))
# print('file list = ', file_list)

# os.chdir('E:/HSE/LungCancer/yolov3/data/images/')
os.chdir('E:/HSE/LungCancerDetect/data/images/')
f = open('lymph_valid_img.txt', 'w')
for ele in file_list:
    label_list = ele.replace('jpg', 'txt')
    if os.path.getsize(label_list) != 0:
        f.write(ele + '\n')
f.close()

# print(file_list2)