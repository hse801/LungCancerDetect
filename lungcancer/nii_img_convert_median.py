# convert nii file into image file
# to use as input for yolov3
# make ct, pet file into one image
# use either 2 channel of ct, 1 channel of pet OR 1 channel of ct, 2 channel of pet
# shape = (80, 128, 160) = (z, y, x)

# transverse plane: fixed z value -> nzero[0], [j, :, :]
# frontal plane: fixed y value -> nzero[1], [:, j, :]
# median plane: fixed x value -> nzero[2], [:, :, j]


import SimpleITK as sitk
import glob
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os


def nifti_convert(fPath):
    ct_file = fPath + 'CT_cut.nii.gz'
    pet_file = fPath + 'PET_cut.nii.gz'
    # path of txt files that contain mean, std
    data_file = fPath + 'img_data.txt'
    roi_list = glob.glob(fPath + 'ROI_cut.nii.gz')

    # get mean, std values to standardization
    f = open(data_file, 'r')
    nums = [float(x) for x in f.read().split()]
    f.close()
    img_ct = sitk.ReadImage(ct_file)
    img_ct_data = sitk.GetArrayFromImage(img_ct)
    img_ct_data[img_ct_data > 500] = 500
    # standardization
    img_ct_data = (img_ct_data - nums[0]) / (nums[1] + 1e-8)
    img_ct_data[img_ct_data > 3] = 3
    ct_rgb_data = ((img_ct_data - img_ct_data.min()) / (img_ct_data.max() - img_ct_data.min()) * 255)
    ct_rgb_data = ct_rgb_data[::-1, :, ::-1]
    img_pet = sitk.ReadImage(pet_file)
    img_pet_data = sitk.GetArrayFromImage(img_pet)
    img_pet_data = (img_pet_data - nums[2]) / (nums[3] + 1e-8)
    # img_pet_data[img_pet_data > 3] = 3
    pet_rgb_data = ((img_pet_data - img_pet_data.min()) / (img_pet_data.max() - img_pet_data.min()) * 255)
    pet_rgb_data = pet_rgb_data[::-1, :, ::-1]
    lymph_list = glob.glob(fPath + '*_lymph_cut.nii.gz')

    patient_num = fPath.split('\\')[-2]
    print(f'patient_num = {patient_num}')

    print('ct max = ', img_ct_data.max(), ' , pet max = ', img_pet_data.max())
    print('ct min = ', img_ct_data.min(), ' , pet min = ', img_pet_data.min())
    print('ct mean = ', img_ct_data.mean(), ' , pet mean = ', img_pet_data.mean())
    print('ct rgb max = ', ct_rgb_data.max(), ' , pet rgb max = ', pet_rgb_data.max())
    print('ct rgb min = ', ct_rgb_data.min(), ' , pet rgb max = ', pet_rgb_data.min())
    print('ct rgb mean = ', ct_rgb_data.mean(), ' , pet rgb mean = ', pet_rgb_data.mean())
    print('ct rgb shape = ', ct_rgb_data.shape, ' , pet rgb shape = ', pet_rgb_data.shape)

    if len(roi_list) >= 1:
        img_roi = sitk.ReadImage(roi_list[0])
        img_roi_data = sitk.GetArrayFromImage(img_roi)
        print(f'img_roi shape = {img_roi_data.shape}')

        nzero = img_roi_data.nonzero()
        new_nzero = []

        for i in nzero[2]:
            if i not in new_nzero:
                new_nzero.append(i)

        start_idx = min(new_nzero)
        end_idx = max(new_nzero)
        print(f'nzero = {nzero}')
        # print(f'nzero shape = {nzero.shape}')
        print(f'new nzero = {new_nzero}')
        print(f'start idx = {start_idx}, end idx = {end_idx}')
        j = start_idx

        print(f'fPath = {fPath}')

        for j in range(start_idx, end_idx + 1):
            num = '{0:0>3}'.format(j)
            os.chdir(fPath)
            ct_slice = ct_rgb_data[:, :, j]
            pet_slice = pet_rgb_data[:, :, j]
            print(f'ct slice = {ct_slice.shape}')
            # zero_arr = np.zeros((128, 160))
            # data = np.stack((ct_slice, ct_slice, pet_slice), axis=-1)
            # data = np.stack((ct_slice, pet_slice, zero_arr), axis=-1)
            ratio_overlay1 = 0.8
            ratio_overlay2 = 0.6
            data = np.stack((np.clip(pet_slice * ratio_overlay1 + ct_slice * ratio_overlay2, 0, 255), ct_slice * ratio_overlay2, ct_slice * ratio_overlay2), axis=-1)

            data = data.astype(np.uint8)
            img = Image.fromarray(data, 'RGB')
            filename = str(patient_num) + '_median_slice' + num + '.jpg'
            img.save(filename)
            print(filename, ' saved')

    # if lymph roi file exist
    if lymph_list:
        print(f'lymph list = {lymph_list}')
        for l in lymph_list:
            img_lymph = sitk.ReadImage(l)
            img_lymph_data = sitk.GetArrayFromImage(img_lymph)
            nzero = img_lymph_data.nonzero()
            # print(f'nzero = {nzero}, type of nzero = {type(nzero)}')
            new_nzero_slice = []
            for i in nzero[2]:
                if i not in new_nzero_slice:
                    new_nzero_slice.append(i)
            # print(f'new nzero = {new_nzero_slice}, type of nzero = {type(new_nzero_slice)}')
            # If ROI data is empty
            if new_nzero_slice == []:
                print('ROI is empty')
                continue
            # print('new nonzero = ', new_nzero_slice)

            start_idx = min(new_nzero_slice)
            end_idx = max(new_nzero_slice)
            print(f'start idx = {start_idx}, end idx = {end_idx}')
            for j in range(start_idx, end_idx + 1):
                num = '{0:0>3}'.format(j)
                os.chdir(fPath)
                ct_slice = ct_rgb_data[:, :, j]
                pet_slice = pet_rgb_data[:, :, j]
                print(f'ct slice = {ct_slice.shape}')

                ratio_overlay1 = 0.8
                ratio_overlay2 = 0.6
                data = np.stack((np.clip(pet_slice * ratio_overlay1 + ct_slice * ratio_overlay2, 0, 255),
                                 ct_slice * ratio_overlay2, ct_slice * ratio_overlay2), axis=-1)

                data = data.astype(np.uint8)
                img = Image.fromarray(data, 'RGB')
                filename = str(patient_num) + '_median_slice' + num + '.jpg'
                img.save(filename)
                print(filename, ' saved')


