#import module

import sys
import os
import glob
import numpy as np
import SimpleITK as sitk

# delete the empty label data due to the error happened while training
# Also delete the slices of images that don't contain cancer


def GetYoloLabel(fPath):
    roiList = glob.glob(fPath + 'ROI_cut.nii.gz')

    img_roi = sitk.ReadImage(roiList[0])
    img_roi_data = sitk.GetArrayFromImage(img_roi)
    nzero = img_roi_data.nonzero()

    new_nzero_z = []
    for i in nzero[0]:
        if i not in new_nzero_z:
            new_nzero_z.append(i)
    print('new nonzero = ', new_nzero_z)

    start_idx = new_nzero_z[0]
    end_idx = new_nzero_z[-1]

    print('start idx = ', start_idx)
    print('end idx = ', end_idx)

    z_count = 0

    for i in range(np.shape(img_roi_data)[0]):
        if i < start_idx or i > end_idx:
            os.chdir(fPath)
            num = '{0:0>3}'.format(i)
            filename = "PET-cut-slice" + str(num) + ".jpg"
            labelname = "PET-cut-slice" + str(num) + ".txt"
            filename2 = "CT-cut-slice" + str(num) + ".jpg"
            labelname2 = "CT-cut-slice" + str(num) + ".txt"

            # if file exists, delete
            if os.path.isfile(filename):
                os.remove(filename)
                print('file in ', fPath, 'filename: ', filename, ' deleted')
            if os.path.isfile(labelname):
                os.remove(labelname)
                print('file in ', fPath, 'filename: ', labelname, ' deleted')
            if os.path.isfile(filename2):
                os.remove(filename2)
                print('file in ', fPath, 'filename: ', filename2, ' deleted')
            if os.path.isfile(labelname2):
                os.remove(labelname2)
                print('file in ', fPath, 'filename: ', labelname2, ' deleted')


foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/images/*/')
count = 0

for i in foldList:
    GetYoloLabel(i)
    count += 1
    print('count = ', count)