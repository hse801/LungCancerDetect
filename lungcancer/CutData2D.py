#import module
import matplotlib as mpl
import matplotlib.pylab as plt
import os
import glob
#from tqdm import tqdm_notebook
from tqdm.notebook import tqdm
import SimpleITK as sitk


# 2D 이미지를 이용하기 위해 cancer roi가 존재하는 부분에 대한 zslice들만 추출
# nonzero 함수를 이용
# ctList type =  <class 'list'>
# ctList =  ['E:/HSE/2dtempdata\\10918160\\CT_cut.nii.gz']
# ctList[0] =  E:/HSE/2dtempdata\10918160\CT_cut.nii.gz
# img ct type =  <class 'numpy.ndarray'>
# img ct data shape =  (80, 128, 160)

def cutImage2d(fPath):
    ctList = glob.glob(fPath + 'CT_cut.nii.gz')
    petList = glob.glob(fPath + 'PET_cut.nii.gz')
    roiList = glob.glob(fPath + 'ROI_cut.nii.gz')
    lymphList = glob.glob(fPath + '*nestle_cut.nii.gz')

    img_ct = sitk.ReadImage(ctList[0])
    img_ct_data = sitk.GetArrayFromImage(img_ct)
    img_pet = sitk.ReadImage(petList[0])
    img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_roi = sitk.ReadImage(roiList[0])
    img_roi_data = sitk.GetArrayFromImage(img_roi)
    nzero = img_roi_data.nonzero()
    new_nzero = []
    for i in nzero[0]:
        if i not in new_nzero:
            new_nzero.append(i)

    start_idx = new_nzero[0]
    end_idx = new_nzero[-1]

    print('start = ', start_idx)
    print('end = ', end_idx)

    os.chdir(fPath)
    sitk.WriteImage(img_ct[:, :, start_idx:end_idx], "CT_2dCut.nii.gz")
    sitk.WriteImage(img_pet[:, :, start_idx:end_idx], "PET_2dCut.nii.gz")
    sitk.WriteImage(img_roi[:, :, start_idx:end_idx], "ROI_2dCut.nii.gz")


foldList = glob.glob('E:/HSE/2dtempdata/*/')
count = 0

for i in tqdm(foldList):
    cutImage2d(i)
    count += 1
    print('count = ', count)