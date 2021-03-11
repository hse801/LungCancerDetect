import os

# https://github.com/hse801/med2image
# nifti image를 slice별로 jpg 파일로 바꿔준다

# dir_top = 'E:\\HSE\\images\\valid'
# dir_list = os.listdir(dir_top)
#
# for folder in dir_list:
#     dir_nii = os.path.join(dir_top, folder)
#     file_ct = os.path.join(dir_nii, 'CT_Cut.nii.gz')
#
#     cmd = 'python E:/HSE/med2image/bin/med2image -i %s -d %s -o CT-cut.jpg -s -1' % (file_ct, dir_nii)
#     os.system(cmd)

dir_nii = (r'E:\HSE\PyTorch-YOLOv3\data\temp\images\test\46332866')
file_ct = os.path.join(dir_nii, 'CT_cancer.nii.gz')
cmd = 'python E:/HSE/med2image/bin/med2image -i %s -d %s -o CT-cut.jpg -s -1' % (file_ct, dir_nii)
os.system(cmd)