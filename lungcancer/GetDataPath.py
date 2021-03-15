import os
import glob
import pickle

# train / test 할 이미지의 경로들을 각각 txt 파일에 저장
# train.txt / test.txt

# file_list = os.listdir('E:\\HSE\\LungCancerSegmentation\\PyTorch-YOLOv3\\data\\images')
# file_list = glob.glob('E:/HSE/PyTorch-YOLOv3/wholepetct/images/valid/*/PET*slice*.npy')
# file_list = glob.glob('E:/HSE/2dtempdata/*/*slice*.txt')
# file_list = glob.glob('E:/HSE/PyTorch-YOLOv3_default/data/dumbbell/images/*.jpg')
# file_list = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/CT_PET_*.jpg')
file_list = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/CT_PET_*.jpg')

print('type = ', type(file_list))
print('len = ', len(file_list))
# print('file list = ', file_list)

# os.chdir('E:/HSE/LungCancer/yolov3/data/images/')
os.chdir('E:/HSE/LungCancerDetect/data/images/')
f = open('ct_pet_test.txt', 'w')
for ele in file_list:
    f.write(ele + '\n')
f.close()

# print(file_list2)