# copy img data label(txt) in src dir to dst dir
# copy files in patient_list only
# source = "E:/HSE/PyTorch-YOLOv3/data/images/"
# src_dir / {patient_num} / {CT, PET}-cut-slice-xxx.txt (xxx = slice num)
# dst = "E:/HSE/PyTorch-YOLOv3/data/temp/labels/train/"
# dst_dir / {patient_num} / {CT, PET}-cut-slice-xxx.txt (xxx = slice num)

import os
import shutil
import glob


def copy_img_label(src_dir, dst_dir):
    patient_list = os.listdir(dst_dir)
    for p in patient_list:
        src_file_list = glob.glob(src_dir + p + '/*-cut*.txt')
        for f in src_file_list:
            print(f'copy {f} to  {dst_dir + p}')
            shutil.copy(f, dst_dir + p)


copy_img_label(src_dir=r"E:/HSE/PyTorch-YOLOv3/wholedata/images/train/",
               dst_dir=r"E:/HSE/PyTorch-YOLOv3/wholedata/labels/train/")

