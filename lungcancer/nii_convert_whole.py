# convert nii file into image file
# to use as input for yolov3
# make ct, pet file into one image
# use either 2 channel of ct, 1 channel of pet OR 1 channel of ct, 2 channel of pet
# convert every 80 slices into image

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
    img_ct_data[img_ct_data > 3] = 3
    ct_rgb_data = ((img_ct_data - img_ct_data.min()) / (img_ct_data.max() - img_ct_data.min()) * 255).astype(np.uint8)
    ct_rgb_data = ct_rgb_data[:, ::-1, :]
    img_pet = sitk.ReadImage(pet_file)
    img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_pet_data = (img_pet_data - nums[2]) / (nums[3] + 1e-8)
    # img_pet_data[img_pet_data > 3] = 3
    pet_rgb_data = ((img_pet_data - img_pet_data.min()) / (img_pet_data.max() - img_pet_data.min()) * 255).astype(np.uint8)
    pet_rgb_data = pet_rgb_data[:, ::-1, :]

    print('ct max = ', img_ct_data.max(), ' , pet max = ', img_pet_data.max())
    print('ct min = ', img_ct_data.min(), ' , pet min = ', img_pet_data.min())
    print('ct mean = ', img_ct_data.mean(), ' , pet mean = ', img_pet_data.mean())
    print('ct rgb max = ', ct_rgb_data.max(), ' , pet rgb max = ', pet_rgb_data.max())
    print('ct rgb min = ', ct_rgb_data.min(), ' , pet rgb max = ', pet_rgb_data.min())
    print('ct rgb mean = ', ct_rgb_data.mean(), ' , pet rgb mean = ', pet_rgb_data.mean())
    print('ct rgb shape = ', ct_rgb_data.shape, ' , pet rgb shape = ', pet_rgb_data.shape)

    for j in range(80):
        num = '{0:0>3}'.format(j)
        os.chdir(fPath)
        ct_slice = ct_rgb_data[j, :, :]
        pet_slice = pet_rgb_data[j, :, :]
        ratio_overlay1 = 0.8
        ratio_overlay2 = 0.6
        data = np.stack((np.clip(pet_slice * ratio_overlay1 + ct_slice * ratio_overlay2, 0, 255) , ct_slice * ratio_overlay2, ct_slice * ratio_overlay2), axis=-1)

        # data = np.stack((ct_slice, ct_slice, pet_slice), axis=-1)
        data = data.astype(np.uint8)
        img = Image.fromarray(data, 'RGB')
        filename = 'CT_PET_slice' + num + '.jpg'
        img.save(filename)
        print(filename, ' saved')

        # load_pet = np.load(fPath + 'PET-cut-slice' + num +'.npy')
        # original_pet_slice = img_pet_data[j, :, :]
        # print('data match = ', np.all(load_pet == original_pet_slice))


# foldList = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/')
foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')
# foldList = glob.glob('E:/HSE/LungCancer/yolov3/data/images/valid/45706084/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/one/23835418/')
count = 0

for i in foldList:
    nifti_convert(i)
    count += 1
    print('count = ', count)