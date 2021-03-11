#import module

import glob

#from tqdm import tqdm_notebook
from tqdm.notebook import tqdm
import SimpleITK as sitk
import scipy.interpolate
import numpy as np

from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
from torchvision import transforms, utils

def cutImage2d(fPath):
    ctList = glob.glob(fPath + 'CT_cancer.nii.gz')
    petList = glob.glob(fPath + 'PET_cancer.nii.gz')
    roiList = glob.glob(fPath + 'ROI_cut.nii.gz')
    lymphList = glob.glob(fPath + '*nestle_cut.nii.gz')

    # img_path = self.img_files[index % len(self.img_files)].rstrip()
    # ct_path = img_path.replace('PET', 'CT')
    # pet_img = sitk.ReadImage(ct_path[0])
    # img_pet_data = sitk.GetArrayFromImage(pet_img)
    #
    # pet_img = np.array(Image.open(img_path).convert('L'), dtype=np.uint8)
    # ct_img = np.array(Image.open(ct_path).convert('L'), dtype=np.uint8)
    # img = np.stack((pet_img, ct_img), axis=-1)
    ct_img = sitk.ReadImage(ctList[0])
    print('ctList type = ', type(ctList))
    print('ctList = ', ctList)
    print('ctList[0] = ', ctList[0])
    # print('ctList shape = ', np.shape(img_ct))
    # print('ctList shape = ', img_ct.size())
    # print('img ct shape = ', np.shape())
    # print(img_ct)
    ct_img_data = sitk.GetArrayFromImage(ct_img)
    ct_img_data[ct_img_data > 500] = 500
    print('img ct type = ', type(ct_img_data))
    print('img ct data shape = ', np.shape(ct_img_data))
    # ct_img_data = ct_img_data.reshape(1, -1, 128, 160)
    # print('img ct data shape reshape = ', np.shape(ct_img_data))
    #   print(img_ct_data)
    pet_img = sitk.ReadImage(petList[0])
    pet_img_data = sitk.GetArrayFromImage(pet_img)
    for i in range(np.shape(ct_img_data)[0]):
        print('i = ', i)
        pet_zslice = pet_img_data[i, :, :]
        print('pet_zslice len1 = ', np.shape(pet_zslice))
        # pet_zslice = pet_img_data[i, :, :].reshape(1, -1, 128, 160)
        # print('pet_zslice len2 = ', np.shape(pet_zslice))
        pet_zslice = np.transpose(pet_img_data[i, :, :])
        print('pet_zslice len = ', np.shape(pet_zslice))
        print('pet z max = ', np.max(pet_zslice))

        ct_zslice = np.transpose(ct_img_data[i, :, :])
        img = np.stack((pet_zslice, ct_zslice), axis=-1)
        print('stacked img shape = ', np.shape(img))

        # ct_zslice = ct_img_data[i, :, :]
        #

    img_roi = sitk.ReadImage(roiList[0])
    img_roi_data = sitk.GetArrayFromImage(img_roi)


foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/temp/images/test/*/')
count = 0

for i in foldList:
    cutImage2d(i)
    count += 1
    print('count = ', count)