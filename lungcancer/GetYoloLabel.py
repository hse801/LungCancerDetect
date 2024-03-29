#import module
import matplotlib as mpl
import matplotlib.pylab as plt

#from torch.utils.tensorboard import SummaryWriter

from scipy.interpolate import interpn

from torch.optim import lr_scheduler

import sys
import os
import glob

#from tqdm import tqdm_notebook
from tqdm.notebook import tqdm

import numpy as np


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import SimpleITK as sitk


# 2d data labeling을 위해 각 roi 영역의 xcenter, ycenter, w, h를 txt 파일로 저장


def GetYoloLabel(fPath):
    # ct_list = glob.glob(fPath + 'CT_Cut.nii.gz')
    roiList = glob.glob(fPath + 'ROI_cut.nii.gz')
    #     lymphList = glob.glob(fPath + '*nestle_cut.nii.gz')

    # img_ct = sitk.ReadImage(ct_list[0])
    # img_ct_data = sitk.GetArrayFromImage(img_ct)
    # img_pet = sitk.ReadImage(pet_list[0])
    # img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_roi = sitk.ReadImage(roiList[0])
    img_roi_data = sitk.GetArrayFromImage(img_roi)
    # print('img idx = ', np.shape(img_roi_data))
    # print('img idx 0 = ', np.shape(img_roi_data[0]))

    # print('roi shape = ', np.shape(img_roi_data))
    #     print(img_roi_data[50,50,:])
    nzero = img_roi_data.nonzero()
    # print('nzero = ',nzero)
    # print('nzero shape = ', np.shape(nzero))
    # print('nonzero z index = ', nzero[0])
    new_nzero_z = []
    for i in nzero[0]:
        if i not in new_nzero_z:
            new_nzero_z.append(i)
    print('new nonzero = ', new_nzero_z)

    start_idx = new_nzero_z[0]
    end_idx = new_nzero_z[-1]

    print('start idx = ', start_idx)
    print('end idx = ', end_idx)

    z_count = 0

    for i in range(np.shape(img_roi_data)[0]):
        if start_idx > i or end_idx < i:
            os.chdir(fPath)
            num = '{0:0>3}'.format(i)
            with open("CT_PET_slice" + str(num) + ".txt", "w") as f:
                pass
        # if start_idx <= i <= end_idx:
        #     roi_zslice = img_roi_data[i, :, :]
        #     # print('i1 = ', i)
        #     nzero = roi_zslice.nonzero()
        #     print('nzero = ', nzero)
        #     new_nzero_x = []
        #     new_nzero_y = []
        #     for j in nzero[1]:
        #         if j not in new_nzero_x:
        #             new_nzero_x.append(j)
        #     for k in nzero[0]:
        #         if k not in new_nzero_y:
        #             new_nzero_y.append(k)
        #     z_count += 1
        #     # normalize with image width and height (160x128)
        #
        #     centerX = ((min(new_nzero_x) + max(new_nzero_x)) / 2)/160
        #     centerY = 1 - (((min(new_nzero_y) + max(new_nzero_y)) / 2)/128)
        #     # centerY = 1 - centerY
        #     w = (max(new_nzero_x) - min(new_nzero_x))/160
        #     h = (max(new_nzero_y) - min(new_nzero_y))/128
        #
        #     # print('center X = ', centerX)
        #     # print('certerY = ', centerY)
        #     # print('w = ', w)
        #     # print('h = ', h)
        #     # print('i = ', i)
        #     os.chdir(fPath)
        #     num = '{0:0>3}'.format(i)
        #     print('num = ', num)
        #
        #     with open("CT_PET_slice" + str(num) + ".txt", "w") as f:
        #         f.write("0 " + str(centerX) + " ")
        #         f.write(str(centerY) + " ")
        #         f.write(str(w) + " ")
        #         f.write(str(h) + " ")
            # with open("CT-cut-slice" + str(num) + ".txt", "w") as f:
            #     f.write("0 " + str(centerX) + " ")
            #     f.write(str(centerY) + " ")
            #     f.write(str(w) + " ")
            #     f.write(str(h) + " ")
            # with open("PET-cut-slice" + str(num) + ".txt", "w") as f:
            #     f.write("0 " + str(centerX) + " ")
            #     f.write(str(centerY) + " ")
            #     f.write(str(w) + " ")
            #     f.write(str(h) + " ")
        # roi에 해당하지 않는 z 인덱스의 경우 label 없는 빈 txt 파일 생성
        # else:
        #     os.chdir(fPath)
        #     num = '{0:0>3}'.format(i)
        #     with open("CT-cut-slice" + str(num) + ".txt", "w") as f:
        #         pass


# foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/temp/images/test/*/')
# foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/wholedata/images/train/*/')
# foldList = glob.glob('E:/HSE/LungCancer/yolov3/data/images/train/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/')
foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
count = 0

for i in foldList:
    GetYoloLabel(i)
    count += 1
    print('count = ', count)

