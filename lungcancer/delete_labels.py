import os
import glob

# delete transverse labels

foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/train/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/valid/*/')
# foldList = glob.glob('E:/HSE/LungCancerDetect/data/images/test/*/')
count = 0

for fold in foldList:
    patient_num = fold.split('\\')[-2]
    print(f'patient num = {patient_num} in {fold}')
    files = glob.glob(str(fold) + str(patient_num) + '_conv_slice*.txt')
    # files = glob.glob(str(fold) + '*-cut-*')

    for f in files:
        print(f'{f} is deleted')
        os.remove(f)
    count += 1
    print('count = ', count)
    # break