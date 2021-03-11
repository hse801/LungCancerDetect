import SimpleITK as sitk
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
# ctList type =  <class 'list'>
# ctList =  ['E:/HSE/2dtempdata\\10918160\\CT_cut.nii.gz']
# ctList[0] =  E:/HSE/2dtempdata\10918160\CT_cut.nii.gz
# img ct type =  <class 'numpy.ndarray'>
# img ct data shape =  (80, 128, 160)

# To use nifti file to train
# save nifti file's data in numpy array
# save as file .npy


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
    img_pet = sitk.ReadImage(pet_file)
    img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_pet_data = (img_pet_data - nums[2]) / (nums[3] + 1e-8)
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
        ct_slice = np.transpose(img_ct_data[j, :, :])
        np.save(fPath + 'CT-cut-slice' + num, ct_slice)
        print('ct slice array shape = ', ct_slice.shape)
        print('CT data saved in ', fPath , 'for slice', j)
        pet_slice = np.transpose(img_pet_data[j, :, :])
        np.save(fPath + 'PET-cut-slice' + num, pet_slice)
        print('PET data saved in ', fPath, 'for slice', j)

        load_pet = np.load(fPath + 'PET-cut-slice' + num +'.npy')
        original_pet_slice = img_pet_data[j, :, :]
        print('data match = ', np.all(load_pet == original_pet_slice))


# foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/petctsample/*/')
# foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/temp/images/test/46332866/')
# nifti_convert('E:/HSE/PyTorch-YOLOv3/data/temp/images/test/46332866/')
# foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/temp/images/test/*/')
# foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/wholepetct/images/train/*/')
foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/wholepetct/onlyoneimage/train/10918160/')
count = 0

for i in foldList:
    nifti_convert(i)
    count += 1
    print('count = ', count)

# 주석 포함
# def nifti_convert(fPath):
#     ct_file  = fPath + 'CT_cut.nii.gz'
#     pet_file = fPath + 'PET_cut.nii.gz'
#     roi_file = fPath + 'ROI_cut.nii.gz'
#     data_file = fPath + 'img_data.txt'
#
#     f = open(data_file, 'r')
#     nums = [float(x) for x in f.read().split()]
#     f.close()
#     img_ct = sitk.ReadImage(ct_file)
#     img_ct_data = sitk.GetArrayFromImage(img_ct)
#     img_ct_data = (img_ct_data - nums[0]) / (nums[1] + 1e-8)
#     # img_ct_data = img_ct_data.reshape(1, -1, 128, 160)
#     # print('shape = ', np.shape(img_ct_data))
#     img_pet = sitk.ReadImage(pet_file)
#     img_pet_data = sitk.GetArrayFromImage(img_pet)
#     img_pet_data = (img_pet_data - nums[2]) / (nums[3] + 1e-8)
#     img_roi = sitk.ReadImage(roi_file)
#     img_roi_data = sitk.GetArrayFromImage(img_roi)
#     print('img_pet_data type = ', type(img_pet_data))
#
#
#
#     nzero = img_roi_data.nonzero()
#     #     print('nzero = ',nzero)
#     #     print('nzero shape = ', np.shape(nzero))
#     #     print('nonzero z index = ', nzero[0])
#     new_nzero = []
#     for i in nzero[0]:
#         if i not in new_nzero:
#             new_nzero.append(i)
#     print('new nonzero = ', new_nzero)
#
#     start_idx = new_nzero[0]
#     end_idx = new_nzero[-1]
#
#     print('start = ', start_idx)
#     print('end = ', end_idx)
#     print('ct shape = ', np.shape(img_ct_data))
#     print('pet shape = ', np.shape(img_pet_data))
#     # print('roi shape = ', np.shape(img_roi_data))
#
#     # j = start_idx
#     for j in range(start_idx, end_idx + 1):
#         num = '{0:0>3}'.format(j)
#         # ct_trans = np.transpose(img_ct_data[j, :, :])
#         ct_trans = img_ct_data[j, :, :]
#         print('ct slice trans shape = ', np.shape(ct_trans))
#         np.save(fPath + 'CT-cut-slice' + num, ct_trans)
#         print('img ct data = ', img_ct_data[j, 0, :])
#         # np.save(fPath + 'CT-cut-slice' + num, img_ct_data[j, :, :])
#         # load_ct = np.load(fPath + 'CT-cut-slice' + num +'.npy')
#
#         # pet_trans = np.transpose(img_pet_data[j, :, :])
#         pet_trans = img_pet_data[j, :, :]
#         print('pet trans shape = ', pet_trans.shape)
#         np.save(fPath + 'PET-cut-slice' + num, pet_trans)
#         # pet_trans = pet_trans.reshape(1, 160, 128)
#         print('pet trans shape = ', pet_trans.shape)
#         print('pet trans type = ', type(pet_trans))
#         print('img pet data = ', img_pet_data[j, 0, :])
#         print('img pet data shape = ', img_pet_data[j, 0, :].shape)
#         rewrite_filename = 'PET_rewrite_' + str(j) + '.nii.gz'
#         print('rewrite filename = ', rewrite_filename)
#         os.chdir(fPath)
#         pet_trans_img = sitk.GetImageFromArray(pet_trans)
#         sitk.WriteImage(pet_trans_img, rewrite_filename)
#         # np.save(fPath + 'PET-cut-slice' + num, img_pet_data[j, :, :])
#         load_pet = np.load(fPath + 'PET-cut-slice' + num +'.npy')
#         original_pet_slice = img_pet_data[j, :, :]
#         print('data match = ', np.all(load_pet == original_pet_slice))
#         # print('Same = ', np.all(ct_trans == load_ct))
#     # print('ct slice shape = ', np.shape(img_ct_data[j, :, :]))
#     # print('ct slice trans shape = ', np.shape(ct_trans))
#     # print('load ct = ', load_ct)
#     #
#     # print('load pet = ', load_pet)
#     # print('trans pet array = ', pet_trans)
#     # print('pet max = ', np.max(pet_trans))
#     # plt.imshow(pet_trans)
#     # pet_max = np.max(pet_trans)
#     # pet_trans = pet_trans * 255 /pet_max
#     # print('pet_trans max ', np.max(pet_trans), 'size =',pet_trans.shape)
#     # pil_pet = Image.fromarray(pet_trans)
#     # pil_pet.show()
#     # pil_ct = Image.fromarray(img_pet_data[j, :, :])
#     # pil_ct.show()
