from scipy.interpolate import interpn

import os
import glob
from tqdm.notebook import tqdm

import numpy as np
import SimpleITK as sitk

# Lymph node data를 160x128x80의 크기로 자른다

def CropImage(fPath, patient_num):
    lymph_path = glob.glob('E:/HSE/lymph/*/RoiVolume')
    for i in lymph_path:
        lymphList = glob.glob(i + '/*.nii.gz')
        lymph_patient = i.split(os.sep)[-2]

        if lymph_patient != patient_num:
            print('not in lymph list')
            break

    ctList = glob.glob(fPath + 'CT*/2*.nii.gz')
    petList = glob.glob(fPath + 'WT*/*.nii.gz')
    lungList = glob.glob(fPath + 'Lung_seg_img.nii.gz')
    roiList = glob.glob(fPath + 'C1_nestle.nii.gz')

    if (len(roiList) != 1):
        return

    if (len(ctList) != 1 or len(petList) != 1):
        return

    if (len(lungList) != 1):
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
    if (z_mid + 40 > img_pet_data.shape[0]):
        z_max = img_pet_data.shape[0]
        z_min = z_max - 80
    elif (z_mid - 40 < 0):
        z_min = 0
        z_max = 80
    else:
        z_max = z_mid + 40
        z_min = z_max - 80

    y_mid = int((np.percentile(nzero[1], 0.01) + np.percentile(nzero[1], 99.99)) / 2)
    if (y_mid + 64 > img_pet_data.shape[2]):
        y_max = img_pet_data.shape[2]
        y_min = y_max - 128
    elif (y_mid - 64 < 0):
        y_min = 0
        y_max = 128
    else:
        y_max = y_mid + 64
        y_min = y_max - 128

    x_mid = int((np.percentile(nzero[2], 0.01) + np.percentile(nzero[2], 99.99)) / 2)
    if (x_mid + 80 > img_pet_data.shape[1]):
        x_max = img_pet_data.shape[1]
        x_min = x_max - 160
    elif (x_mid - 80 < 0):
        x_min = 0
        x_max = 160
    else:
        x_max = x_mid + 80
        x_min = x_max - 160

    #     ct_crop_img = sitk.GetImageFromArray(interp[z_min:z_max, y_min:y_max, x_min:x_max])
    #     ct_crop_img.CopyInformation(img_pet[x_min:x_max, y_min:y_max, z_min:z_max])
    #     img_roi = img_roi[::-1, :, :]

    # Lymph node
    lymph_path = glob.glob('E:/HSE/lymph/*/RoiVolume')

    for i in tqdm(lymph_path):
        #         if os.path.exists('RoiVolume'):
        #         lymphList = glob.glob(i + '/*.nii.gz')
        #         lymph_patient = i.split(os.sep)[-2]

        #         if lymph_patient == patient_num:
        #     #         print('i = ', i)
        #         for j in lymphList:
        #             print('j = ', j)
        img_lymph = sitk.ReadImage(j)
        img_lymph = img_lymph[::-1, :, :]

        lymph_filename = j.split(os.sep)[-1]
        splitted = lymph_filename.split(".")
        new_filename = splitted[0] + '_cut.nii.gz'

        #                 lymph_save = i.split(os.sep)[-2]
        #             print('lymph save = ', lymph_save)
        os.chdir('E:/HSE/lymph/' + lymph_patient)
        sitk.WriteImage(img_lymph[x_min:x_max, y_min:y_max, z_min:z_max], new_filename)
        print(new_filename, ' saved')


foldList = glob.glob('F:/03. DataSet/Lung Cancer (PET-CT)/SNUH_lung/*/')
count = 0
for i in tqdm(foldList):
    patient_num = i.split(os.sep)[-2]
    if patient_num in lymph_list:
        CropImage(i, patient_num)