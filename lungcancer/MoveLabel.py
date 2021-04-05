import os
import shutil
import glob
import tqdm

# label이 들어갈 폴더를 생성
# 해당 환자 이름의 빈 폴더를 생성해준다


def CopyLymph(fPath, patient_num):
    # lymph_roi_path = fPath
    # roi_patient_num = lymph_roi_path.split(os.sep)[-3]

    # if roi_patient_num in patient_list:
    #     fName = roi_patient_num
    labelPath = 'E:/HSE/PyTorch-YOLOv3/wholedata/labels/train/'
    print('fPath type', type(fPath))
    print('num type = ', type(patient_num))
    dir_name = labelPath + patient_num
    print('dir name type = ', type(dir_name))

    # os.chdir('E:/HSE/LungCancerSegmentation/PyTorch-YOLOv3/data/temp/labels/test/')
    os.mkdir(dir_name)
    # for path in dir_name:
    #     os.mkdir(path)
    # try:
    #     if not os.path.exists(dir_name):
    #         print('Directory Created . ', dir_name)
    #         os.makedirs(dir_name)
    # except OSError:
    #     print('Error: Creating Directory. ' + dir_name)

    # os.chdir('E:\HSE/LungData_Cdrive/' + patient_num)
    # shutil.copytree(lymph_roi_path, 'RoiVolume')


# labelPath = glob.glob('E:/HSE/LungCancerSegmentation/PyTorch-YOLOv3/data/temp/labels/test/')
imgPath = glob.glob('E:/HSE/PyTorch-YOLOv3/wholedata/images/train/*/')
# patient_list = []
#
# for i in imgPath:
#     patient_num = i.split(os.sep)[-2]
#     patient_list.append(patient_num)
#
# print('lymph_only_patient num = ', patient_list)

for i in imgPath:
    print('i = ', i)
    patient_num = i.split(os.sep)[-2]
    print('lymph_only_patient num = ', patient_num)
    CopyLymph(i, patient_num)
