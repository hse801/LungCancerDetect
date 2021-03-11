# convert nii file into image file
# to use as input for yolov3
# make ct, pet file into one image
# use either 2 channel of ct, 1 channel of pet OR 1 channel of ct, 2 channel of pet

import SimpleITK as sitk
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


def nifti_convert(fPath):
    ct_file  = fPath + 'CT_cut.nii.gz'
    pet_file = fPath + 'PET_cut.nii.gz'
    roi_file = fPath + 'ROI_cut.nii.gz'
    # path of txt files that contain mean, std
    data_file = fPath + 'img_data.txt'

    # get mean, std values to standardization
    f = open(data_file, 'r')
    nums = [float(x) for x in f.read().split()]
    f.close()
    img_ct = sitk.ReadImage(ct_file)
    img_ct_data = sitk.GetArrayFromImage(img_ct)
    img_ct_data[img_ct_data > 500] = 500
    # standardization
    img_ct_data = (img_ct_data - nums[0]) / (nums[1] + 1e-8)
    ct_rgb_data = ((img_ct_data - img_ct_data.min()) / (img_ct_data.max() - img_ct_data.min()) * 255).astype(np.uint8)
    ct_rgb_data = ct_rgb_data[:, ::-1, :]
    img_pet = sitk.ReadImage(pet_file)
    img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_pet_data = (img_pet_data - nums[2]) / (nums[3] + 1e-8)
    pet_rgb_data = ((img_pet_data - img_pet_data.min()) / (img_pet_data.max() - img_pet_data.min()) * 255).astype(np.uint8)
    pet_rgb_data = pet_rgb_data[:, ::-1, :]
    img_roi = sitk.ReadImage(roi_file)
    img_roi_data = sitk.GetArrayFromImage(img_roi)

    nzero = img_roi_data.nonzero()
    new_nzero = []
    for i in nzero[0]:
        if i not in new_nzero:
            new_nzero.append(i)

    start_idx = new_nzero[0]
    end_idx = new_nzero[-1]

    # j = start_idx
    for j in range(start_idx, end_idx + 1):
        num = '{0:0>3}'.format(j)
        os.chdir(fPath)
        ct_slice = ct_rgb_data[j, :, :]
        pet_slice = pet_rgb_data[j, :, :]
        data = np.stack((ct_slice, ct_slice, pet_slice), axis=-1)
        img = Image.fromarray(data, 'RGB')
        filename = 'CT_PET_slice' + num + '.jpg'
        img.save(filename)
        print(filename, ' saved')

        # load_pet = np.load(fPath + 'PET-cut-slice' + num +'.npy')
        # original_pet_slice = img_pet_data[j, :, :]
        # print('data match = ', np.all(load_pet == original_pet_slice))


foldList = glob.glob('E:/HSE/LungCancer/yolov3/data/images/train/*/')
count = 0

for i in foldList:
    nifti_convert(i)
    count += 1
    print('count = ', count)

# convert nii file into image file
# to use as input for yolov3
# make ct, pet file into one image
# use either 2 channel of ct, 1 channel of pet OR 1 channel of ct, 2 channel of pet

# import SimpleITK as sitk
# import glob
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# import os
#
# # ctList type =  <class 'list'>
# # ctList =  ['E:/HSE/2dtempdata\\10918160\\CT_cut.nii.gz']
# # ctList[0] =  E:/HSE/2dtempdata\10918160\CT_cut.nii.gz
# # img ct type =  <class 'numpy.ndarray'>
# # img ct data shape =  (80, 128, 160)
#
#
# def nifti_convert(fPath):
#     ct_file  = fPath + 'CT_cut.nii.gz'
#     pet_file = fPath + 'PET_cut.nii.gz'
#     roi_file = fPath + 'ROI_cut.nii.gz'
#     # path of txt files that contain mean, std
#     data_file = fPath + 'img_data.txt'
#
#     # get mean, std values to standardization
#     f = open(data_file, 'r')
#     nums = [float(x) for x in f.read().split()]
#     f.close()
#     img_ct = sitk.ReadImage(ct_file)
#     img_ct_data = sitk.GetArrayFromImage(img_ct)
#     img_ct_data[img_ct_data > 500] = 500
#     # standardization
#     img_ct_data = (img_ct_data - nums[0]) / (nums[1] + 1e-8)
#     img_pet = sitk.ReadImage(pet_file)
#     img_pet_data = sitk.GetArrayFromImage(img_pet)
#     img_pet_data = (img_pet_data - nums[2]) / (nums[3] + 1e-8)
#     img_roi = sitk.ReadImage(roi_file)
#     img_roi_data = sitk.GetArrayFromImage(img_roi)
#
#     nzero = img_roi_data.nonzero()
#     new_nzero = []
#     for i in nzero[0]:
#         if i not in new_nzero:
#             new_nzero.append(i)
#
#     start_idx = new_nzero[0]
#     end_idx = new_nzero[-1]
#
#     # j = start_idx
#     for j in range(start_idx, end_idx + 1):
#         num = '{0:0>3}'.format(j)
#         os.chdir(fPath)
#         ct_slice = img_ct_data[j, :, :]
#         pet_slice = img_pet_data[j, :, :]
#         data = np.stack((ct_slice, ct_slice, pet_slice), axis=-1)
#         print('data = ', data)
#         print('data type = ', type(data))
#         print('data shape = ', data.shape)
#         print('ct data shape = ', ct_slice.shape)
#         ct_img = Image.fromarray(ct_slice)
#         ct_name = 'New_CT_slice' + num + '.jpg'
#         # ct_img.save(ct_name, 'L')
#         img = Image.fromarray(data, 'RGB')
#         filename = 'CT_PET_slice' + num + '.jpg'
#         img.save(filename)
#         rewrite_filename = 'PET_rewrite_' + str(j) + '.nii.gz'
#         print('rewrite filename = ', rewrite_filename)
#         os.chdir(fPath)
#         pet_trans_img = sitk.GetImageFromArray(pet_slice)
#         sitk.WriteImage(pet_trans_img, rewrite_filename)
#
#         print('img type = ', type(img))
#         # print('img shape = ', img.shape)
#
#         load_pet = np.load(fPath + 'PET-cut-slice' + num +'.npy')
#         original_pet_slice = img_pet_data[j, :, :]
#         print('data match = ', np.all(load_pet == original_pet_slice))
#
#
# foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/wholepetct/onlyoneimage/train/10918160/')
# count = 0
#
# for i in foldList:
#     nifti_convert(i)
#     count += 1
#     print('count = ', count)