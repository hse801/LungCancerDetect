from scipy.interpolate import interpn
import os
import glob
import numpy as np
import SimpleITK as sitk
import shutil
from nii_convert_whole import nifti_convert

# deal with the data that only have lymph roi data
# F:\03. DataSet\Lung Cancer (PET-CT)\SNUH_lung\* -> CT, PET before any preprocessing
# E:\HSE\lymphdata\RoiVolume -> lymph roi data
# 1. make CT_cut and PET_cut
# 2. make txt file img_data.txt that contains mean, std
# 3. create image data of 2d slices
# 4. paste to training data folder
#
# create CT_cut and PET_cut files
# for the patient who don't have lung_seg
# patient who only have lymph roi
# set certain range of x,y,z to cut
def crop_ct_pet(patient_num):
    patient_path = 'F:/03. DataSet/Lung Cancer (PET-CT)/SNUH_lung/' + patient_num + '/'
    ct_list = glob.glob(patient_path + 'CT*/2*.nii.gz')
    pet_list = glob.glob(patient_path + 'WT*/*.nii.gz')

    if len(ct_list) == 0 or len(pet_list) == 0:
        print('No CT or PET')
        return

    img_ct = sitk.ReadImage(ct_list[0])
    # print(img_ct)
    img_ct_data = sitk.GetArrayFromImage(img_ct)
    # print(img_ct_data)
    img_pet = sitk.ReadImage(pet_list[0])
    img_pet_data = sitk.GetArrayFromImage(img_pet)

    x_ct = np.arange(-img_ct.GetOrigin()[0],
                     -img_ct.GetOrigin()[0] + (-img_ct.GetSpacing()[0]) * img_ct_data.shape[1],
                     step=-img_ct.GetSpacing()[0])
    x_ct = x_ct[::-1]
    y_ct = np.arange(-img_ct.GetOrigin()[1],
                     -img_ct.GetOrigin()[1] + img_ct.GetSpacing()[1] * img_ct_data.shape[2],
                     step=img_ct.GetSpacing()[1])
    z_ct = np.arange(img_ct.GetOrigin()[2],
                     img_ct.GetOrigin()[2] + img_ct.GetSpacing()[2] * img_ct_data.shape[0],
                     step=img_ct.GetSpacing()[2])

    x_pet = np.arange(-img_pet.GetOrigin()[0],
                      -img_pet.GetOrigin()[0] + (-img_pet.GetSpacing()[0]) * img_pet_data.shape[1],
                      step=-img_pet.GetSpacing()[0])
    x_pet = x_pet[::-1]
    y_pet = np.arange(-img_pet.GetOrigin()[1],
                      -img_pet.GetOrigin()[1] + img_pet.GetSpacing()[1] * img_pet_data.shape[2],
                      step=img_pet.GetSpacing()[1])
    z_pet = np.arange(img_pet.GetOrigin()[2],
                      img_pet.GetOrigin()[2] + img_pet.GetSpacing()[2] * img_pet_data.shape[0],
                      step=img_pet.GetSpacing()[2])
    mesh_pet = np.array(np.meshgrid(z_pet, y_pet, x_pet))

    mesh_points = np.rollaxis(mesh_pet, 0, 4)
    mesh_points = np.rollaxis(mesh_points, 0, 2)
    interp = interpn((z_ct, y_ct, x_ct), img_ct_data[:, :, ::-1],
                     mesh_points, bounds_error=False, fill_value=-1024)
    interp = interp[:, :, ::-1]

    z_min = 80
    z_max = 160
    y_min = 30
    y_max = 158
    x_min = 20
    x_max = 180

    ct_crop_img = sitk.GetImageFromArray(interp[z_min:z_max, y_min:y_max, x_min:x_max])
    ct_crop_img.CopyInformation(img_pet[x_min:x_max, y_min:y_max, z_min:z_max])

    os.chdir('E:/HSE/lymphdata/' + patient_num + '/')
    sitk.WriteImage(ct_crop_img, "CT_cut.nii.gz")
    print('CT_cut.nii.gz saved in ', os.getcwd())
    sitk.WriteImage(img_pet[x_min:x_max, y_min:y_max, z_min:z_max], "PET_cut.nii.gz")
    print('PET_cut.nii.gz saved in ', os.getcwd())


