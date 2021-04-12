from lungmask import mask
import SimpleITK as sitk
import os
import glob
import torch

# create lung segmentation nifti file
# code from https://github.com/JoHof/lungmask


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
lymph_only_patient = ['18153556', '18682799', '18838996',
    '23525317', '23779703', '23920587', '25827660', '26158932', '26975214', '27231760', '28389826',
 '28483658', '28719922', '30282687', '30797134', '31294816', '32107061', '33287193', '33910671', '35130231',
 '36521917', '37366384', '37494708', '37650926', '38770614', '38867734', '39141644', '39342447',
 '40467687', '40733740', '42072364', '42101659', '42110569', '42153845', '42575539', '42870227', '43082915',
 '43759936', '44208563', '44252135', '44506128', '44760528', '46198794', '46392318']

if __name__ == '__main__':
    # run()
    for i in folder_path:
        lung_seg(i)
