import nibabel
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


def save_img():
    fold_list = glob.glob('E:/HSE/tempdata/*/')
    for i in tqdm(fold_list):
        src_crop = glob.glob(i + 'WT*/*.nii.gz')
        src_interp = glob.glob(i + 'CT*/2*.nii.gz')
        os.chdir(i)
        crop_img(src_file=src_crop[0], dst_file='pet_cropped.nii.gz', crop_index=[100, 190])

        ref_interp = glob.glob(i + 'pet_cropped.nii.gz')
        interp_img(src_file=src_interp[0], dst_file='ct_interp.nii.gz', ref_file=ref_interp[0])