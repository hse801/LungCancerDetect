# Data 폴더의 lymph node roi 파일 복사하기
# shutil 모듈 이용

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
        os.chdir('E:/HSE/LungData_Cdrive/' + fName)
        shutil.copytree(lymph_roi_path, 'RoiVolume')


dstPath = glob.glob('E:/HSE/LungData_Cdrive/*/')
roiPath = glob.glob('C:/Users/Bohye/data/*/RoiVolume/')
patient_list = []

for i in tqdm(dstPath):
    dst_patient_num = i.split(os.sep)[-2]
    patient_list.append(dst_patient_num)

for i in tqdm(roiPath):
    CopyLymph(i, patient_list)