import os
import glob

# delete CT files in test, train data
# delete both image and label data
# CT and PET data are not matched yet. So use PET data only to train the model better

foldList = glob.glob('E:/HSE/PyTorch-YOLOv3/data/images/*/CT-*')
count = 0

for i in foldList:
    os.remove(i)
    count += 1
    print('count = ', count)