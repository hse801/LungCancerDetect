import os
import glob
import shutil

# copytree: copy whole directory
# copy2(src, dst): copy file with meta data
# copy file out of the RoiVolume_cut folder


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

file_path = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
# img_path = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')
# img_path = glob.glob('E:/HSE/LungCancerDetect/data/testset/*/')

for i in file_path:
    copy_file_out(i)