roiPath = glob.glob('E:/HSE/lymphdata/*/RoiVolume/')
lymph_list = []

for i in roiPath:
    lymph_list.append(i.split(os.sep)[-3])
print('lymph list len = ', len(lymph_list))

# get the list of patients that have only lymph node and don't have C1_nestle
count = 0
only_lymph_patient = []
file_path = glob.glob('F:/03. DataSet/Lung Cancer (PET-CT)/SNUH_lung/*/')
for i in file_path:
    patient_num = i.split(os.sep)[-2]
    print('For patient ', patient_num)
    if patient_num in lymph_list:
        ct_list = glob.glob(i + 'CT*/2*.nii.gz')
        pet_list = glob.glob(i + 'WT*/*.nii.gz')
        file_exist = os.path.isfile(i + 'Lung_seg_img.nii.gz')

        if len(ct_list) == 0 or len(pet_list) == 0:
            print('No CT or PET in ', i)
            print(f'CT length = {len(ct_list)}, PET length = {len(pet_list)}')
        elif not file_exist:
            only_lymph_patient.append(patient_num)
            print('No lung data in ', i)
            # CropImage(patient_num)
            count += 1

        # get_only_lymph(i)
print(f'only lymph patient = {only_lymph_patient}')
print(f'only lymph patient num = {len(only_lymph_patient)}')
print(f'Total count = {count}')


def Normal(fPath):
    img_ct = sitk.ReadImage(fPath + 'CT_cut.nii.gz')
    img_ct_data = sitk.GetArrayFromImage(img_ct)
    img_ct_data[img_ct_data > 500] = 500
    img_pet = sitk.ReadImage(fPath + 'PET_cut.nii.gz')
    img_pet_data = sitk.GetArrayFromImage(img_pet)

    ct_mean = img_ct_data.mean()
    pet_mean = img_pet_data.mean()

    ct_std = img_ct_data.std()
    pet_std = img_pet_data.std()

    os.chdir(fPath)
    k = open('img_data.txt', mode='w')
    k.write(str(ct_mean) + ' ' + str(ct_std) + ' ' + str(pet_mean) + ' ' + str(pet_std))
    k.close()
    print('img_data file saved in ', os.getcwd())

# copy folder of patient who only have lymph node
# contain lymph roi, CT_cut, PET_cut, img_data.txt
# move all 48 patients to train data folder


def copy_folder_out(src_path, dst_path):
    shutil.copytree(src_path, dst_path)
    print('folder copied from ', src_path, ' to ', dst_path)


def copy_file_out(file_path):

    os.chdir(file_path)
    if os.path.isdir('RoiVolume_cut'):
        print('RoiVolume_cut Exists')
        lymph_roi_path = file_path + 'RoiVolume_cut/'
        print('list of file = ', os.listdir(lymph_roi_path))
        roi_list = os.listdir(lymph_roi_path)
        for f in roi_list:
            shutil.copy2(lymph_roi_path + f, file_path)
        print('file copied from ', lymph_roi_path, ' to ', file_path)


for p in only_lymph_patient:
    only_lymph_path = 'E:/HSE/lymphdata/'+ p + '/'
    dst_path = 'E:/HSE/LungCancerDetect/data/images/train/' + p + '/'
    # crop_ct_pet(p)
    # Normal(only_lymph_path)
    copy_folder_out(only_lymph_path, dst_path)
    # copy_file_out(only_lymph_path)
    # nifti_convert(only_lymph_path)



