import SimpleITK as sitk
import glob

# count file
# count total number of slices that contain roi
# 6162


def count_file(fPath):
    file_num = 0
    roiList = glob.glob(fPath + 'ROI_cut.nii.gz')

    img_roi = sitk.ReadImage(roiList[0])
    img_roi_data = sitk.GetArrayFromImage(img_roi)
    nzero = img_roi_data.nonzero()

    new_nzero_z = []
    for i in nzero[0]:
        if i not in new_nzero_z:
            new_nzero_z.append(i)
    print('new nonzero = ', new_nzero_z)
    file_num += len(new_nzero_z)
    print('file num = ', file_num)
    return file_num


foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/images_backup/*/')
count = 0
total_file_num = 0


for i in foldList:
    total_file_num += count_file(i)
    print('total file num = ', total_file_num)
    count += 1
    print('count = ', count)