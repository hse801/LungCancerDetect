from lungmask import mask
import SimpleITK as sitk
import os
import glob
import torch

# create lung segmentation nifti file
# code from https://github.com/JoHof/lungmask
# 기존의 파일들은 오른쪽 lung만 있어서 전부 다시 생성하자


def lung_seg(file_path):
    ct_file = file_path + 'CT_cut.nii.gz'
    # print(f'file path = {file_path}')
    # ct_list = glob.glob(i + 'CT*/2*.nii.gz')
    input_image = sitk.ReadImage(ct_file)
    print(f'input image type = {type(input_image)}')
    model = mask.get_model('unet', 'LTRCLobes')
    seg_arr_1 = mask.apply(input_image, model)  # default model is U-net(R231)
    seg_arr_2 = mask.apply(input_image)
    seg_arr = seg_arr_1 + seg_arr_2
    seg_arr[seg_arr > 0] = 2
    seg_img = sitk.GetImageFromArray(seg_arr)
    # seg_img_1 = sitk.GetImageFromArray(seg_arr_1)
    # seg_img_2 = sitk.GetImageFromArray(seg_arr_2)
    # seg_img = seg_img_1 + seg_img_2
    print(f'seg type = {type(seg_img)}')
    print(f'seg = {seg_img}')
    file_name = str(file_path.split('/')[-2]) + '_Lung_seg_add_1.nii.gz'
    print(f'file_name = {file_name}')
    os.chdir(file_path)
    sitk.WriteImage(seg_img, fileName=file_name)


folder_path = glob.glob('E:/HSE/LungCancerDetect/one/23835418/')


def run():
    torch.multiprocessing.freeze_support()
    print('loop')


if __name__ == '__main__':
    # run()
    for i in folder_path:
        lung_seg(i)
