# Data 폴더의 lymph node roi 폴더 복사하기
# shutil 모듈 이용
# file from roi_path copied to dst_path
# paste folder named RoiVolume_cut

import os
import glob

# from tqdm import tqdm_notebook
from tqdm.notebook import tqdm
import shutil


def CopyLymph(roi_path, patient_list):
    lymph_roi_path = roi_path
    roi_patient_num = lymph_roi_path.split(os.sep)[-3]
    dst_list = patient_list

    if roi_patient_num in dst_list:
        fName = roi_patient_num
        os.chdir('E:/HSE/LungCancerDetect/data/images/valid/' + fName)
        shutil.copytree(lymph_roi_path, 'RoiVolume_cut')
        print('filed copied from ', lymph_roi_path)


# dstPath = glob.glob('E:/HSE/LungDataPlus_Cdrive/*/')
# roiPath = glob.glob('C:/Users/Bohye/data/*/RoiVolume/')
dstPath = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')
roiPath = glob.glob('E:/HSE/lymphdata/*/RoiVolume_cut/')
patient_list = []
count = 0

for i in dstPath:
    dst_patient_num = i.split(os.sep)[-2]
    print('patient num = ', dst_patient_num)
    patient_list.append(dst_patient_num)
    count += 1
print('total count = ', count)
for i in roiPath:
    CopyLymph(i, patient_list)
    # print('i = ', i)