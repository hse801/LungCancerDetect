import os
import glob
import shutil

"""
copytree: copy whole directory
copy2(src, dst): copy file with meta data

copy data from E:\HSE\LungCancerDetect\data\images
to E:\HSE\LungCancerData

copy nii.gz data only
"""

file_path = glob.glob('E:/HSE/LungCancerDetect/data/images/test/*/')

for f in file_path:
    print(f'file path = {f}')
    patient_num = f.split('\\')[-2]
    print(f'patient num = {patient_num}')
    nii_files = glob.glob(f + '*.nii.gz')
    print(f'nii_files = {nii_files}')
    dst_path = 'E:/HSE/LungCancerData/test/' + patient_num
    if not os.path.isdir(dst_path):
        os.makedirs(dst_path, exist_ok=True)
        print('New dst_path created')

    for nii in nii_files:
        shutil.copy2(nii, dst_path)
        print(f'{nii} copied to {dst_path}')
    # break
