import os
import glob
import numpy as np
import SimpleITK as sitk


def get_depth(file_path):
    ct_list = glob.glob(file_path + 'CT_cut.nii.gz')
    img_ct = sitk.ReadImage(ct_list[0])
    depth = img_ct.GetDepth()
    print(f'depth = {depth}')
    print(f'depth type = {type(depth)}')


file_path = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/')
# img_path = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
# img_path = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')

for i in file_path:
    get_depth(i)
