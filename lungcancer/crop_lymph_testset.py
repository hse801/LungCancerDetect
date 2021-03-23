from scipy.interpolate import interpn

import os
import glob
from tqdm.notebook import tqdm

import numpy as np
import SimpleITK as sitk


# Lymph node data를 160x128x80의 크기로 자른다
# 'C:\Users\Bohye\data' 복사해서 'E:/HSE/lymphdata/*/'로 이동
# 'E:/HSE/lymphdata/*/' 디렉토리에 전체 RoiVolume data 있음
# RoiVolume_cut 폴더 생성하여 80으로 크롭한 data 저장



def CropImage(fPath, patient_num):
    # lymph_path = glob.glob('E:/HSE/lymph/*/RoiVolume')
    # for i in lymph_path:
    #     lymph_list = glob.glob(i + '/*.nii.gz')
    #     lymph_patient = i.split(os.sep)[-2]
    #
    #     if lymph_patient != patient_num:
    #         print('not in lymph list')
    #         break
    print('check 1')
    ctList = glob.glob(fPath + 'CT*/2*.nii.gz')
    petList = glob.glob(fPath + 'WT*/*.nii.gz')
    lungList = glob.glob(fPath + 'Lung_seg_img.nii.gz')
    roiList = glob.glob(fPath + 'C1*_nestle.nii.gz')

    if len(roiList) != 1:
        print('No Roi')
        return

    if len(ctList) != 1 or len(petList) != 1:
        print('No CT or PET')
        return

    if len(lungList) != 1:
        print('No lung data')
        return

    img_ct = sitk.ReadImage(ctList[0])
    img_ct_data = sitk.GetArrayFromImage(img_ct)
    img_pet = sitk.ReadImage(petList[0])
    img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_roi = sitk.ReadImage(roiList[0])

    x_ct = np.arange(-img_ct.GetOrigin()[0], -img_ct.GetOrigin()[0] + (-img_ct.GetSpacing()[0]) * img_ct_data.shape[1],
                     step=-img_ct.GetSpacing()[0])
    x_ct = x_ct[::-1]
    y_ct = np.arange(-img_ct.GetOrigin()[1], -img_ct.GetOrigin()[1] + img_ct.GetSpacing()[1] * img_ct_data.shape[2],
                     step=img_ct.GetSpacing()[1])
    z_ct = np.arange(img_ct.GetOrigin()[2], img_ct.GetOrigin()[2] + img_ct.GetSpacing()[2] * img_ct_data.shape[0],
                     step=img_ct.GetSpacing()[2])

    x_pet = np.arange(-img_pet.GetOrigin()[0],
                      -img_pet.GetOrigin()[0] + (-img_pet.GetSpacing()[0]) * img_pet_data.shape[1],
                      step=-img_pet.GetSpacing()[0])
    x_pet = x_pet[::-1]
    y_pet = np.arange(-img_pet.GetOrigin()[1],
                      -img_pet.GetOrigin()[1] + img_pet.GetSpacing()[1] * img_pet_data.shape[2],
                      step=img_pet.GetSpacing()[1])
    z_pet = np.arange(img_pet.GetOrigin()[2], img_pet.GetOrigin()[2] + img_pet.GetSpacing()[2] * img_pet_data.shape[0],
                      step=img_pet.GetSpacing()[2])
    mesh_pet = np.array(np.meshgrid(z_pet, y_pet, x_pet))

    mesh_points = np.rollaxis(mesh_pet, 0, 4)
    mesh_points = np.rollaxis(mesh_points, 0, 2)
    interp = interpn((z_ct, y_ct, x_ct), img_ct_data[:, :, ::-1], mesh_points, bounds_error=False, fill_value=-1024)
    interp = interp[:, :, ::-1]

    img_lung = sitk.ReadImage(lungList[0])
    img_lung_data = sitk.GetArrayFromImage(img_lung)

    # os.chdir(fPath)
    nzero = img_lung_data.nonzero()

    z_min = 0
    z_max = 0
    y_min = 0
    y_max = 0
    x_min = 0
    x_max = 0

    z_mid = int((np.percentile(nzero[0], 0.01) + np.percentile(nzero[0], 99.99)) / 2)
    if z_mid + 40 > img_pet_data.shape[0]:
        z_max = img_pet_data.shape[0]
        z_min = z_max - 80
    elif z_mid - 40 < 0:
        z_min = 0
        z_max = 80
    else:
        z_max = z_mid + 40
        z_min = z_max - 80

    y_mid = int((np.percentile(nzero[1], 0.01) + np.percentile(nzero[1], 99.99)) / 2)
    if y_mid + 64 > img_pet_data.shape[2]:
        y_max = img_pet_data.shape[2]
        y_min = y_max - 128
    elif y_mid - 64 < 0:
        y_min = 0
        y_max = 128
    else:
        y_max = y_mid + 64
        y_min = y_max - 128

    x_mid = int((np.percentile(nzero[2], 0.01) + np.percentile(nzero[2], 99.99)) / 2)
    if x_mid + 80 > img_pet_data.shape[1]:
        x_max = img_pet_data.shape[1]
        x_min = x_max - 160
    elif x_mid - 80 < 0:
        x_min = 0
        x_max = 160
    else:
        x_max = x_mid + 80
        x_min = x_max - 160

    #     ct_crop_img = sitk.GetImageFromArray(interp[z_min:z_max, y_min:y_max, x_min:x_max])
    #     ct_crop_img.CopyInformation(img_pet[x_min:x_max, y_min:y_max, z_min:z_max])
    #     img_roi = img_roi[::-1, :, :]
    print('check 2')
    # Lymph node
    lymph_path = 'E:/HSE/lymphdata/'+ patient_num + '/RoiVolume/'
    print('lymph path = ', lymph_path)
    # lymph_path = glob.glob('E:/HSE/LungCancerDetect/one/23835418/')
    # lymph_path = glob.glob('C:/Users/Bohye/data/*/RoiVolume/')

    # file name of the lymph node data
    lymph_list = os.listdir(lymph_path)
    print('lymph list = ', lymph_list)
    # print('i = ', i)
    # print('i.split(os.sep)[-1] = ', i.split('/')[-2])
    lymph_patient = lymph_path.split('/')[3]
    print('lymph patient = ', lymph_patient)
    print('patient num = ', patient_num)
    print('is lymph_patient == patient_num : ', lymph_patient == patient_num)
    print('check 3')

    for j in lymph_list:
        print('j = ', j)
        full_path = lymph_path + j
        print('full path of lymph node = ', full_path)
        img_lymph = sitk.ReadImage(full_path)
        img_lymph = img_lymph[::-1, :, :]
        lymph_filename = full_path.split(os.sep)[-1]
        splitted = lymph_filename.split(".")
        new_filename = splitted[0] + '_lymph_cut.nii.gz'
        new_filename = new_filename.replace('RoiVolume', 'RoiVolume_cut')
        print('splitted[0] = ', splitted[0])
        print('new file name = ', new_filename)
#             lymph_save = i.split(os.sep)[-2]
#             print('lymph save = ', lymph_save)
#         os.chdir('E:/HSE/lymph/' + patient_num + '/RoiVolume_cut/')
        sitk.WriteImage(img_lymph[x_min:x_max, y_min:y_max, z_min:z_max], new_filename)
        print(new_filename, ' saved')
    print('check 4')


# Create RoiVolume_cut Folder to save cropped lymph node data
# fold_path = glob.glob('E:/HSE/lymphdata/*/')
# count = 0
#
# for i in fold_path:
#     os.makedirs(i + 'RoiVolume_cut/', exist_ok=True)
#     count += 1
# print('count = ', count)

foldList = glob.glob('F:/03. DataSet/Lung Cancer (PET-CT)/SNUH_lung/*/')
count = 0

roiPath = glob.glob('E:/HSE/lymphdata/*/RoiVolume/')
lymph_list = []

for i in roiPath:
    lymph_list.append(i.split(os.sep)[-3])
print('lymph list len = ', len(lymph_list))

for i in foldList:
    patient_num = i.split(os.sep)[-2]
    print('For patient ', patient_num)
    if patient_num in lymph_list:
        CropImage(i, patient_num)
        count += 1
        print('Total count = ', count)
