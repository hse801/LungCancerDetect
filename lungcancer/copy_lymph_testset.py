# Data 폴더의 lymph node roi 파일 복사하기
# shutil 모듈 이용
# 생성된 RoiVolume 폴더 안에서 roi 파일들 꺼내오기

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
        os.chdir('E:/HSE/LungCancerDetect/data/testset/' + fName)
        dst_path = 'E:/HSE/LungCancerDetect/data/testset/' + fName
        lymph_roi_list = os.listdir('C:/Users/Bohye/data/' + fName + '/RoiVolume/')
        print('lymph roi list = ', lymph_roi_list)
        for f in lymph_roi_list:
            file_to_copy = 'C:/Users/Bohye/data/' + fName + '/RoiVolume/' + f
            print('file to copy = ', file_to_copy)
            shutil.copy2(file_to_copy, dst_path)


dstPath = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/')
roiPath = glob.glob('C:/Users/Bohye/data/*/RoiVolume/')
patient_list = []

for i in dstPath:
    dst_patient_num = i.split(os.sep)[-2]
    patient_list.append(dst_patient_num)

for i in roiPath:
    CopyLymph(i, patient_list)