def get_labels(fPath):
    # ct_list = glob.glob(fPath + 'CT_Cut.nii.gz')
    roi_list = glob.glob(fPath + 'ROI_cut.nii.gz')
    lymph_list = glob.glob(fPath + '*_lymph_cut.nii.gz')

    patient_num = fPath.split('\\')[-2]
    print(f'patient_num = {patient_num}')

    if len(roi_list) >= 1:
        print('ROI_cut exists in ', fPath)
        img_roi = sitk.ReadImage(roi_list[0])
        img_roi_data = sitk.GetArrayFromImage(img_roi)
        nzero = img_roi_data.nonzero()
        new_nzero_slice = []
        for i in nzero[2]:
            if i not in new_nzero_slice:
                new_nzero_slice.append(i)
        # print('new nonzero = ', new_nzero_slice)

        start_idx = min(new_nzero_slice)
        end_idx = max(new_nzero_slice)
        print(f'start idx = {start_idx}, end idx = {end_idx}')
        for i in range(np.shape(img_roi_data)[2]):
            # if start_idx > i or end_idx < i:
            #     os.chdir(fPath)
            #     num = '{0:0>3}'.format(i)
            #     with open(patient_num + "_slice" + str(num) + ".txt", "w") as f:
            #         pass
            if start_idx <= i <= end_idx:
                roi_slice = img_roi_data[:, :, i]
                nzero = roi_slice.nonzero()
                print(f'roi_slice = {roi_slice}')
                # print('nzero = ', nzero[2])
                # print(f'nzero shape = {nzero.shape}')
                new_nzero_w = [] # 128, y
                new_nzero_h = [] # 80, z
                for j in nzero[1]:
                    if j not in new_nzero_w:
                        new_nzero_w.append(j)
                for k in nzero[0]:
                    if k not in new_nzero_h:
                        new_nzero_h.append(k)
                # normalize with image width and height (128x80)
                centerX = ((min(new_nzero_w) + max(new_nzero_w)) / 2)/np.shape(img_roi_data)[1]
                centerY = 1 - (((min(new_nzero_h) + max(new_nzero_h)) / 2)/np.shape(img_roi_data)[0])
                # centerY = 1 - centerY
                w = (max(new_nzero_w) - min(new_nzero_w))/np.shape(img_roi_data)[1]
                h = (max(new_nzero_h) - min(new_nzero_h))/np.shape(img_roi_data)[0]
                os.chdir(fPath)
                num = '{0:0>3}'.format(i)
                # print('num = ', num)

                with open(patient_num + "_median_slice" + str(num) + ".txt", "w") as f:
                    f.write("0 " + str(centerX) + " ")
                    f.write(str(centerY) + " ")
                    f.write(str(w) + " ")
                    f.write(str(h) + " " + "\n")
                print('Have ROI_cut and in roi')
    #         # roi에 해당하지 않는 z 인덱스의 경우 label 없는 빈 txt 파일 생성
    #         else:
    #             os.chdir(fPath)
    #             num = '{0:0>3}'.format(i)
    #             with open(patient_num + "_slice" + str(num) + ".txt", "w") as f:
    #                 pass
                # print("Have ROI_cut but not roi")
    # elif len(roi_list) == 0:
    #     for j in range(80):
    #         num = '{0:0>3}'.format(j)
    #         with open(patient_num + "_slice" + str(num) + ".txt", "w") as f:
    #             pass
    #     print('Do not have ROI_cut')

    # if lymph roi file exist
    if lymph_list:
        print(f'lymph list = {lymph_list}')
        for l in lymph_list:
            img_lymph = sitk.ReadImage(l)
            img_lymph_data = sitk.GetArrayFromImage(img_lymph)
            nzero = img_lymph_data.nonzero()
            # print(f'nzero = {nzero}, type of nzero = {type(nzero)}')
            new_nzero_slice = []
            for i in nzero[2]:
                if i not in new_nzero_slice:
                    new_nzero_slice.append(i)
            # print(f'new nzero = {new_nzero_slice}, type of nzero = {type(new_nzero_slice)}')
            # If ROI data is empty
            if new_nzero_slice == []:
                print('ROI is empty')
                continue
            # print('new nonzero = ', new_nzero_slice)

            start_idx = min(new_nzero_slice)
            end_idx = max(new_nzero_slice)
            print(f'start idx = {start_idx}, end idx = {end_idx}')

            for i in range(np.shape(img_lymph_data)[2]):
                # if start_idx > i or end_idx < i:
                #     os.chdir(fPath)
                #     num = '{0:0>3}'.format(i)
                #     with open(patient_num + "_slice" + str(num) + ".txt", "a") as f:
                #         pass
                if start_idx <= i <= end_idx:
                    roi_slice = img_lymph_data[:, :, i]
                    # print('i1 = ', i)
                    nzero = roi_slice.nonzero()
                    # print('nzero = ', nzero)
                    new_nzero_w = []
                    new_nzero_h = []
                    for j in nzero[1]:
                        if j not in new_nzero_w:
                            new_nzero_w.append(j)
                    for k in nzero[0]:
                        if k not in new_nzero_h:
                            new_nzero_h.append(k)
                    # normalize with image width and height (160x80)

                    print(f'min(new_nzero_w) = {min(new_nzero_w)}, max(new_nzero_w) = {max(new_nzero_w)}')
                    print(f'min(new_nzero_h) = {min(new_nzero_h)}, max(new_nzero_h) = {max(new_nzero_h)}')
                    # print(f'np.shape(img_roi_data)[1] = {np.shape(img_roi_data)[1]}, np.shape(img_roi_data)[0] = {np.shape(img_roi_data)[0]}')
                    centerX = ((min(new_nzero_w) + max(new_nzero_w)) / 2)/np.shape(img_lymph_data)[1]
                    centerY = 1 - (((min(new_nzero_h) + max(new_nzero_h)) / 2)/np.shape(img_lymph_data)[0])
                    # centerY = 1 - centerY
                    w = (max(new_nzero_w) - min(new_nzero_w))/np.shape(img_lymph_data)[1]
                    h = (max(new_nzero_h) - min(new_nzero_h))/np.shape(img_lymph_data)[0]

                    os.chdir(fPath)
                    num = '{0:0>3}'.format(i)

                    # "a" is append mode
                    # 기존의 파일의 마지막에 추가
                    file_name = patient_num + "_median_slice" + str(num) + ".txt"
                    if os.path.isfile(fPath + '/' + file_name):
                        txt_mode = 'a'
                    else:
                        txt_mode = 'w'

                    with open(file_name, txt_mode) as f:
                        f.write("1 " + str(centerX) + " ")
                        f.write(str(centerY) + " ")
                        f.write(str(w) + " ")
                        f.write(str(h) + " " + "\n")
                    print('Patient ', l, ' Have lymph node')


# foldList = glob.glob('E:/HSE/LungCancerDetect/one/23835418/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/one/45730513/')
foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/test/*/')
# foldList = glob.glob('E:/HSE/LungCancer/yolov3/data/images/valid/45706084/')
count = 0

for i in foldList:
    nifti_convert(i)
    get_labels(i)
    count += 1
    print('count = ', count)
    # break
