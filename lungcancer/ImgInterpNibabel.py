import nibabel
import SimpleITK as sitk
from typing import List
from pathlib import Path
import tqdm
#import module
import matplotlib as mpl
import matplotlib.pylab as plt
from scipy.interpolate import interpn
from torch.optim import lr_scheduler
import sys
import os
import glob
from tqdm.notebook import tqdm
import numpy as np
import matplotlib.pyplot as plt


def reverse_along_axis(data: np.array, axis: int):
    if axis == 0:
        data = data[::-1, :, :]
    elif axis == 1:
        data = data[:, ::-1, :]
    else:
        data = data[:, :, ::-1]
    return data


def crop_img(src_file: str, dst_file: str, crop_index: List[int]):

    start_index, end_index = crop_index
    src_img = nibabel.load(src_file)

    zorigin = src_img.affine[2][3]
    zspacing = src_img.affine[2][2]

    src_img_data = src_img.get_fdata()
    src_img_data = src_img_data.astype(np.float32)

    affine = src_img.affine
    affine[2][3] = zorigin + zspacing * start_index
    crop_img_data = src_img_data[:, :, start_index: end_index]

    nibabel.save(nibabel.Nifti1Pair(crop_img_data, affine), dst_file)


def interp_img(src_file: str, dst_file: str, ref_file: str):
    print(f'nii_resize_image: src={src_file} dst={dst_file} ref={ref_file}')
    src_img = nibabel.load(src_file)
    ref_img = nibabel.load(ref_file)
    src_coord = np.array([np.arange(d) for d in src_img.shape])
    ref_coord = np.array([np.arange(d) for d in ref_img.shape])
    src_img_data = src_img.get_fdata()

    for i in range(3):
        src_coord[i] = src_img.affine[i][i] * src_coord[i] + src_img.affine[i][3]
        ref_coord[i] = ref_img.affine[i][i] * ref_coord[i] + ref_img.affine[i][3]
        if src_img.affine[i][i] < 0:
            src_coord[i] = src_coord[i][::-1]
            src_img_data = reverse_along_axis(src_img_data, i)
        if ref_img.affine[i][i] < 0:
            ref_coord[i] = ref_coord[i][::-1]

    ref_mesh = np.rollaxis(np.array(np.meshgrid(*ref_coord)), 0, 4) # [xdim][ydim][zdim][3]
    src_resize_data = interpn(src_coord, src_img.get_fdata(), ref_mesh, bounds_error=False, fill_value=-1024)

    for i in range(3):
        if ref_img.affine[i][i] < 0:
            src_resize_data = reverse_along_axis(src_resize_data, i)
    src_resize_data = src_resize_data.astype(np.float32)

    import pathlib
    if pathlib.Path(dst_file).exists():
        print(f'{dst_file} already exists. will overwrite')
    src_resize_data = src_resize_data.swapaxes(0, 1)
    src_resize_data = src_resize_data[::-1, ::-1, :]

    nibabel.save(nibabel.Nifti1Pair(src_resize_data, ref_img.affine), dst_file)


def CropImage(fPath):
    ctList = glob.glob(fPath + 'CT*/2*.nii.gz')
    petList = glob.glob(fPath + 'WT*/*.nii.gz')

    roiList = glob.glob(fPath + 'C1_nestle.nii.gz')

    if (len(roiList) != 1):
        return

    if (len(ctList) != 1 or len(petList) != 1):
        return

    img_ct = sitk.ReadImage(ctList[0])
    # print(img_ct)
    img_ct_data = sitk.GetArrayFromImage(img_ct)
    print(img_ct_data)
    img_pet = sitk.ReadImage(petList[0])
    img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_roi = sitk.ReadImage(roiList[0])

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

    ct_crop_img = sitk.GetImageFromArray(interp[80:170, :, ::-1])
    ct_crop_img.CopyInformation(img_pet[:, :, 80:170])

    os.chdir(fPath)
    sitk.WriteImage(ct_crop_img, "CT_crop_h.nii.gz")
    sitk.WriteImage(img_pet[:, :, 80:170], "PET_crop_h.nii.gz")
    sitk.WriteImage(img_roi[::-1, :, 80:170], "ROI_crop_h.nii.gz")

def save_img():
    fold_list = glob.glob('E:/HSE/tempdata/*/')
    for i in tqdm(fold_list):
        src_crop = glob.glob(i + 'WT*/*.nii.gz')
        src_interp = glob.glob(i + 'CT*/2*.nii.gz')
        os.chdir(i)
        crop_img(src_file=src_crop[0], dst_file='pet_cropped.nii.gz', crop_index=[100, 190])

        ref_interp = glob.glob(i + 'pet_cropped.nii.gz')
        interp_img(src_file=src_interp[0], dst_file='ct_interp.nii.gz', ref_file=ref_interp[0])
